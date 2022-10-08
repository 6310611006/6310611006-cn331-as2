from urllib import response
from django.test import TestCase, Client
from .models import *
from django.urls import reverse, resolve
from university.views import *


class TestUrls(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('zero', 'test@hotmail.com', 'zero234523')
        self.client.login(username='zero', password='zero234523')

    def test_home_url_is_resolved(self):
        url = reverse('home-page')
        self.assertEquals(resolve(url).func, HomePage)
        
    def test_about_url_is_resolved(self):
        url = reverse('about-page')
        self.assertEquals(resolve(url).func, AboutPage)

    def test_contactus_url_is_resolved(self):
        url = reverse('contact-page')
        self.assertEquals(resolve(url).func, ContactusPage)
