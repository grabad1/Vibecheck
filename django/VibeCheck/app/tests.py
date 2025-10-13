from multiprocessing.connection import Client
from unittest import TestCase

from django.urls import reverse

from app.models import *
from django.contrib.auth.models import User as djangoUser


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

