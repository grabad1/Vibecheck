from django.db import models
from django.contrib.auth.models import User as djangoUser


class User(models.Model):
    """
    Korisnik aplikacije koji je povezan putem Django autentifikacije.

    Ova klasa prosiruje Django User model sa dodatnim informacijama o tipu
    korisnika (regular, premium, moderator, admin).
    """
    iduser = models.AutoField(db_column='idUser', primary_key=True)
    type = models.CharField(max_length=9)
    idauth = models.OneToOneField(djangoUser, on_delete=models.CASCADE, db_column='idauth')

    class Meta:
        managed = True
        db_table = 'user'


class Playlist(models.Model):
    """
    Predstavlja kolekciju pesama koju kreiraju korisnici.

    Svaka plejlista moze sadrzati više pesama i moze biti deo kolaboracije
    izmedju vise korisnika.
    """
    idplaylist = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'playlist'


class Song(models.Model):
    """
    Predstavlja pesmu iz Spotify kataloga.

    Sadrzi informacije o pesmi kao što su naziv, umetnik, trajanje i link
    do slike. Svaka pesma je jedinstvena po spotify_id.
    """
    idsong = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)
    link = models.CharField(max_length=150)
    artist = models.CharField(max_length=45, blank=True, null=True)
    imagelink = models.CharField(max_length=150, blank=True, null=True)
    duration = models.IntegerField(blank=True, null=True)
    spotify_id = models.CharField(unique=True, max_length=50)
    duration_string = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'song'


class Collab(models.Model):
    """
    Predstavlja kolaboraciju izmedju korisnika na zajednickoj plejlisti.

    Status moze biti 'created' (u kreiranju) ili 'active' (aktivna kolaboracija).
    Kolaboracija je povezana sa korisnikom :model:`app.User` koji je inicijator
    i sa plejlistom :model:`app.Playlist` na kojoj se radi.
    """
    idcollab = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45, blank=True, null=True)
    iduser = models.ForeignKey(User, on_delete=models.CASCADE, db_column='iduser')
    idplaylist = models.ForeignKey(Playlist, on_delete=models.CASCADE, db_column='idplaylist', blank=True, null=True)
    status = models.CharField(max_length=45)

    class Meta:
        managed = True
        db_table = 'collab'


class Requestfriendship(models.Model):
    """
    Predstavlja zahtev za prijateljstvo izmedju dva korisnika.

    Sadrzi informacije o posiljaocu i primaocu zahteva, kao i vremenske
    informacije kada je zahtev poslat. Svaki par korisnika :model:`app.User` moze imati samo
    jedan aktivan zahtev buduci da postoji unique constraint.
    """
    idrf = models.AutoField(primary_key=True)
    idusersend = models.ForeignKey(User, on_delete=models.CASCADE, db_column='idusersend', related_name='friend_requests_sent')
    iduserrecieve = models.ForeignKey(User, on_delete=models.CASCADE, db_column='iduserrecieve', related_name='friend_requests_received')
    time = models.DateTimeField(auto_now_add=True)  # ← auto_now_add за креирање

    class Meta:
        managed = True
        db_table = 'requestfriendship'
        constraints = [
            models.UniqueConstraint(fields=['idusersend', 'iduserrecieve'], name='unique_friend_request')
        ]


