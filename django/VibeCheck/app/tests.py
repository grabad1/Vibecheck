import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import TestCase, Client
from selenium import webdriver
from selenium.webdriver.common.by import By
from django.urls import reverse
import json
from django.contrib.auth.models import User as djangoUser
from .models import *


def create_user(username='user', password='123', email='user@gmail.com', utype='regular'):
    auth = djangoUser.objects.create_user(username=username, email=email, password=password)
    u = User.objects.create(idauth=auth, type=utype)
    return u


class LoginTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = create_user('user', '123')

    def test_loginuser_get(self):
        res = self.client.get(reverse('loginuser'))
        self.assertEqual(res.status_code, 200)

    def test_loginuser_post_wrong_user(self):
        res = self.client.post(reverse('loginuser'), {'username': 'x', 'password': 'x'})
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "User does not exist")

    def test_loginuser_post_wrong_password(self):
        res = self.client.post(reverse('loginuser'), {'username': 'user', 'password': 'bad'})
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "Incorrect password")

    def test_loginuser_post_success(self):
        res = self.client.post(reverse('loginuser'), {'username': 'user', 'password': '123'})
        self.assertIn(res.status_code, (200, 302))

    def test_logoutuser(self):
        self.client.login(username='user', password='123')
        res = self.client.get(reverse('logoutuser'), follow=True)
        self.assertIn(res.status_code, (200, 302))


class AdminTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = create_user('admin', '123', utype='admin')

        p = Playlist.objects.create(name='p1')
        self.moderator = create_user('moderator', '123')
        self.user = create_user('user', '123')
        created = Created.objects.create(idplaylist=p, iduser=self.moderator, trending=1)

    def test_admin_get(self):
        self.client.login(username='admin', password='123')
        res = self.client.get(reverse('admin'))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'admin.html')

    def test_admin_post_trending_delete(self):
        self.client.login(username='admin', password='123')
        p = Playlist.objects.create(name='p2')
        created = Created.objects.create(idplaylist=p, iduser=self.moderator, trending=1)
        res = self.client.post(reverse('admin'), {'form_type': 'trending', 'fordelete': p.idplaylist})
        self.assertIn(res.status_code, (200, 302))

    def test_admin_promote(self):
        self.client.login(username='admin', password='123')
        res = self.client.post(reverse('admin'),
                               {'form_type': 'users', 'action': 'promote', 'userid': self.user.iduser})
        self.assertIn(res.status_code, (200, 302))
        u = User.objects.get(iduser=self.user.iduser)
        self.assertEqual(u.type, 'moderator')

    def test_admin_demote(self):
        res = self.client.post(reverse('admin'),
                               {'form_type': 'users', 'action': 'demote', 'userid': self.moderator.iduser})
        self.assertIn(res.status_code, (200, 302))
        u = User.objects.get(iduser=self.user.iduser)
        self.assertEqual(u.type, 'regular')

    def test_admin_remove(self):
        res = self.client.post(reverse('admin'), {'form_type': 'users', 'action': 'remove', 'userid': self.user.iduser})
        self.assertIn(res.status_code, (200, 302))


class SignupPasswordTests(TestCase):
    def setUp(self):
        self.client = Client()
        djangoUser.objects.filter(username='user').delete()

    def test_signup_get(self):
        res = self.client.get(reverse('signup'))
        self.assertEqual(res.status_code, 200)

    def test_signup_existing_user(self):
        djangoUser.objects.create_user(username='user', password='123')
        res = self.client.post(reverse('signup'), {'username': 'user', 'password': '123', 'email': 'user@gmail.com'})
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "Korisnik već postoji")

    def test_signup_success(self):
        res = self.client.post(reverse('signup'), {'username': 'user', 'password': '123', 'email': 'user@gmail.com'})
        self.assertIn(res.status_code, (200, 302))
        self.assertTrue(djangoUser.objects.filter(username='user').exists())
        self.assertTrue(User.objects.filter(idauth__username='user').exists())

    def test_password_change_wrong_old(self):
        user = create_user('user', '123')
        self.client.login(username='user', password='123')
        res = self.client.post(reverse('passwordChange'), {'old': 'bad', 'new': 'n', 'confirm': 'n'})
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "Invalid password")

    def test_password_change_mismatch(self):
        user = create_user('user', '123')
        self.client.login(username='user', password='123')
        res = self.client.post(reverse('passwordChange'), {'old': '123', 'new': 'n1', 'confirm': 'n2'})
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "New password and confirmation must be the same.")

    def test_password_change_success(self):
        user = create_user('user', '123')
        self.client.login(username='user', password='123')
        res = self.client.post(reverse('passwordChange'), {'old': '123', 'new': 'n1', 'confirm': 'n1'}, follow=True)
        self.assertIn(res.status_code, (200, 302))
        self.client.logout()
        logged = self.client.login(username='user', password='n1')
        self.assertTrue(logged)


class TracksTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = create_user('user', '123')
        self.client.login(username='user', password='123')
        pl = Playlist.objects.create(name='Plejlista')
        coll = Collab.objects.create(name='Plejlista', iduser=self.user, idplaylist=pl, status='created')

    def test_add_track(self):
        coll = Collab.objects.first()
        post = {
            'spotify_id': 'id1',
            'artist': 'Artist',
            'name': 'Song',
            'duration': '1800',
            'link': 'link'
        }
        res = self.client.post(reverse('add_track', args=[coll.idcollab]), post)
        self.assertIn(res.status_code, (200, 302))
        self.assertTrue(Song.objects.filter(spotify_id='id1').exists())
        song = Song.objects.get(spotify_id='id1')
        self.assertTrue(Contains.objects.filter(idsong=song, idplaylist=coll.idplaylist).exists())
        self.assertIn('collabPage', res.url)
        res = self.client.post(reverse('collabPage', args=[coll.idcollab]))
        self.assertContains(res, 'Song', html=True)

    def test_remove_track(self):
        coll = Collab.objects.first()
        song = Song.objects.create(name='Song', spotify_id='id1', artist='Artist', duration=1800, link='link')
        Contains.objects.create(idsong=song, idplaylist=coll.idplaylist, iduser=self.user)
        res = self.client.post(reverse('remove_track', args=[coll.idcollab, song.idsong]))
        self.assertIn(res.status_code, (200, 302))
        self.assertFalse(Contains.objects.filter(idsong=song, idplaylist=coll.idplaylist).exists())
        res = self.client.post(reverse('collabPage', args=[coll.idcollab]))
        self.assertNotContains(res, 'Song', html=True)


class TrendingTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = create_user('user', '123')
        self.client.login(username='user', password='123')
        p = Playlist.objects.create(name='Plejlista')
        created = Created.objects.create(idplaylist=p, iduser=self.user, trending=1)

    def test_trending_get(self):
        res = self.client.get(reverse('trending'))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'Plejlista', html=True)

    def test_like(self):
        created = Created.objects.first()
        res = self.client.post(reverse('like', args=[created.idplaylist.idplaylist]))
        self.assertIn(res.status_code, (200, 302))
        self.assertTrue(Liked.objects.filter(created=created).exists())

    def test_rate(self):
        created = Created.objects.first()
        res = self.client.get(reverse('rate', args=[created.idplaylist.idplaylist]))
        self.assertEqual(res.status_code, 200)
        res = self.client.post(reverse('rate', args=[created.idplaylist.idplaylist]), {'rating': '5'})
        self.assertIn(res.status_code, (200, 302))
        self.assertTrue(Rated.objects.filter(created=created).exists())

    def test_cancelrate(self):
        created = Created.objects.first()
        Rated.objects.create(created=created, iduser=self.user, rating=3)
        res = self.client.post(reverse('cancelrate', args=[created.idplaylist.idplaylist]))
        self.assertIn(res.status_code, (200, 302))
        self.assertFalse(Rated.objects.filter(created=created).exists())

class ModeratorTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.moderator = create_user('moderator', '123', utype='moderator')

        p = Playlist.objects.create(name='Plejlista1')
        c = Collab.objects.create(iduser=self.moderator, idplaylist=p)
        self.created = Created.objects.create(idplaylist=p, iduser=self.moderator, trending=1)
        p2 = Playlist.objects.create(name='Plejlista2')
        c = Collab.objects.create(iduser=self.moderator, idplaylist=p2)
        self.created2 = Created.objects.create(idplaylist=p2, iduser=self.moderator, trending=0)

    def test_moderator_get(self):
        self.client.login(username='moderator', password='123')
        res = self.client.get(reverse('moderator'))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'moderator.html')

    def test_moderator_post_trending_delete(self):
        self.client.login(username='moderator', password='123')
        res = self.client.post(reverse('moderator'),
                               {'form_type': 'myPlaylists', 'action': 'remove', 'created': self.created.id})
        self.assertIn(res.status_code, (200, 302))
        c = Created.objects.get(id=self.created.id)
        self.assertEqual(c.trending, 0)

    def test_moderator_post_trending_upload(self):
        self.client.login(username='moderator', password='123')
        res = self.client.post(reverse('moderator'),
                               {'form_type': 'myPlaylists', 'action': 'upload', 'created': self.created2.id})
        self.assertIn(res.status_code, (200, 302))
        c = Created.objects.get(id=self.created.id)
        self.assertEqual(c.trending, 1)

    def test_moderator_edit(self):
        self.client.login(username='moderator', password='123')
        res = self.client.post(reverse('moderator'),
                               {'form_type': 'myPlaylists', 'action': 'edit', 'created': self.created2.id})
        self.assertIn(res.status_code, (200, 302))
        self.assertIn('makePlaylist', res.url)

    def test_moderator_create(self):
        self.client.login(username='moderator', password='123')
        res = self.client.post(reverse('moderator'), {'form_type': 'createPlaylist', 'name': 'Plejlista'})
        self.assertIn(res.status_code, (200, 302))
        self.assertIn('makePlaylist', res.url)

class PremiumTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = create_user('user', '123')

    def test_pricing_get(self):
        res = self.client.get(reverse('pricing'))
        self.assertEqual(res.status_code, 200)

    def test_pricing_post_redirect_authenticated(self):
        self.client.login(username='user', password='123')
        res = self.client.post(reverse('pricing'))
        self.assertIn(res.status_code, (200, 302))

    def test_checkout_post_authenticated(self):
        self.client.login(username='user', password='123')
        res = self.client.post(reverse('checkout'))
        user = User.objects.get(idauth=self.user.idauth)
        self.assertEqual(user.type, 'premium')


class CollabTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = create_user('user', '123')
        self.client.login(username='user', password='123')

    def test_createCollab_get(self):
        pl = Playlist.objects.create(name='Plejlista')
        coll = Collab.objects.create(name='Collab', iduser=self.user, idplaylist=pl, status='created')
        p = Participated.objects.create(idcollab=coll, iduser=self.user)
        res = self.client.get(reverse('createCollab', args=[coll.idcollab]))
        self.assertEqual(res.status_code, 200)


