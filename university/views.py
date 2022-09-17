from itertools import product
from re import X, sub
from django.contrib.auth.decorators import login_required
from subprocess import SubprocessError
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.template import loader
from .models import Student, Subject, Enrolled
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import messages

def HomePage(request):
    return render(request, "university/home.html") 
    #return HttpResponse('<h1>Hello World</h1>')

def AboutPage(request):
    return render(request, "university/about.html") 
    #return HttpResponse('<h1>Hello World</h1>')


def ContactusPage(request):
    return render(request, "university/contactus.html") 


def Register(request):

    if request.method == 'POST':
        data = request.POST.copy()
        first_name = data.get('first_name')
        last_name =  data.get('last_name')
        email = data.get('email')
        username = data.get('username')
        password = data.get('password')

        newuser = User()
        newuser.username = username
        newuser.first_name = first_name
        newuser.last_name = last_name
        newuser.email = email
        newuser.set_password(password)
        newuser.save()
        return redirect('home-page')

    return render(request, "university/register.html")


    #main page
    #"not_enroll_subject": Subject.objects.exclude(enrolled_student = Student.objects.get(pk=int(request.user.username))
@login_required(login_url="/login")
def subject(request):
    subject = Subject.objects.all()
    #enrolled = Enrolled.objects.values_list('subject_id')
    enrolled = Enrolled.objects.all()
    
    return render(request, "university/subject.html", {
        "subject": subject,
        "enrolled": enrolled,
    })
@login_required(login_url="/login")
def enrolled(request):
    enrolled = Enrolled.objects.all()
    return render(request, "university/enrolledsubject.html", {
        "enrolled": enrolled,
    })
@login_required(login_url="/login")
def post(request,pk):
    enroll = str(request.POST['enroll'])
    subject = Subject.objects.get(subject_id = enroll)
    mydata = Subject.objects.filter(subject_id = enroll).values()
    
    for x in mydata:
        subject_id = x['subject_id']
        subject_name = x['subject_name']
        semester = x['semester']
        academic_year = x['academic_year']
        num_seats = x['num_seats'] - 1
        p = Enrolled(subject_id = subject_id,subject_name = subject_name,semester = semester,academic_year = academic_year,num_seats = num_seats)
        p.save()
        subject.num_seats = subject.num_seats - 1
        subject.save()
        messages.success(request, "Enroll Successfully")
        return redirect('subject-page')
    return redirect('subject-page')
    
@login_required(login_url="/login")
def delete(request,pk):
    #delete = Enrolled.objects.filter(subject_id=pk)
    #delete.delete()
    #messages.success(request, "Deleted Enrolled Successfully")
    delete = str(request.POST['delete'])
    Enrolled.objects.filter(subject_id = delete).delete()
    subject = Subject.objects.get(subject_id = delete)
    subject.num_seats = subject.num_seats + 1
    subject.save()
    messages.success(request, "Delete Enrolled Successfully")
    return redirect('enrolled-page')