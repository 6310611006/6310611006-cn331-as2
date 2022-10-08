from django.test import TestCase, Client
from django.urls import reverse
from django.db.models import Max
from django.contrib.auth.models import User
from django.urls import reverse, resolve
from .models import *
from .views import *
class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('zero', 'test@hotmail.com', 'zero234523')
        self.client.login(username='zero', password='zero234523')
        
    def test_home_status_code(self):
        response = self.client.get(reverse('home-page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'university/home.html')

    def test_about_status_code(self):
        response = self.client.get(reverse('about-page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'university/about.html')

    def test_contactus_status_code(self):
        response = self.client.get(reverse('contact-page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'university/contactus.html')

    def test_subject_page_status_code(self):
        response = self.client.get(reverse('subject-page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'university/subject.html')
    


class UniversityTestCase(TestCase):
    def setUp(self):
        User.objects.create(username="zero", first_name="zero", last_name="sum")
        self.client.login(username='zero', password='zero234523')
        Subject.objects.create(subject_name="python", subject_id="CN101", section="314056", academic_year="1", semester="1", num_seat=1, status=True)
        Subject.objects.create(subject_name="java", subject_id="CN201", section="156857", academic_year="1", semester="2", num_seat=0, status=True)
    
   
    def test_enroll(self):
        student = Student.objects.first()
        subject = Subject.objects.first()
        c = Client()
        c.post(reverse('enroll-subject'), {'user': student.name,'subject_id': subject.subject_id})
        self.assertEqual(Subject.objects.get(subject_id=subject.subject_id).num_seat, 0)

    def test_remove_enroll(self):
        student = Student.objects.first()
        subject = Subject.objects.get(pk= 2)
        c = Client()
        c.post(reverse('remove-enroll'), {'user': student.name,'subject_id': subject.subject_id})
        self.assertEqual(Subject.objects.get(subject_id=subject.subject_id).num_seat, 1)

