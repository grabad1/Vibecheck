from django.shortcuts import render

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

def login(request):
    return render(request, 'login.html')

def moderator(request):
    return render(request, 'moderator.html')

def passwordChange(request):
    return render(request, 'passwordChange.html')

def playlist(request):
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
    return render(request, 'user.html')