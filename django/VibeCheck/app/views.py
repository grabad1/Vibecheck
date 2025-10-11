from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.models import User as djangoUser
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import *


def index(request):
    if request.user.is_authenticated:
        user = User.objects.get(idauth=request.user)
        user_type = user.type
        if user_type in ('regular', 'premium'):
            return redirect('user')
        elif user_type == 'moderator':
            return redirect('moderator')
        elif user_type == 'admin':
            return redirect('admin')
    return render(request, 'index.html')


def checkout(request):
    return render(request, 'checkout.html')


def admin(request):
    return render(request, 'admin.html')


def createCollab(request, collabid):
    user = User.objects.get(idauth=request.user)
    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'friends':
            friend_id = request.POST.get('friend_id')
            if Requestcollab.objects.filter(idcollab=Collab.objects.get(idcollab=collabid)) \
                    .filter(iduserrecieve=User.objects.get(idauth=friend_id)).exists():
                return render(request, 'createCollab.html', createCollab_context(user, collabid))
            req = Requestcollab.objects.create(
                idusersend=user,
                iduserrecieve=User.objects.get(idauth=friend_id),
                idcollab=Collab.objects.get(idcollab=collabid)
            )
        elif form_type == 'exit':
            Requestcollab.objects.filter(idcollab=collabid).delete()
            Participated.objects.filter(idcollab=collabid).delete()
            collab = Collab.objects.get(idcollab=collabid)
            play = Playlist.objects.get(idplaylist=collab.idplaylist.idplaylist)
            collab.delete()
            play.delete()
            return redirect('user')

        elif form_type == 'start':
            name = request.POST.get('name', '').strip()
            if Participated.objects.filter(idcollab=collabid).count() == 1:
                mess = "Other people have to join"
                context = createCollab_context(user, collabid, {'mess': mess})
                return render(request, 'createCollab.html', context)
            elif name == '':
                mess = "You have to enter name for the collab!"
                context = createCollab_context(user, collabid, {'mess': mess})
                return render(request, 'createCollab.html', context)
            collab = Collab.objects.get(idcollab=collabid)
            pl = collab.idplaylist
            pl.name = name
            pl.save()
            collab.status = "active"
            collab.name = name
            collab.save()
            return redirect('collabPage', collabid)

    return render(request, 'createCollab.html', createCollab_context(user, collabid))


def createCollab_context(user, collabid, extra=None):
    participants = Participated.objects.filter(idcollab=collabid)
    friendlist = get_friends_list(user)
    friends = []
    for friend in friendlist:
        if Requestcollab.objects.filter(iduserrecieve=User.objects.get(idauth=friend)).filter(
                idcollab=collabid).exists():
            friends.append({
                'friend': friend,
                'sent': True
            })
        else:
            friends.append({
                'friend': friend,
                'sent': False
            })
    context = {
        'username': user.idauth.username,
        'friends': friends,
        'participants': participants
    }
    if extra:
        context.update(extra)
    return context


def loginuser(request):
    if request.user.is_authenticated:
        return redirect('user')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        remember_me = request.POST.get('remember-me')
        try:
            user = djangoUser.objects.get(username=username)
        except:
            mess = "User does not exist"
            context = {'mess': mess}
            return render(request, 'login.html', context)
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            if remember_me == 'on':
                request.session.set_expiry(60 * 60 * 24 * 30)
            else:
                request.session.set_expiry(0)
            user_obj = User.objects.get(idauth=user.id)
            user_type = user_obj.type
            if user_type in ('regular', 'premium'):
                return redirect('user')
            elif user_type == 'moderator':
                return redirect('moderator')
            elif user_type == 'admin':
                return redirect('admin')
        else:
            mess = "Incorrect password"
            context = {'mess': mess}
            return render(request, 'login.html', context)
    else:
        return render(request, 'login.html')


