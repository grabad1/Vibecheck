from django.contrib.auth import login, authenticate
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

def collabPage(request):
    return render(request, 'collabPage.html')

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
    return render(request, 'signup.html')

def successful_password_change(request):
    return render(request, 'successful_password_change.html')

def successful_payment(request):
    return render(request, 'successful_payment.html')

def trending(request):
    return render(request, 'trending.html')

def user(request):
    user = request.user
    collabs = Collab.objects.filter(iduser=1)
    return render(request, 'user.html', context={'collabs':collabs, 'username': user.username})