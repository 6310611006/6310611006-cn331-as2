from django.test import TestCase, Client
from .models import *
from django.contrib.auth.models import User


class UniversityTestCase(TestCase):
    def setUp(self):

        User.objects.create(username="zero", first_name="zero", last_name="sum")
        self.client.login(username='zero', password='zero234523')
        Subject.objects.create(subject_name="python", subject_id="CN101", section="314056", academic_year="1", semester="1", num_seat=1, status=True)

    def test_seat_available(self):
        subject = Subject.objects.first()
        self.assertTrue(subject.is_seat_available())

    def test_seat_isnot_available(self):
        subject = Subject.objects.first()
        subject.num_seat -= 1
        self.assertFalse(subject.is_seat_available())
