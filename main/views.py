from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings

from users.models import Student, Aspirant

def home(request):
    if request.user.is_authenticated:
        student = None
        if Student.objects.filter(user = request.user).exists():
            student = Student.objects.get(user = request.user)
            
        aspirant = None
        if Aspirant.objects.filter(user = request.user).exists():
            aspirant = Aspirant.objects.get(user = request.user)
        
        context = {
            'student': student,
            'aspirant': aspirant,
        }
        print(context)
    else:
        context = {}
    return render(request, 'main/home.htm', context)


def see_all_students(request):
    if not request.user.is_authenticated:
        messages.error(request, f'You must sign in to the site first in order to see the list of seniors')
        return redirect('login')
    
    students = Student.objects.filter(private_mode = False)
    
    context = {
        'students': students,
    }
    
    return render(request, 'main/allStudents.htm', context)


def see_student_profile(request, student_slug):
    if not request.user.is_authenticated:
        messages.error(request, f'You must sign in to the site first in order to see the students information')
        return redirect('login')
    
    student = get_object_or_404(Student, student_slug = student_slug)
    
    if student is None:
        messages.error(request, f'Student not found!')
        return redirect('all_students')
    
    if student.user != request.user and student.private_mode:
        print("locker profile")
        messages.error(request, f'Sorry, the student has locked their profile')
        return redirect('all_students')
    
    context = {
        'student': student
    }
    
    return render(request, 'main/studentInfo.htm', context)
