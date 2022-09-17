from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Subject(models.Model):

    subject_id = models.CharField(max_length=10,primary_key=True)
    subject_name = models.CharField(max_length=200)
    semester = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(2)], default =1)
    academic_year = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(4)], default =1)
    num_seats = models.IntegerField()
    available = models.BooleanField(default =True)
    
    
    def __str__(self):
        return self.subject_id + '-' + self.subject_name + '-' + str(self.semester) + '-' + str(self.academic_year) + '-' + str(self.num_seats)

class Enrolled(models.Model):

    subject_id = models.CharField(max_length=10,primary_key=True)
    subject_name = models.CharField(max_length=200)
    semester = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(2)], default =1)
    academic_year = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(4)], default =1)
    num_seats = models.IntegerField(validators=[MinValueValidator(1)])
    available = models.BooleanField(default =True)
    
   
    def __str__(self):
       return self.subject_id + '-' + self.subject_name + '-' + str(self.semester) + '-' + str(self.academic_year) + '-' + str(self.num_seats)

class Student(models.Model):
    first = models.CharField(max_length=64)
    last = models.CharField(max_length=64)
    enroll_subject = models.ManyToManyField(Subject, blank=True, related_name="studentenroll")

    def __str__(self):
        return self.first + '-' + self.last