def moderator(request):
    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        if form_type == 'createPlaylist':
            name = request.POST.get('name', '').strip()
            if name == '':
                mess = "You have to enter name for the collab!"
                return render(request, 'moderator.html', {'mess': mess, 'active_section': 'createPlaylist'})
            play = Playlist.objects.create(name=name)
            created = Created.objects.create(
                idplaylist=play,
                iduser=User.objects.get(idauth=request.user),
                trending=0
            )
            collab = Collab.objects.create(
                name=name,
                iduser=User.objects.get(idauth=request.user),
                idplaylist=play,
                status='active'
            )
            return redirect('makePlaylist', collab.idcollab)
        elif form_type == 'trending' or form_type == 'myPlaylists':
            created = request.POST.get('created')
            create = Created.objects.get(id=created)
            action = request.POST.get('action')
            if action == 'edit':
                collab = Collab.objects.get(idplaylist=create.idplaylist).idcollab
                return redirect('collabPage', collab)
            elif action == 'remove':
                create.trending = 0
                create.save()
                if form_type == 'trending':
                    return redirect(f'/moderator/?section=trending')
                else:
                    return redirect(f'/moderator/?section=myPlaylists')
        if form_type == 'myPlaylists':
            created = request.POST.get('created')
            create = Created.objects.get(id=created)
            action = request.POST.get('action')
            if action == 'upload':
                create.trending = 1
                create.save()
                return redirect(f'/moderator/?section=myPlaylists')

    user = User.objects.get(idauth=request.user)
    createdlist = Created.objects.filter(iduser=user.iduser)
    num = createdlist.count()
    total_rating_sum = 0
    cnt = 0
    activities = []
    playlists = []
    trending = []
    for c in createdlist:
        ratings = []
        rated = Rated.objects.filter(created=c)
        for rr in rated:
            ratings.append(rr.rating)
            activities.append(rr)
        rating = 'N/A'
        if len(ratings) > 0:
            total_rating_sum += sum(ratings)
            cnt += len(ratings)
            rating = round(total_rating_sum / cnt, 2)
        if c.trending == 1:
            trending.append({
                'created': c,
                'rate': rating
            })
        playlists.append({
            'created': c,
            'rate': rating
        })

    if cnt == 0:
        avg = 0
    else:
        avg = total_rating_sum / cnt

    section = request.GET.get('section', 'home')
    context = {
        'numPlaylists': num,
        'avg': avg,
        'activities': sorted(activities, key=lambda r: r.time, reverse=True),
        'playlists': playlists,
        'trending': trending,
        'active_section': section
    }
    return render(request, 'moderator.html', context)


def makePlaylist(request, id):
    collab = Collab.objects.get(idcollab=id)
    pesme = Contains.objects.filter(idplaylist=collab.idplaylist)
    playlist = []
    for i in pesme:
        playlist.append({
            'song': i.idsong,
            'user': i.iduser.idauth,
        })
    context = {
        'collab': collab,
        'playlist': playlist,
        'status': False
    }
    return render(request, 'collabPage.html', context)


def passwordChange(request):
    if request.method == 'POST':
        old = request.POST['old']
        new = request.POST['new']
        confirm = request.POST['confirm']
        username = request.user.username
        user = authenticate(username=username, password=old)
        if user is None:
            mess = "Invalid password"
            context = {'mess': mess}
            return render(request, 'passwordChange.html', context)
        elif confirm != new:
            mess = "New password and confirmation must be the same."
            context = {'mess': mess}
            return render(request, 'passwordChange.html', context)
        else:
            user.set_password(new)
            user.save()
            update_session_auth_hash(request, user)
            return redirect('successful_password_change')
    else:
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


def userpage(request):
    user = User.objects.get(idauth=request.user)
    col = Collab.objects.filter(status="created").filter(iduser=user.iduser).first()
    if Collab.objects.filter(status="created").filter(iduser=user.iduser).exists():
        return redirect('createCollab', col.idcollab)
    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'friend_request':
            username = request.POST['username']
            try:
                userr = djangoUser.objects.get(username=username)
            except:
                mess = "User does not exist."
                context = user_context(User.objects.get(idauth=request.user), {'mess': mess})
                return render(request, 'user.html', context)

            receiver = User.objects.get(idauth=userr)
            sender = User.objects.get(idauth=request.user)

            if Requestfriendship.objects.filter(idusersend=receiver) \
                    .filter(iduserrecieve=sender).exists() \
                    or Requestfriendship.objects.filter(idusersend=sender) \
                    .filter(iduserrecieve=receiver).exists():
                mess = "Request already sent"
                context = user_context(sender, {'mess': mess})
                return render(request, 'user.html', context)

            req = Requestfriendship.objects.create(
                idusersend=sender,
                iduserrecieve=receiver
            )

        elif form_type == 'mailbox':
            mail_id = request.POST.get('mail_id')
            action = request.POST.get('action')
            type = request.POST.get('mail_type')
            if action == 'accept' and type == 'm':
                fr = Friendship.objects.create(
                    request=Requestfriendship.objects.get(idrf=mail_id)
                )

            elif action == 'deny' and type == 'm':
                req = Requestfriendship.objects.get(idrf=mail_id)
                req.delete()

            elif action == 'accept' and type == 'c':
                req = Requestcollab.objects.get(idrc=mail_id)
                fr = Participated.objects.create(
                    iduser=User.objects.get(idauth=request.user),
                    idcollab=req.idcollab
                )
                req.delete()

            elif action == 'deny' and type == 'c':
                req = Requestcollab.objects.filter(idrc=mail_id)
                req.delete()

        elif form_type == 'collab':
            play = Playlist.objects.create()
            coll = Collab.objects.create(
                iduser=User.objects.get(idauth=request.user),
                idplaylist=play,
                status="created"
            )
            par = Participated.objects.create(
                idcollab=coll,
                iduser=User.objects.get(idauth=request.user)
            )
            return redirect('createCollab', coll.idcollab)

    return render(request, 'user.html', context=user_context(user))


