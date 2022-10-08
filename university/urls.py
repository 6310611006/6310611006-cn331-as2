from django.urls import path
from . import views
urlpatterns = [
    #localhost:8000/
    path('',views.HomePage,name='home-page'),
    path('about/',views.AboutPage,name='about-page'),
    path('contact/',views.ContactusPage,name='contact-page'),
    path('register', views.RegistrationView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('subject', views.subject_page, name='subject-page'),
    path('enrolled', views.enrolled, name='enrolled'),
    path('enroll', views.enroll_subject, name='enroll-subject'),
    path('remove_enroll', views.remove_enrolled, name='remove-enroll'),

    
    
   
    
]
