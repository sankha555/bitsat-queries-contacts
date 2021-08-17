from django.urls import path
from main.views import *

urlpatterns = [
    path('', home, name='home'),
    path('seniors/', see_all_students, name='all_students'),
    path('seniors/<str:student_slug>', see_student_profile, name='student_info'),
]
