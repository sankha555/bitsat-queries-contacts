from django.urls import path
from users.views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('update_students', update_student_list, name='update_student'),
    path('senior/register', student_registration, name='student_registration'),
    path('senior/update', update_student_profile, name='update_student_profile'),
    
    path('aspirant/register', aspirant_registration, name='aspirant_registration'),
    path('redirecting', login_redirection, name='login_redirection'),
     
    path('login', auth_views.LoginView.as_view(template_name='main/login.htm'), name='login'),
    
    path('logout', auth_views.LogoutView.as_view(template_name='main/logout.htm'), name='logout'),
]
