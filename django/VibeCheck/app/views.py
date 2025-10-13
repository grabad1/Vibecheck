from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.models import User as djangoUser
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
import requests
from django.http import HttpResponse, JsonResponse
from datetime import datetime, timedelta
from django.contrib import messages
from .models import *


def index(request):
    if request.user.is_authenticated:
        user = User.objects.get(idauth=request.user)
        user_type = user.type
        purchases = Purchased.objects.filter(iduser=user)
        p = None
        if purchases.exists():
            p = purchases.first()
        if user_type == 'premium' and datetime.now().date() - p.date.date() > timedelta(days=30):
            user.type = 'regular'
            user.save()
        if user_type in ('regular', 'premium'):
            return redirect('user')
        elif user_type == 'moderator':
            return redirect('moderator')
        elif user_type == 'admin':
            return redirect('admin')
    return render(request, 'index.html')


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
            user_obj = User.objects.get(idauth=user)
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


def successful_password_change(request):
    return render(request, 'successful_password_change.html')


def signup(request):
    if request.user.is_authenticated:
        return redirect('user')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        user_type = 'regular'

        if djangoUser.objects.filter(username=username).exists():
            mess = "Korisnik već postoji"
            return render(request, 'signup.html', {'mess': mess})

        django_user = djangoUser.objects.create_user(
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


def checkout(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            user = User.objects.get(idauth=request.user.id)
            Purchased.objects.create(iduser=user, date=datetime.now())
            user.type = "premium"
            user.save()
            return redirect('successful_payment')
        else:
            context = {"mess": "Error: Purchase failed!"}
            return render('checkout', context)
    return render(request, 'checkout.html')


def admin(request):
    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        if form_type == 'trending':
            delete = request.POST.get('fordelete')
            plejlista = Playlist.objects.get(idplaylist=delete)
            created = Created.objects.get(idplaylist=plejlista)
            plejlista.delete()
            return redirect(f'/adminpage/?section=trending')
        elif form_type == 'users':
            action = request.POST.get('action')
            if action == 'remove':
                delete = request.POST.get('userid')
                korisnik = User.objects.get(iduser=delete)
                korisnik.idauth.delete()
                korisnik.delete()
            elif action == 'promote':
                promote = request.POST.get('userid')
                korisnik = User.objects.get(iduser=promote)
                korisnik.type = "moderator"
                korisnik.save()
            else:
                demote = request.POST.get('userid')
                korisnik = User.objects.get(iduser=demote)

                subscriptions = Purchased.objects.filter(iduser=demote)
                if subscriptions.exists():
                    subscription = subscriptions.last()
                    if datetime.now().date() - subscription.date.date() < timedelta(days=30):
                        korisnik.type = "premium"
                        korisnik.save()
                        return redirect(f'/adminpage/?section=users')
                korisnik.type = "regular"
                korisnik.save()
            return redirect(f'/adminpage/?section=users')
    dashboard = []
    all_purchases = []
    all_users = []
    trending_playlists = []
    liked = Liked.objects.all()
    purchased = Purchased.objects.all()
    rated = Rated.objects.all()
    requested_collab = Requestcollab.objects.all()
    requested_friendship = Requestfriendship.objects.all()
    auth_users = djangoUser.objects.all()

    tp = Created.objects.filter(trending=1)
    for p in tp:
        row = {
            'name': p.idplaylist.name,
            'author': p.iduser.idauth.username,
            'likes': Liked.objects.filter(created=p).count(),
            'score': None,
            'order': None,
            'id': p.idplaylist.idplaylist
        }

        rated = Rated.objects.filter(created=p)
        sum = 0
        count = 0
        avg = 0
        for r in rated:
            sum += r.rating
            count += 1
        if count == 0:
            avg = 0
        else:
            avg = sum / count
        row['score'] = avg
        trending_playlists.append(row)

    sorted_trending_playlists = sorted(trending_playlists, key=lambda k: k['score'])
    count = len(sorted_trending_playlists)
    for s in sorted_trending_playlists:
        s['order'] = count
        count -= 1

    users = User.objects.all()
    for user in users:
        row = {
            'id': user.iduser,
            'name': user.idauth.username,
            'email': user.idauth.email,
            'joined': user.idauth.date_joined.date(),
            'status': user.type
        }
        all_users.append(row)

    for l in liked:
        row = {
            'time': l.time,
            'activity': f"Liked a playlist by {l.created.iduser.idauth.username}",
            'user': l.iduser.idauth.username,
            'status': l.iduser.type,
            'details': f"Playlist name: {l.created.idplaylist.name}"
        }
        dashboard.append(row)
    for p in purchased:
        row = {
            'time': p.date,
            'activity': "Payment",
            'user': p.iduser.idauth.username,
            'status': p.iduser.type,
            'details': "VibeCheck Premium subscription"
        }
        purchase = {
            'id': p.idpur,
            'iduser': p.iduser.idauth.username,
            'time': p.date.date(),
        }
        if datetime.now().date() - p.date.date() < timedelta(days=30):
            purchase['state'] = 'active'
        else:
            purchase['state'] = 'inactive'
        dashboard.append(row)
        all_purchases.append(purchase)
    for r in rated:
        row = {
            'time': r.time,
            'activity': f"Rated a playlist by {r.created.iduser.idauth.username}",
            'user': r.iduser.idauth.username,
            'status': r.iduser.type,
            'details': f"Playlist name: {r.created.idplaylist.name}, Rating: {r.rating}"
        }
        dashboard.append(row)
    for rc in requested_collab:
        row = {
            'time': rc.time,
            'activity': "Requested a collab with another user",
            'user': rc.idusersend.idauth.username,
            'status': rc.idusersend.type,
            'details': f"Other user: {rc.iduserrecieve.idauth.username}"
        }
        dashboard.append(row)
    for rf in requested_friendship:
        row = {
            'time': rf.time,
            'activity': "Sent a friend request",
            'user': rf.idusersend.idauth.username,
            'status': rf.idusersend.type,
            'details': f"Other user: {rf.iduserrecieve.idauth.username}"
        }
        dashboard.append(row)
    for au in auth_users:
        if not User.objects.filter(idauth=au):
            continue
        row = {
            'time': au.date_joined,
            'activity': "User authorized",
            'user': au.username,
            'status': User.objects.get(idauth=au).type,
            'details': "Succesful account creation"
        }
        dashboard.append(row)
    dashboard_sorted = sorted(dashboard, key=lambda k: k['time'], reverse=True)
    all_purchases_sorted = sorted(all_purchases, key=lambda k: k['id'], reverse=True)

    users_count = User.objects.count()
    playlist_count = Playlist.objects.count()
    moderators_count = User.objects.filter(type='moderator').count()
    active_subscriptions_count = User.objects.filter(type='premium').count()

    section = request.GET.get('section', 'home')
    context = {
        "dashboard": dashboard_sorted,
        "playlist_count": playlist_count,
        "moderators_count": moderators_count,
        "active_subscriptions_count": active_subscriptions_count,
        "users_count": users_count,
        "all_purchases": all_purchases_sorted,
        "trending": sorted_trending_playlists,
        "users": all_users,
        'active_section': section
    }

    return render(request, 'admin.html', context)


def pricing(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            return redirect('checkout')
        else:
            return redirect('loginuser')
    return render(request, 'pricing.html')


def successful_payment(request):
    return render(request, 'successful_payment.html')


def createCollab(request, collabid):
    user = User.objects.get(idauth=request.user)
    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        if form_type == 'friends':
            sent_count = Requestcollab.objects.filter(
                idusersend=user,
                idcollab=collabid
            ).count()
            participants_count = Participated.objects.filter(idcollab=collabid).count()
            total_count = participants_count + sent_count
            if user.type == 'regular' and total_count >= 4:
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({
                        'ok': False,
                        'error': 'As a regular user, you can add a maximum of 3 people.'
                    })
                mess = "As a regular user, you can add a maximum of 3 people."
                context = createCollab_context(user, collabid, {'mess': mess})
                return render(request, 'createCollab.html', context)
            friend_id = request.POST.get('friend_id')
            friend = User.objects.get(idauth=friend_id)

            existing = Requestcollab.objects.filter(
                idcollab=collabid,
                iduserrecieve=friend
            ).exists()
            if not existing:
                req = Requestcollab.objects.create(
                    idusersend=user,
                    iduserrecieve=friend,
                    idcollab=Collab.objects.get(idcollab=collabid)
                )
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'ok': True})

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
        sent = Requestcollab.objects.filter(iduserrecieve=User.objects.get(idauth=friend)) \
            .filter(idcollab=collabid).exists()
        friends.append({
            'friend': friend,
            'sent': sent
        })
    context = {
        'username': user.idauth.username,
        'friends': friends,
        'participants': participants,
        'collabid': collabid
    }
    if extra:
        context.update(extra)
    return context


@login_required
def ajax_friends_collab(request, collabid):
    user = User.objects.get(idauth=request.user)
    collab = Collab.objects.get(idcollab=collabid)
    friendlist = get_friends_list(user)
    friends_data = []

    for friend in friendlist:
        friend_obj = User.objects.get(idauth=friend)
        if Participated.objects.filter(iduser=friend_obj) \
                .filter(idcollab=collabid).exists():
            continue

        sent = Requestcollab.objects.filter(
            iduserrecieve=friend_obj,
            idcollab=collab
        ).exists()

        friends_data.append({
            'friend_id': friend.id,
            'username': friend.username,
            'sent': sent
        })

    return JsonResponse(friends_data, safe=False)


def moderator(request):
    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        if form_type == 'createPlaylist':
            name = request.POST.get('name', '').strip()
            if name == '':
                mess = "You have to enter name for the playlist!"
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
                return redirect('makePlaylist', collab)
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


def userpage(request):
    user = User.objects.get(idauth=request.user)
    collabs = Collab.objects.filter(status="created").filter(iduser=user.iduser)
    col = collabs.first()
    if collabs.exists():
        return redirect('createCollab', col.idcollab)
    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'friend_request':
            username = request.POST['username']
            try:
                userr = djangoUser.objects.get(username=username)
            except:
                mess = "User does not exist."
                context = user_context(user, {'mess': mess})
                return render(request, 'user.html', context)

            receiver = User.objects.get(idauth=userr)
            if receiver.type == 'moderator' or receiver.type == 'admin':
                mess = "User does not exist."
                context = user_context(user, {'mess': mess})
                return render(request, 'user.html', context)

            sender = user

            if Requestfriendship.objects.filter(idusersend=receiver, iduserrecieve=sender).exists() \
                    or Requestfriendship.objects.filter(idusersend=sender, iduserrecieve=receiver).exists():
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
            mailbox(mail_id, action, type, user)

        elif form_type == 'collab':
            if user.type == "regular" and Collab.objects.filter(iduser=user).count() >= 5:
                mess = "As a regular user, you can have a maximum of 5 collabs"
                context = user_context(user, {'mess1': mess})
                return render(request, 'user.html', context)
            play = Playlist.objects.create()
            coll = Collab.objects.create(
                iduser=user,
                idplaylist=play,
                status="created"
            )
            par = Participated.objects.create(
                idcollab=coll,
                iduser=user
            )
            return redirect('createCollab', coll.idcollab)

    return render(request, 'user.html', context=user_context(user))


def user_context(user, extra=None):
    participated = Participated.objects.filter(iduser=user)
    collabs = []
    for part in participated:
        if part.idcollab.status != 'created':
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


def mailbox(mail_id, action, type, user):
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
            iduser=user,
            idcollab=req.idcollab
        )
        req.delete()

    elif action == 'deny' and type == 'c':
        req = Requestcollab.objects.filter(idrc=mail_id)
        req.delete()


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
    return render(request, 'collabPage.html',
                  {'collab': collab, 'playlist': playlist, 'users': users, 'status': True, 'count': len(playlist)})


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
    user = User.objects.get(idauth=request.user)
    pl = Collab.objects.get(idcollab=id).idplaylist
    num = Contains.objects.filter(iduser=user, idplaylist=pl).count()
    if user.type == 'regular' and num >= 10:
        messages.error(request, 'As a regular user, you can add a maximum of 10 songs.')
        return redirect('collabPage', id=id)
    if request.method == "POST":
        spotify_id = request.POST.get("spotify_id")
        song = Song()
        if Song.objects.filter(spotify_id=spotify_id).count() == 0:
            print("Nema vec")
            song.artist = request.POST.get("artist")
            song.spotify_id = spotify_id
            song.name = request.POST.get("name")

            dur = int(request.POST.get("duration"))
            song.duration = dur
            total_seconds = dur // 1000
            minutes = total_seconds // 60
            seconds = total_seconds % 60
            song.duration_string = f"{minutes}:{seconds:02d}"
            song.imagelink = request.POST.get("imagelink")
            song.link = request.POST.get("link")
            song.save()
        else:
            song = Song.objects.filter(spotify_id=spotify_id).first()
        if not Contains.objects.filter(idsong=song, idplaylist=pl).exists():
            contains = Contains()
            contains.idsong = song
            contains.idplaylist = pl
            contains.iduser = user
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
        if request.user.is_authenticated:
            user = User.objects.filter(idauth=request.user).first()
            liked = Liked.objects.filter(created=i, iduser=user).count() > 0
            rated = Rated.objects.filter(created=i, iduser=user).count() > 0
        else:
            liked = False
            rated = False
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