def user_context(user, extra=None):
    participated = Participated.objects.filter(iduser=user)
    collabs = []
    for part in participated:
        if part.idcollab.idplaylist.name != "":
            collabs.append(part.idcollab)
    friends = get_friends_list(user)
    messages = get_messages_list(user)
    context = {'collabs': collabs,
               'username': user.idauth.username,
               'friends': friends,
               'messages': sorted(messages, key=lambda d: d['message'].time, reverse=True)}
    if extra:
        context.update(extra)
    return context


def get_friends_list(user):
    friends = []
    friendsid = []

    friends1 = Requestfriendship.objects.filter(idusersend=user)
    for friend in friends1:
        idauth = friend.iduserrecieve.idauth
        friendsid.append(friend.idrf)
        friends.append(idauth)

    friends2 = Requestfriendship.objects.filter(iduserrecieve=user)
    for friend in friends2:
        idauth = friend.idusersend.idauth
        friendsid.append(friend.idrf)
        friends.append(idauth)

    friendlist = []
    for id in friendsid:
        if Friendship.objects.filter(request=id).exists():
            friendlist.append(friends[friendsid.index(id)])
    return friendlist


def get_messages_list(user):
    messages = Requestfriendship.objects.filter(iduserrecieve=user)
    collabs = Requestcollab.objects.filter(iduserrecieve=user)
    filtered = []

    for message in messages:
        if not Friendship.objects.filter(request=message).exists():
            filtered.append({
                'message': message,
                'type': 'm'
            })
    for collab in collabs:
        filtered.append({
            'message': collab,
            'type': 'c'
        })
    return filtered


def logoutuser(request):
    logout(request)
    return redirect('index')


@login_required(login_url='loginuser')
def collabPage(request, id):
    collab = Collab.objects.get(idcollab=id)
    pesme = Contains.objects.filter(idplaylist=collab.idplaylist)
    users = []
    for j in Participated.objects.filter(idcollab=collab):
        users.append(j.iduser)
    playlist = []
    for i in pesme:
        playlist.append({
            'song': i.idsong,
            'user': i.iduser.idauth,
        })
        print(i.idsong.name)
    return render(request, 'collabPage.html', {'collab': collab, 'playlist': playlist, 'users': users, 'status': True, 'count':len(playlist)})


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
    return render(request, "search.html", {"tracks": data, "id": id})


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
        liked = Liked.objects.filter(created=i, iduser=user).count() > 0
        rated = Rated.objects.filter(created=i, iduser=user).count() > 0
        ratings = []
        r = Rated.objects.filter(created=i)
        for rr in r:
            ratings.append(rr.rating)
        rating = 'N/A'
        if len(ratings) > 0:
            rating = sum(ratings) / len(ratings)
            rating = round(rating, 2)
        res.append({'playlist': i.idplaylist, 'likes': Liked.objects.filter(created=i).count(), 'user': i.iduser,
                    'photo': photo, 'liked': liked, 'rated': rated, 'rating': rating})
    return render(request, 'trending.html', {'res': res})


def like(request, id):
    if request.method == "POST":
        created = Created.objects.filter(idplaylist=id).first()
        user = User.objects.filter(idauth=request.user).first()
        liked = Liked.objects.filter(created=created, iduser=user).first()
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
        if rating_string == '':
            return render(request, 'rate.html', {'id': id})
        rating_value = int(rating_string)
        created = Created.objects.filter(idplaylist=id).first()
        user = User.objects.filter(idauth=request.user).first()
        rated = Rated.objects.filter(created=created, iduser=user).first()
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
    rating = 0
    if rated is not None:
        r = True
        rating = rated.rating
    return render(request, 'rate.html', {'id': id, 'rated': r, 'rating': rating})


def cancelrate(request, id):
    if request.method == "POST":
        created = Created.objects.filter(idplaylist=id).first()
        user = User.objects.filter(idauth=request.user).first()
        rated = Rated.objects.filter(created=created, iduser=user).first()
        if rated is not None:
            rated.delete()
    return redirect('trending')
