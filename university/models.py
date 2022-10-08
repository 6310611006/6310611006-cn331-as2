from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def create_user_picks(sender, instance, created, **kwargs):
    if created:
        Student.objects.create(name=instance)

class Subject(models.Model):
    subject_name = models.CharField(max_length=200)
    subject_id = models.CharField(max_length=200)
    section = models.CharField(max_length=200)
    academic_year = models.CharField(max_length=200)
    semester = models.CharField(max_length=200)
    num_seat = models.PositiveIntegerField(default = 0)
    status = models.BooleanField(default = False)

    def __str__(self):
        return f'{self.id}: {self.subject_id} {self.subject_name} {self.subject_id}: {self.section} {self.num_seat}'
        
    def is_seat_available(self):
        return self.num_seat > 0
            
class Student(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    subject_enroll = models.ManyToManyField(Subject, related_name='student')

    def __str__(self):
        return f"{self.name.first_name} {self.name.last_name}"