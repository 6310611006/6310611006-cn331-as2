from pyexpat import model
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import *
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.db import models

class BaseTest(TestCase):
    def setUp(self):
        
        self.register_url=reverse('register')
        self.login_url=reverse('login')
        self.user={
            'email':'testemail@gmail.com',
            'username':'username',
            'first_name':'first_name',
            'last_name':'last_name',
            'password':'password',
            'password2':'password',
            'name':'fullname'
        }
        self.user_short_password={
            'email':'testemail@gmail.com',
            'username':'username',
            'first_name':'first_name',
            'last_name':'last_name',
            'password':'t',
            'password2':'t',
            'name':'fullname'
        }
        self.user_unmatching_password={

            'email':'testemail@gmail.com',
            'username':'username',
            'first_name':'first_name',
            'last_name':'last_name',
            'password':'password1',
            'password2':'password2',
            'name':'fullname'
        }

        self.user_invalid_email={
            
            'email':'test.com',
            'username':'username',
            'first_name':'first_name',
            'last_name':'last_name',
            'password':'password1',
            'password2':'password2',
            'name':'fullname'
        }
        return super().setUp()


class LoginTest(BaseTest):
    def test_can_access_page(self):
        response=self.client.get(self.login_url)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'university/login.html')
        #ทดสอบการเข้าถึงหน้า login ถ้าถูกต้อง status_code = 200 เเละมีการเรียกใช้ template university/login.html

    def test_login_success(self):
        self.client.post(self.register_url,self.user)
        response= self.client.post(self.login_url,self.user)
        self.assertEqual(response.status_code,302)
        #ทดสอบว่า login สำเร็จ 

    def test_cantlogin_with_no_username(self):
        response= self.client.post(self.login_url,{'username':'','password':'password'})
        self.assertEqual(response.status_code,401)
        #ทดสอบ method login ไม่สำเร็จเมื่อไม่ใส่ username 

    def test_cantlogin_with_no_password(self):
        response= self.client.post(self.login_url,{'username':'username','password':''})
        self.assertEqual(response.status_code,401)
        #ทดสอบ method login ไม่สำเร็จเมื่อไม่ใส่ password

    def test_login_notsuccess(self):
        response= self.client.post(self.login_url,{'username':'wronguser','password':'wrongpassword'})
        self.assertEqual(response.status_code,401)
        #ทดสอบ method login ไม่สำเร็จเมื่อใส่ username password ที่ไม่มีในระบบ

class RegisterTest(BaseTest):
   def test_can_view_page_correctly(self):
       response=self.client.get(self.register_url)
       self.assertEqual(response.status_code,200)
       self.assertTemplateUsed(response,'university/register.html')
       #ทดสอบการเข้าถึงหน้า register ถ้าถูกต้อง status_code = 200 เเละมีการเรียกใช้ template university/register.html

   def test_can_register_user(self):
        response=self.client.post(self.register_url,self.user)
        self.assertEqual(response.status_code,302)
        #ทดสอบว่า register สำเร็จ

   def test_cant_register_user_withshortpassword(self):
        response=self.client.post(self.register_url,self.user_short_password)
        self.assertEqual(response.status_code,400)
        #ทดสอบ method register ไม่สำเร็จเมื่อใส่ password น้อยกว่า 6 ตัว

   def test_cant_register_user_with_unmatching_passwords(self):
        response=self.client.post(self.register_url,self.user_unmatching_password)
        self.assertEqual(response.status_code,400)
        #ทดสอบ method register ไม่สำเร็จเมื่อใส่ password กับ confirm password ไม่ตรงกัน

   def test_cant_register_user_with_invalid_email(self):
        response=self.client.post(self.register_url,self.user_invalid_email)
        self.assertEqual(response.status_code,400)
        #ทดสอบ method register ไม่สำเร็จเมื่อใส่ email ผิดรูปเเบบ

class LogoutTest(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.client.login(username = 'zero', password = '1234')
    def test_logout(self):
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        #ทดสอบ logout ว่าสำเร็จไหม



    