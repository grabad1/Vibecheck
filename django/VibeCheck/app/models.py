from django.db import models
from django.contrib.auth.models import User as djangoUser


class User(models.Model):
    iduser = models.AutoField(db_column='idUser', primary_key=True)
    type = models.CharField(max_length=9)
    idauth = models.OneToOneField(djangoUser, on_delete=models.CASCADE, db_column='idauth')

    class Meta:
        managed = True
        db_table = 'user'


class Playlist(models.Model):
    idplaylist = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'playlist'


class Song(models.Model):
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
    idcollab = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45, blank=True, null=True)
    iduser = models.ForeignKey(User, on_delete=models.CASCADE, db_column='iduser')
    idplaylist = models.ForeignKey(Playlist, on_delete=models.CASCADE, db_column='idplaylist', blank=True, null=True)
    status = models.CharField(max_length=45)

    class Meta:
        managed = True
        db_table = 'collab'


class Requestfriendship(models.Model):
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
    id = models.AutoField(primary_key=True)
    request = models.ForeignKey(Requestfriendship, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        managed = True
        db_table = 'friendship'


class Requestcollab(models.Model):
    idrc = models.AutoField(primary_key=True)
    idusersend = models.ForeignKey(User, on_delete=models.CASCADE, db_column='idusersend')
    iduserrecieve = models.ForeignKey(User, on_delete=models.CASCADE, db_column='iduserrecieve', related_name='requestcollab_received')
    idcollab = models.ForeignKey(Collab, on_delete=models.CASCADE, db_column='idcollab')
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'requestcollab'


class Participated(models.Model):
    id = models.AutoField(primary_key=True)
    iduser = models.ForeignKey(User, on_delete=models.CASCADE, db_column='iduser')
    idcollab = models.ForeignKey(Collab, on_delete=models.CASCADE, db_column='idcollab')

    class Meta:
        managed = True
        db_table = 'participated'


class Created(models.Model):
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
    idpur = models.AutoField(primary_key=True)
    iduser = models.ForeignKey(User, on_delete=models.CASCADE, db_column='iduser')
    date = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'purchased'