from django.urls import path
from . import views
urlpatterns = [
    #localhost:8000/
    path('',views.HomePage,name='home-page'),
    path('about/',views.AboutPage,name='about-page'),
    path('contact/',views.ContactusPage,name='contact-page'),
    path('register/',views.Register,name='register-page'),
    path('enrolled/',views.enrolled,name='enrolled-page'),
    path('subject/',views.subject, name='subject-page'),
    path('subject/<str:pk>',views.post,name='add-enrolled'),
    path('enrolled/<str:pk>',views.delete, name = 'delete-enrolled'),
    
    
   
    
]
