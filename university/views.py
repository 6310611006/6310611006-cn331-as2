from itertools import product
from re import X, sub
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from subprocess import SubprocessError
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.template import loader
from validate_email import validate_email
from .models import *
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

def HomePage(request):
    return render(request, "university/home.html") 
    #return HttpResponse('<h1>Hello World</h1>')

def AboutPage(request):
    return render(request, "university/about.html") 
    #return HttpResponse('<h1>Hello World</h1>')


def ContactusPage(request):
    return render(request, "university/contactus.html") 


class RegistrationView(View):
    def get(self, request):
        return render(request, 'university/register.html')

    def post(self, request):
        context = {

            'data': request.POST,
            'has_error': False
        }

        email = request.POST.get('email')
        username = request.POST.get('username')
        full_name = request.POST.get('name')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        if len(password) < 6:
            messages.add_message(request, messages.ERROR,
                                 'passwords should be atleast 6 characters long')
            context['has_error'] = True
        if password != password2:
            messages.add_message(request, messages.ERROR,
                                 'passwords dont match')
            context['has_error'] = True

        if not validate_email(email):
            messages.add_message(request, messages.ERROR,
                                 'Please provide a valid email')
            context['has_error'] = True

    
        if context['has_error']:
            return render(request, 'university/register.html', context, status=400)

        user = User.objects.create_user(username=username, email=email)
        user.set_password(password)
        user.first_name = full_name
        user.last_name = full_name
        
        user.save()

        

        return redirect('login')

class LoginView(View):
    def get(self, request):
        return render(request, 'university/login.html')

    def post(self, request):
        context = {
            'data': request.POST,
            'has_error': False
        }
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username == '':
            messages.add_message(request, messages.ERROR,
                                 'Username is required')
            context['has_error'] = True
        if password == '':
            messages.add_message(request, messages.ERROR,
                                 'Password is required')
            context['has_error'] = True
        user = authenticate(request, username=username, password=password)

        if not user and not context['has_error']:
            messages.add_message(request, messages.ERROR, 'Invalid login')
            context['has_error'] = True

        if context['has_error']:
            return render(request, 'university/login.html', status=401, context=context)
        login(request, user)
        return redirect('home-page')

class LogoutView(View):
    def post(self, request):
        logout(request)
        messages.add_message(request, messages.SUCCESS, 'Logout successfully')
        return redirect('login')



@login_required(login_url="login")
def subject_page(request):
    enroll = Student.objects.get(name__username=request.user).subject_enroll
    subject = Subject.objects.all()
    if enroll.filter(subject_id__in=subject.values_list('subject_id')) != None:
        subject = subject.exclude(subject_id__in=enroll.all().values_list('subject_id'))
    return render(request, 'university/subject.html',
    {
        'Subjects' : subject,
        'Enroll' : enroll
    })

@login_required(login_url="login")
def enrolled(request):
    enrolled = Student.objects.get(name__username=request.user).subject_enroll.order_by('subject_id')
    return render(request, 'University/enrolledsubject.html', {
        'Enrolled' : enrolled
    })

def enroll_subject(request):
    if request.method == "POST":
        subject = Subject.objects.get(subject_id=request.POST['subject_id'])
        student = Student.objects.get(name__username=request.POST['user'])
        Subject.objects.filter(subject_id=request.POST['subject_id']).update(num_seat=(subject.num_seat - 1))
        student.subject_enroll.add(subject)
        return HttpResponseRedirect(reverse('subject-page'))

def remove_enrolled(request):
    if request.method == "POST":
        subject = Subject.objects.get(subject_id=request.POST['subject_id'])
        student = Student.objects.get(name__username=request.POST['user'])
        Subject.objects.filter(subject_id=request.POST['subject_id']).update(num_seat=(subject.num_seat + 1))
        student.subject_enroll.remove(subject)
        return HttpResponseRedirect(reverse('subject-page'))