@login_required(login_url='loginuser')
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


@login_required(login_url='loginuser')
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


def ajax_get_friends(request):
    user = User.objects.get(idauth=request.user)
    friends = get_friends_list(user)
    html = ""
    for friend in friends:
        html += f"{friend.username}<br>"
    return HttpResponse(html)


def ajax_get_collabs(request):
    user = User.objects.get(idauth=request.user)
    participated = Participated.objects.filter(iduser=user)
    html = ""
    for p in participated:
        collab = p.idcollab
        if collab.status != 'created':
            html += f"<a href='/collabPage/{collab.idcollab}' class='playlistlink'>{collab.name}</a><br>"
    return HttpResponse(html)


def ajax_get_messages(request):
    user = User.objects.get(idauth=request.user)
    messages = get_messages_list(user)
    messages = sorted(messages, key=lambda d: d['message'].time, reverse=True)
    html = ""
    for mail in messages:
        if mail['type'] == 'm':
            html += f"""
            <form method='post'>
                <input type='hidden' name='form_type' value='mailbox'>
                <input type='hidden' name='mail_type' value='m'>
                <input type='hidden' name='mail_id' value='{mail["message"].idrf}'>
                {mail["message"].idusersend.idauth.username} sent you a friend request.<br>
                <button type='submit' name='action' value='accept' class='btn new_request'>Accept</button>
                <button type='submit' name='action' value='deny' class='btn new_request'>Deny</button>
            </form>
            <hr>
            """
        elif mail['type'] == 'c':
            html += f"""
            <form method='post'>
                <input type='hidden' name='form_type' value='mailbox'>
                <input type='hidden' name='mail_type' value='c'>
                <input type='hidden' name='mail_id' value='{mail["message"].idrc}'>
                {mail["message"].idusersend.idauth.username} invited you to join a collab.<br>
                <button type='submit' name='action' value='accept' class='btn new_request'>Accept</button>
                <button type='submit' name='action' value='deny' class='btn new_request'>Deny</button>
            </form>
            <hr>
            """
    return HttpResponse(html)


@login_required
def ajax_get_participants(request, collabid):
    participants = Participated.objects.filter(idcollab_id=collabid)
    html = ""
    for p in participants:
        html += f"{p.iduser.idauth.username}<br>"
    return HttpResponse(html)


@login_required
def ajax_mailbox_action(request):
    if request.method == "POST":
        form_type = request.POST.get("form_type")
        mail_type = request.POST.get("mail_type")
        mail_id = request.POST.get("mail_id")
        action = request.POST.get("action")

        if form_type == "mailbox":
            user = User.objects.get(idauth=request.user)
            if mail_type == "m":
                req = Requestfriendship.objects.get(idrf=mail_id)
                if action == "accept":
                    friendship = Friendship.objects.create(request=req)
                else:
                    req.delete()
            elif mail_type == "c":
                req = Requestcollab.objects.get(idrc=mail_id)
                if action == "accept":
                    participated = Participated.objects.create(iduser=user, idcollab=req.idcollab)
                req.delete()
            return JsonResponse({"ok": True})
    return JsonResponse({"ok": False}, status=400)
