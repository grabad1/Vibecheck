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