class FunctionalTestCase(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.appUrl = self.live_server_url

    def tearDown(self):
        self.browser.close()

    def create_test_users(self):
        django_user1 = djangoUser.objects.create_user(username='dusan', password='123')
        user1 = User.objects.create(idauth=django_user1, type='regular')

        django_user2 = djangoUser.objects.create_user(username='masa', password='123')
        user2 = User.objects.create(idauth=django_user2, type='regular')

        django_user3 = djangoUser.objects.create_user(username='nikola', password='123')
        user3 = User.objects.create(idauth=django_user3, type='regular')

        return user1, user2, user3

    def login_user(self, username, password):
        self.browser.get(self.appUrl)

        login_btn = self.browser.find_element(By.CLASS_NAME, 'login-btn')
        login_btn.click()

        username_field = self.browser.find_element(By.NAME, 'username')
        username_field.send_keys(username)

        password_field = self.browser.find_element(By.NAME, 'password')
        password_field.send_keys(password)

        login_submit = self.browser.find_element(By.ID, 'login')
        login_submit.click()

        time.sleep(2)


class LoginAndPasswordFunctionalTestCase(FunctionalTestCase):

    def test_login_admin(self):
        django_user1 = djangoUser.objects.create_user(username='admin', password='123')
        user1 = User.objects.create(idauth=django_user1, type='admin')
        self.browser.get(self.appUrl)

        login_btn = self.browser.find_element(By.CLASS_NAME, 'login-btn')
        login_btn.click()

        username_field = self.browser.find_element(By.NAME, 'username')
        username_field.send_keys('admin')

        password_field = self.browser.find_element(By.NAME, 'password')
        password_field.send_keys('123')

        login_submit = self.browser.find_element(By.ID, 'login')
        login_submit.click()

        time.sleep(2)

        self.assertIn('Dashboard', self.browser.page_source)

    def test_login_moderator(self):
        django_user1 = djangoUser.objects.create_user(username='moderator', password='123')
        user1 = User.objects.create(idauth=django_user1, type='moderator')
        self.browser.get(self.appUrl)

        login_btn = self.browser.find_element(By.CLASS_NAME, 'login-btn')
        login_btn.click()

        username_field = self.browser.find_element(By.NAME, 'username')
        username_field.send_keys('moderator')

        password_field = self.browser.find_element(By.NAME, 'password')
        password_field.send_keys('123')

        login_submit = self.browser.find_element(By.ID, 'login')
        login_submit.click()

        time.sleep(2)

        self.assertIn('Dashboard', self.browser.page_source)

    def test_change_password(self):
        django_user = djangoUser.objects.create_user(username='testuser', password='oldpass')
        User.objects.create(idauth=django_user, type='regular')

        self.login_user('testuser', 'oldpass')

        dropdown = self.browser.find_element(By.CLASS_NAME, 'dropdown-toggle')
        dropdown.click()

        time.sleep(1)

        change_pass_link = self.browser.find_element(By.LINK_TEXT, 'Change password')
        change_pass_link.click()

        time.sleep(2)

        old_pass = self.browser.find_element(By.NAME, 'old')
        old_pass.send_keys('oldpass')

        new_pass = self.browser.find_element(By.NAME, 'new')
        new_pass.send_keys('newpass123')

        confirm_pass = self.browser.find_element(By.NAME, 'confirm')
        confirm_pass.send_keys('newpass123')

        submit_btn = self.browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        submit_btn.click()

        time.sleep(2)

        self.assertIn('successful', self.browser.current_url.lower())


class FriendshipFunctionalTestCase(FunctionalTestCase):

    def test_add_friend(self):
        user1, user2, _ = self.create_test_users()
        self.login_user('dusan', '123')
        add = self.browser.find_element(By.ID, 'addfr')
        add.click()
        time.sleep(5)
        inputname = self.browser.find_element(By.NAME, 'username')
        inputname.send_keys('masa')
        addfriend = self.browser.find_element(By.ID, 'addfriend')
        addfriend.click()

        time.sleep(2)

        self.assertEqual(Requestfriendship.objects.count(), 1)
        request = Requestfriendship.objects.first()
        self.assertEqual(request.idusersend, user1)
        self.assertEqual(request.iduserrecieve, user2)

    def test_accept_friend_request(self):
        user1, user2, _ = self.create_test_users()

        request = Requestfriendship.objects.create(
            idusersend=user1,
            iduserrecieve=user2
        )

        self.login_user('masa', '123')

        self.assertIn('dusan', self.browser.page_source)
        self.assertIn('friend request', self.browser.page_source)

        accept_btn = self.browser.find_element(By.CSS_SELECTOR, 'button[value="accept"]')
        accept_btn.click()

        time.sleep(3)

        self.assertEqual(Friendship.objects.count(), 1)

    def test_deny_friend_request(self):
        user1, user2, _ = self.create_test_users()

        request = Requestfriendship.objects.create(
            idusersend=user1,
            iduserrecieve=user2
        )

        self.login_user('masa', '123')

        self.assertIn('dusan', self.browser.page_source)
        self.assertIn('friend request', self.browser.page_source)

        deny_btn = self.browser.find_element(By.CSS_SELECTOR, 'button[value="deny"]')
        deny_btn.click()

        time.sleep(2)

        self.assertEqual(Requestfriendship.objects.count(), 0)
        self.assertEqual(Friendship.objects.count(), 0)


class ModeratorFunctionalTestCase(FunctionalTestCase):

    def test_moderator_create_playlist(self):
        django_user1 = djangoUser.objects.create_user(username='moderator', password='123')
        user1 = User.objects.create(idauth=django_user1, type='moderator')
        self.login_user('moderator', '123')
        link = self.browser.find_element(By.LINK_TEXT, 'Create Playlist')
        link.click()
        name = self.browser.find_element(By.NAME, 'name')
        name.send_keys("Car Mix")
        submit_btn = self.browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        submit_btn.click()
        time.sleep(2)
        self.assertIn('/makePlaylist', self.browser.current_url)

    def test_moderator_myplaylist_upload(self):
        django_user1 = djangoUser.objects.create_user(username='moderator', password='123')
        user = User.objects.create(idauth=django_user1, type='moderator')

        pl = Playlist.objects.create(name="Plejlista")
        Created.objects.create(
            iduser=user,
            idplaylist=pl
        )
        self.login_user('moderator', '123')

        link = self.browser.find_element(By.LINK_TEXT, 'My Playlists')
        link.click()
        time.sleep(5)
        submit_btn = self.browser.find_element(By.CSS_SELECTOR, 'button[value="upload"]')
        submit_btn.click()
        time.sleep(2)
        self.assertIn('Remove', self.browser.page_source)

    def test_moderator_remove_from_trending(self):
        django_user1 = djangoUser.objects.create_user(username='moderator', password='123')
        user = User.objects.create(idauth=django_user1, type='moderator')

        pl = Playlist.objects.create(name="Plejlista")
        Created.objects.create(
            iduser=user,
            idplaylist=pl,
            trending=1
        )
        self.login_user('moderator', '123')

        link = self.browser.find_element(By.LINK_TEXT, 'Edit Trending')
        link.click()
        time.sleep(5)
        submit_btn = self.browser.find_element(By.CSS_SELECTOR, 'button[value="remove"]')
        submit_btn.click()
        time.sleep(2)
        trending = Created.objects.filter(trending=1).count()
        self.assertEqual(trending, 0)


class CollabPageFunctionalTestCase(FunctionalTestCase):

    def test_search_song(self):
        user1, user2, _ = self.create_test_users()

        req = Requestfriendship.objects.create(idusersend=user1, iduserrecieve=user2)
        Friendship.objects.create(request=req)

        playlist = Playlist.objects.create(name='Plejlista')
        collab = Collab.objects.create(
            iduser=user1,
            idplaylist=playlist,
            status='active',
            name='Plejlista'
        )
        Participated.objects.create(iduser=user1, idcollab=collab)
        Participated.objects.create(iduser=user2, idcollab=collab)

        self.login_user('dusan', '123')

        self.browser.get(f'{self.appUrl}/collabPage/{collab.idcollab}')
        time.sleep(2)

        searchsong = self.browser.find_element(By.ID, 'search-input')
        searchsong.send_keys('Juznjaci')
        time.sleep(5)

        self.assertIn('Zdravko Čolić', self.browser.page_source)

    def test_add_song(self):
        user1, user2, _ = self.create_test_users()

        req = Requestfriendship.objects.create(idusersend=user1, iduserrecieve=user2)
        Friendship.objects.create(request=req)

        playlist = Playlist.objects.create(name='Plejlista')
        collab = Collab.objects.create(
            iduser=user1,
            idplaylist=playlist,
            status='active',
            name='Plejlista'
        )
        Participated.objects.create(iduser=user1, idcollab=collab)
        Participated.objects.create(iduser=user2, idcollab=collab)

        self.login_user('dusan', '123')

        self.browser.get(f'{self.appUrl}/collabPage/{collab.idcollab}')
        time.sleep(2)

        searchsong = self.browser.find_element(By.ID, 'search-input')
        searchsong.send_keys('Juznjaci')
        time.sleep(5)
        submit_btn = self.browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        submit_btn.click()
        time.sleep(5)


class PremiumFunctionalTestCase(FunctionalTestCase):

    def test_buy_premium_fail(self):
        user1, _, _ = self.create_test_users()
        self.login_user('dusan', '123')
        self.browser.get(f'{self.appUrl}/pricing/')
        start = self.browser.find_element(By.CLASS_NAME, 'start')
        self.browser.execute_script("arguments[0].scrollIntoView(true);", start)
        time.sleep(3)
        start.click()
        submit_btn = self.browser.find_element(By.CSS_SELECTOR, 'button[type="button"]')
        self.browser.execute_script("arguments[0].scrollIntoView(true);", submit_btn)
        time.sleep(3)
        submit_btn.click()
        time.sleep(5)
        self.assertIn('required', self.browser.page_source)


class AdminFunctionalTestCase(FunctionalTestCase):

    def test_admin_promote(self):
        django_user1 = djangoUser.objects.create_user(username='dusan', password='123')
        user = User.objects.create(idauth=django_user1, type='regular')
        django_user2 = djangoUser.objects.create_user(username='admin', password='123')
        user2 = User.objects.create(idauth=django_user2, type='admin')

        self.login_user('admin', '123')

        link = self.browser.find_element(By.LINK_TEXT, 'Users')
        link.click()
        time.sleep(5)
        submit_btn = self.browser.find_element(By.CSS_SELECTOR, 'button[value="promote"]')
        submit_btn.click()
        time.sleep(2)
        self.assertIn('Moderator', self.browser.page_source)

    def test_admin_demote(self):
        django_user1 = djangoUser.objects.create_user(username='moderator', password='123')
        user = User.objects.create(idauth=django_user1, type='moderator')
        django_user2 = djangoUser.objects.create_user(username='admin', password='123')
        user2 = User.objects.create(idauth=django_user2, type='admin')

        self.login_user('admin', '123')

        link = self.browser.find_element(By.LINK_TEXT, 'Users')
        link.click()
        time.sleep(5)
        submit_btn = self.browser.find_element(By.CSS_SELECTOR, 'button[value="demote"]')
        submit_btn.click()
        time.sleep(2)
        self.assertIn('Registered', self.browser.page_source)

    def test_admin_remove_user(self):
        django_user1 = djangoUser.objects.create_user(username='dusan', password='123')
        user = User.objects.create(idauth=django_user1, type='regular')
        django_user2 = djangoUser.objects.create_user(username='admin', password='123')
        user2 = User.objects.create(idauth=django_user2, type='admin')

        self.login_user('admin', '123')

        link = self.browser.find_element(By.LINK_TEXT, 'Users')
        link.click()
        time.sleep(5)
        submit_btn = self.browser.find_element(By.CSS_SELECTOR, 'button[value="remove"]')
        submit_btn.click()
        time.sleep(2)

class CreateCollabFunctionalTestCase(FunctionalTestCase):

    def test_accept_collab_request(self):
        user1, user2, _ = self.create_test_users()

        pl = Playlist.objects.create()
        collab = Collab.objects.create(
            iduser=user1,
            idplaylist=pl,
            status='created'
        )
        Participated.objects.create(
            iduser=user2,
            idcollab=collab
        )

        request = Requestcollab.objects.create(
            idusersend=user1,
            iduserrecieve=user2,
            idcollab=collab
        )

        self.login_user('masa', '123')

        self.assertIn('dusan', self.browser.page_source)
        self.assertIn('join a collab', self.browser.page_source)

        accept_btn = self.browser.find_element(By.CSS_SELECTOR, 'button[value="accept"]')
        accept_btn.click()

        time.sleep(3)

        self.assertEqual(Requestcollab.objects.count(), 0)
        self.assertEqual(Participated.objects.count(), 2)

    def test_deny_collab_request(self):
        user1, user2, _ = self.create_test_users()

        pl = Playlist.objects.create()
        collab = Collab.objects.create(
            iduser=user1,
            idplaylist=pl,
            status='created'
        )
        Participated.objects.create(
            iduser=user2,
            idcollab=collab
        )

        request = Requestcollab.objects.create(
            idusersend=user1,
            iduserrecieve=user2,
            idcollab=collab
        )

        self.login_user('masa', '123')

        self.assertIn('dusan', self.browser.page_source)
        self.assertIn('join a collab', self.browser.page_source)

        deny_btn = self.browser.find_element(By.CSS_SELECTOR, 'button[value="deny"]')
        deny_btn.click()

        time.sleep(3)
        self.assertEqual(Requestcollab.objects.count(), 0)

    def test_create_new_collab(self):
        user1, _, _ = self.create_test_users()
        self.login_user('dusan', '123')

        create_btn = self.browser.find_element(By.CSS_SELECTOR, 'button.new_collab')
        create_btn.click()

        time.sleep(2)

        self.assertIn('/createCollab/', self.browser.current_url)

        time.sleep(3)
        self.assertEqual(Collab.objects.filter(status='created').count(), 1)
        collab = Collab.objects.first()
        self.assertEqual(collab.iduser, user1)
        self.assertEqual(Participated.objects.filter(idcollab=collab).count(), 1)

    def test_invite_friend_to_collab(self):
        user1, user2, _ = self.create_test_users()

        req = Requestfriendship.objects.create(idusersend=user1, iduserrecieve=user2)
        Friendship.objects.create(request=req)

        self.login_user('dusan', '123')

        create_btn = self.browser.find_element(By.CSS_SELECTOR, 'button.new_collab')
        create_btn.click()

        time.sleep(2)

        self.assertIn('masa', self.browser.page_source)

        add_friend_btn = self.browser.find_element(By.CSS_SELECTOR, 'button.addfriend')
        add_friend_btn.click()

        time.sleep(3)

        self.assertEqual(Requestcollab.objects.count(), 1)
        invite = Requestcollab.objects.first()
        self.assertEqual(invite.idusersend, user1)
        self.assertEqual(invite.iduserrecieve, user2)

    def test_start_collab_with_name(self):
        user1, user2, _ = self.create_test_users()

        req = Requestfriendship.objects.create(idusersend=user1, iduserrecieve=user2)
        Friendship.objects.create(request=req)

        playlist = Playlist.objects.create(name='')
        collab = Collab.objects.create(
            iduser=user1,
            idplaylist=playlist,
            status='created'
        )
        Participated.objects.create(iduser=user1, idcollab=collab)
        Participated.objects.create(iduser=user2, idcollab=collab)

        self.login_user('dusan', '123')

        self.browser.get(f'{self.appUrl}/createCollab/{collab.idcollab}')
        time.sleep(2)

        name_input = self.browser.find_element(By.NAME, 'name')
        name_input.send_keys('Summer Vibes 2024')

        start_btn = self.browser.find_element(By.CSS_SELECTOR, 'button.new_collab')
        start_btn.click()

        time.sleep(2)

        self.assertIn('/collabPage/', self.browser.current_url)

        collab.refresh_from_db()
        self.assertEqual(collab.status, 'active')
        self.assertEqual(collab.name, 'Summer Vibes 2024')

    def test_start_collab_without_name(self):
        user1, user2, _ = self.create_test_users()

        req = Requestfriendship.objects.create(idusersend=user1, iduserrecieve=user2)
        Friendship.objects.create(request=req)

        playlist = Playlist.objects.create(name='')
        collab = Collab.objects.create(
            iduser=user1,
            idplaylist=playlist,
            status='created'
        )
        Participated.objects.create(iduser=user1, idcollab=collab)
        Participated.objects.create(iduser=user2, idcollab=collab)

        self.login_user('dusan', '123')

        self.browser.get(f'{self.appUrl}/createCollab/{collab.idcollab}')
        time.sleep(2)

        name_input = self.browser.find_element(By.NAME, 'name')
        name_input.send_keys('')

        start_btn = self.browser.find_element(By.CSS_SELECTOR, 'button.new_collab')
        start_btn.click()

        time.sleep(2)

        self.assertIn('You have to enter', self.browser.page_source)

    def test_collab_limit_three_people(self):
        user1, user2, user3 = self.create_test_users()

        django_user4 = djangoUser.objects.create_user(username='pera', password='123')
        user4 = User.objects.create(idauth=django_user4, type='regular')
        django_user5 = djangoUser.objects.create_user(username='zika', password='123')
        user5 = User.objects.create(idauth=django_user5, type='regular')

        req1 = Requestfriendship.objects.create(idusersend=user1, iduserrecieve=user2)
        Friendship.objects.create(request=req1)
        req2 = Requestfriendship.objects.create(idusersend=user1, iduserrecieve=user3)
        Friendship.objects.create(request=req2)
        req3 = Requestfriendship.objects.create(idusersend=user1, iduserrecieve=user4)
        Friendship.objects.create(request=req3)
        req3 = Requestfriendship.objects.create(idusersend=user1, iduserrecieve=user5)
        Friendship.objects.create(request=req3)

        self.login_user('dusan', '123')

        create_btn = self.browser.find_element(By.CSS_SELECTOR, 'button.new_collab')
        create_btn.click()
        time.sleep(2)

        add_buttons = self.browser.find_elements(By.CSS_SELECTOR, 'button.addfriend')

        for i in range(min(3, len(add_buttons))):
            add_buttons = self.browser.find_elements(By.CSS_SELECTOR, 'button.addfriend')
            add_buttons[0].click()
            time.sleep(1)

        time.sleep(2)
        add_buttons = self.browser.find_elements(By.CSS_SELECTOR, 'button.addfriend')

        if add_buttons:
            add_buttons[0].click()
            time.sleep(2)

            self.assertIn('maximum of 3 people', self.browser.page_source)

    def test_collab_limit_five_total(self):
        user1, _, _ = self.create_test_users()

        for i in range(5):
            pl = Playlist.objects.create()
            collab = Collab.objects.create(iduser=user1, idplaylist=pl, status='active', name="Playlist " + str(i))
            Participated.objects.create(iduser=user1, idcollab=collab)
        self.login_user('dusan', '123')
        create_btn = self.browser.find_element(By.CSS_SELECTOR, 'button.new_collab')
        create_btn.click()

        time.sleep(2)

        self.assertIn('maximum of 5 collabs', self.browser.page_source)

class TrendingFunctionalTestCase(FunctionalTestCase):

    def test_view_trending_page(self):
        user1, _, _ = self.create_test_users()

        pl = Playlist.objects.create(name='Top Hits 2024')
        Created.objects.create(iduser=user1, idplaylist=pl, trending=1)

        self.login_user('dusan', '123')

        trending_link = self.browser.find_element(By.LINK_TEXT, 'Trending')
        trending_link.click()

        time.sleep(2)

        self.assertIn('/trending', self.browser.current_url)
        self.assertIn('Top Hits 2024', self.browser.page_source)

    def test_like_playlist(self):
        user1, user2, _ = self.create_test_users()

        pl = Playlist.objects.create(name='Chill Vibes')
        created = Created.objects.create(iduser=user1, idplaylist=pl, trending=1)

        self.login_user('masa', '123')

        self.browser.get(f'{self.appUrl}/trending/')
        time.sleep(2)

        like_btn = self.browser.find_element(By.CSS_SELECTOR, 'button.like-btn')
        self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", like_btn)
        time.sleep(2)
        like_btn.click()

        time.sleep(2)

        self.assertEqual(Liked.objects.filter(created=created).count(), 1)