class Friendship(models.Model):
    """
    Predstavlja potvrdjeno prijateljstvo izmedju dva korisnika.

    Kreira se nakon sto je primalac prihvatio zahtev za prijateljstvo.
    Povezana je sa :model:`app.Requestfriendship` koji sadrzi inicijatora zahteva.
    """
    id = models.AutoField(primary_key=True)
    request = models.ForeignKey(Requestfriendship, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        managed = True
        db_table = 'friendship'


class Requestcollab(models.Model):
    """
    Predstavlja zahtev za pridruzivanje kolaboraciji.

    Jedan korisnik :model:`app.User` (posiljalac) poziva drugog (primalac) da se pridruzi
    njegovoj kolaboraciji :model:`app.Collab`. Sadrzi informaciju o vremenu kada je zahtev poslat.
    """
    idrc = models.AutoField(primary_key=True)
    idusersend = models.ForeignKey(User, on_delete=models.CASCADE, db_column='idusersend')
    iduserrecieve = models.ForeignKey(User, on_delete=models.CASCADE, db_column='iduserrecieve', related_name='requestcollab_received')
    idcollab = models.ForeignKey(Collab, on_delete=models.CASCADE, db_column='idcollab')
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'requestcollab'


class Participated(models.Model):
    """
    Povezuje korisnika sa kolaboracijom u kojoj je ucesnik.

    Cuva informaciju o tome koji su ucesnici :model:`app.User`
    deo odredjene kolaboracije :model:`app.Collab` i omogucava
    pracenje ko je radio na kojoj kolaboraciji.
    """
    id = models.AutoField(primary_key=True)
    iduser = models.ForeignKey(User, on_delete=models.CASCADE, db_column='iduser')
    idcollab = models.ForeignKey(Collab, on_delete=models.CASCADE, db_column='idcollab')

    class Meta:
        managed = True
        db_table = 'participated'


class Created(models.Model):
    """
    Povezuje korisnika sa plejlistom koju je kreirao.

    Cuva informaciju o tome ko :model:`app.User` je
    kreirao koju plejlistu :model:`app.Playlist`, kao i
    trending status koji ukazuje da li je plejlista u trending sekciji.
    Svaki par korisnik-plejlista je jedinstven.
    """
    id = models.AutoField(primary_key=True)
    iduser = models.ForeignKey(User, on_delete=models.CASCADE, db_column='iduser')
    idplaylist = models.ForeignKey(Playlist, on_delete=models.CASCADE, db_column='idplaylist')
    trending = models.IntegerField(blank=True, null=True, default=0)

    class Meta:
        managed = True
        db_table = 'created'
        constraints = [
            models.UniqueConstraint(fields=['iduser', 'idplaylist'], name='unique_created')
        ]


class Contains(models.Model):
    """
    Povezuje pesmu sa plejlistom i cuva informaciju ko je dodao pesmu.

    Omogucava pracenje koje pesme :model:`app.Song` se
    nalaze u kojoj plejlisti :model:`app.Playlist`,
    kao i koji korisnik :model:`app.User` je dodao tu pesmu.
    Svaka kombinacija plejlista-pesma je jedinstvena.
    """
    id = models.AutoField(primary_key=True)
    idplaylist = models.ForeignKey(Playlist, on_delete=models.CASCADE, db_column='idplaylist')
    idsong = models.ForeignKey(Song, on_delete=models.CASCADE, db_column='idsong')
    iduser = models.ForeignKey(User, on_delete=models.CASCADE, db_column='iduser')

    class Meta:
        managed = True
        db_table = 'contains'
        constraints = [
            models.UniqueConstraint(fields=['idplaylist', 'idsong'], name='unique_playlist_song')
        ]


class Liked(models.Model):
    """
    Korisnik moze da lajkuje plejlistu.

    Cuva informaciju koji korisnici :model:`app.User` su ostavili like na
    kojoj plejlisti :model:`app.Created`, kao i kada su to uradili.
    Svaki korisnik moze ostaviti samo jedan like na jednoj plejlisti.
    """
    id = models.AutoField(primary_key=True)
    created = models.ForeignKey(Created, on_delete=models.CASCADE)
    iduser = models.ForeignKey(User, on_delete=models.CASCADE, db_column='iduser')
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'liked'
        constraints = [
            models.UniqueConstraint(fields=['created', 'iduser'], name='unique_liked')
        ]


class Rated(models.Model):
    """
    Korisnik moze da oceni plejlistu.

    Cuva informaciju o tome koji je korisnik :model:`app.User`
    dao koju ocenu plejlisti :model:`app.Created`, samu ocenu (rating)
    i vreme kada je ocena data.
    Svaki korisnik moze dati samo jednu ocenu po plejlisti (moze je azurirati).
    """
    id = models.AutoField(primary_key=True)
    created = models.ForeignKey(Created, on_delete=models.CASCADE)
    iduser = models.ForeignKey(User, on_delete=models.CASCADE, db_column='iduser')
    rating = models.IntegerField(default=0)
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'rated'
        constraints = [
            models.UniqueConstraint(fields=['created', 'iduser'], name='unique_rated')
        ]


class Purchased(models.Model):
    """
    Predstavlja kupovinu premium pretplate od strane korisnika.

    Cuva informaciju o tome koji korisnik :model:`app.User` je kupio
    premium pretplatu i kada je to ucinio.
    Koristi se za pracenje validnosti premium statusa (30 dana od kupovine).
    """
    idpur = models.AutoField(primary_key=True)
    iduser = models.ForeignKey(User, on_delete=models.CASCADE, db_column='iduser')
    date = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'purchased'