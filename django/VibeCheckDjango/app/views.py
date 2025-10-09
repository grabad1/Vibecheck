from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User as djangoUser
from django.shortcuts import render, redirect
from .models import *
# Create your views here.
def index(request):
    return render(request, 'index.html')

def checkout(request):
    return render(request, 'checkout.html')

def admin(request):
    return render(request, 'admin.html')

def createCollab(request):
    return render(request, 'createCollab.html')

def loginuser(request):
    if request.user.is_authenticated:
        return redirect('user')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = djangoUser.objects.get(username=username)
        except:
            mess = "Ne postoji korisnik"
            context = {'mess': mess}
            return render(request, 'login.html', context)
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('user')
        else:
            mess = "Neisparvna lozinka"
            context = {'mess': mess}
            return render(request, 'login.html', context)
    else:
        return render(request, 'login.html')

def moderator(request):
    return render(request, 'moderator.html')

def passwordChange(request):
    return render(request, 'passwordChange.html')

def playlist(request, idplaylist):
    playlist = Playlist.objects.get(idplaylist=idplaylist)
    return render(request, 'playlist.html')

def playlistView(request):
    return render(request, 'playlistView.html')

def pricing(request):
    return render(request, 'pricing.html')

def signup(request):
    if request.user.is_authenticated:
        return redirect('user')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        user_type = 'regular'

        if DjangoUser.objects.filter(username=username).exists():
            mess = "Korisnik već postoji"
            return render(request, 'signup.html', {'mess': mess})

        django_user = DjangoUser.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        User.objects.create(
            idauth=django_user,
            type=user_type
        )

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('user')

        mess = "Došlo je do greške prilikom kreiranja korisnika"
        return render(request, 'signup.html', {'mess': mess})

    else:
        return render(request, 'signup.html')

def successful_password_change(request):
    return render(request, 'successful_password_change.html')

def successful_payment(request):
    return render(request, 'successful_payment.html')



def user(request):
    user = request.user
    collabs = Collab.objects.filter(iduser=User.objects.filter(idauth=request.user).first())
    return render(request, 'user.html', context={'collabs':collabs, 'username': user.username})




@login_required(login_url='loginuser')
def collabPage(request, id):
    collab=Collab.objects.get(idcollab=id)
    pesme = Contains.objects.filter(idplaylist=collab.idplaylist)
    playlist = []
    for i in pesme:
        playlist.append({
            'song': i.idsong,
            'user': i.iduser.idauth
        })
        print(i.idsong.name)
    return render(request, 'collabPage.html',{'collab':collab, 'playlist':playlist})


import requests
from django.http import HttpResponse
from django.shortcuts import render

def get_spotify_token():
    import base64
    import time

    if not hasattr(get_spotify_token, "token") or time.time() > getattr(get_spotify_token, "expiry", 0):
        client_id = "172aabf79532439381a63f40f6aa175f"
        client_secret = "73cde19a90ae4582a2c1e066944e7276"
        creds = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
        res = requests.post(
            "https://accounts.spotify.com/api/token",
            headers={"Authorization": f"Basic {creds}", "Content-Type": "application/x-www-form-urlencoded"},
            data={"grant_type": "client_credentials"}
        )
        data = res.json()
        get_spotify_token.token = data["access_token"]
        get_spotify_token.expiry = time.time() + data["expires_in"]
    return get_spotify_token.token

def search_spotify(request, id):
    query = request.GET.get("q", "")
    if not query:
        return HttpResponse("")

    token = get_spotify_token()
    res = requests.get(
        "https://api.spotify.com/v1/search",
        headers={"Authorization": f"Bearer {token}"},
        params={"q": query, "type": "track", "limit": 8},
    )
    data = res.json()["tracks"]["items"]
    return render(request, "search.html", {"tracks": data, "id":id})
@login_required(login_url='loginuser')
def add_track(request, id):
    if request.method == "POST":
        spotify_id = request.POST.get("spotify_id")
        song = Song()
        if len(Song.objects.filter(spotify_id=spotify_id)) == 0:
            song.artist = request.POST.get("artist")
            song.spotify_id = spotify_id
            song.name = request.POST.get("name")
            song.duration = request.POST.get("duration")
            song.imagelink = request.POST.get("imagelink")
            song.link = request.POST.get("link")
            song.save()
        else:
            song = Song.objects.filter(spotify_id=spotify_id).first()
        contains = Contains()
        contains.idsong = song
        contains.idplaylist = Collab.objects.get(idcollab=id).idplaylist
        contains.iduser = User.objects.filter(idauth=request.user).first()
        contains.save()
        return redirect('collabPage', id=id)

def remove_track(request, id, idsong):
    if request.method == "POST":
        playlist = Collab.objects.get(idcollab=id).idplaylist
        song = Song.objects.get(idsong=idsong)
        contains = Contains.objects.filter(idsong=song, idplaylist=playlist).first()
        contains.delete()
        return redirect('collabPage', id=id)

def logoutuser(request):
    logout(request)
    return redirect('loginuser')

def trending(request):
    cr = Created.objects.filter(trending=1)
    res = []
    for i in cr:
        songs = []
        for j in Contains.objects.filter(idplaylist=i.idplaylist):
            songs.append(j.idsong)
        import random
        if songs:
            photo = random.choice(songs).imagelink
        else:
            photo = ''
        user = User.objects.filter(idauth=request.user).first()
        liked = Liked.objects.filter(created=i,iduser=user).count() > 0
        rated = Rated.objects.filter(created=i,iduser=user).count() > 0
        ratings=[]
        r = Rated.objects.filter(created=i)
        for rr in r:
            ratings.append(rr.rating)
        rating='N/A'
        if len(ratings)>0:
            rating = sum(ratings) / len(ratings)
            rating = round(rating, 2)
        res.append({'playlist':i.idplaylist, 'likes': Liked.objects.filter(created=i).count(), 'user':i.iduser, 'photo':photo, 'liked':liked, 'rated':rated, 'rating':rating })
    return render(request, 'trending.html', {'res': res})

def like(request, id):
    if request.method == "POST":
        created=Created.objects.filter(idplaylist=id).first()
        user = User.objects.filter(idauth=request.user).first()
        liked = Liked.objects.filter(created=created,iduser=user).first()
        if liked is None:
            liked = Liked()
            liked.created = created
            liked.iduser = user
            liked.save()
        else:
            liked.delete()
    return redirect('trending')

def rate(request, id):
    if request.method == "POST":
        rating_string = request.POST.get('rating', '')
        if rating_string=='':
            return render(request, 'rate.html', {'id': id})
        rating_value = int(rating_string)
        created=Created.objects.filter(idplaylist=id).first()
        user = User.objects.filter(idauth=request.user).first()
        rated = Rated.objects.filter(created=created,iduser=user).first()
        if rated is not None:
            rated.delete()
        rated = Rated()
        rated.created = created
        rated.iduser = user
        rated.rating = rating_value
        rated.save()
        return redirect('trending')
    created = Created.objects.filter(idplaylist=id).first()
    user = User.objects.filter(idauth=request.user).first()
    rated = Rated.objects.filter(created=created, iduser=user).first()
    r = False
    rating=0
    if rated is not None:
        r=True
        rating=rated.rating
    return render(request, 'rate.html', {'id':id, 'rated':r, 'rating':rating})

def cancelrate(request, id):
    if request.method == "POST":
        created=Created.objects.filter(idplaylist=id).first()
        user = User.objects.filter(idauth=request.user).first()
        rated = Rated.objects.filter(created=created,iduser=user).first()
        if rated is not None:
            rated.delete()
    return redirect('trending')