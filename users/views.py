from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
import xlrd
from django.conf import settings
from django.contrib import messages


from users.models import Student, Aspirant
from allauth.socialaccount.models import SocialAccount

from users.forms import StudentRegistrationForm, AspirantRegistrationForm, StudentUpdateForm

STUDENTS_SHEET = settings.STUDENTS_SHEET

@staff_member_required
def update_student_list(request):
    if request.user.is_superuser:
        students = Student.objects.all()
        
        wb = xlrd.open_workbook(STUDENTS_SHEET)
        sheet = wb.sheet_by_index(0)
        sheet.cell_value(0, 0)

        rows = sheet.nrows
        cols = sheet.ncols

        for i in range(1, rows):
            bits_email = sheet.cell_value(i, 1)
            name = sheet.cell_value(i, 2)
            bits_id = sheet.cell_value(i, 3)
            campus = sheet.cell_value(i, 4)
            contact_regarding = sheet.cell_value(i, 6)
            fb_profile = sheet.cell_value(i, 7)
            phone_number = sheet.cell_value(i, 8)
            contact_time = sheet.cell_value(i, 9)
            
            try: 
                student = Student.objects.get(bits_email = bits_email)
                
                student.bits_email = bits_email
                student.bits_id = bits_id
                student.name = name
                student.campus = campus
                student.fb_profile = fb_profile
                student.phone_number = phone_number
                student.contact_regarding = contact_regarding
                student.contact_time = contact_time
                
                student.save()
                student.extract_branches()
                student.save()
            except:
                student = Student.objects.create(
                    bits_email = bits_email,
                    bits_id = bits_id,
                    name = name,
                    campus = campus,
                    fb_profile = fb_profile,
                    phone_number = phone_number,
                    contact_regarding = contact_regarding,
                    contact_time = contact_time
                )
                student.save()
                
                student.extract_branches()
                student.save()

        return redirect('home')
           
    else:
        messages.error(request, 'You are not authorized to access that page!')
        return redirect('home')

@login_required
def login_redirection(request):

    if request.user.email is None or request.user.email == "":
        # no profile has been created yet
        print(78)
        if SocialAccount.objects.filter(user = request.user).exists():
            social_account = SocialAccount.objects.get(user = request.user)
            print(social_account)
            if social_account.provider == "google" or social_account.provider == "Google":
                print(social_account.extra_data)
                # request.user.email = social_account.extra_data["email"]
                # request.user.username = social_account.extra_data["email"]
                # request.user.save()
                
                if "bits-pilani.ac.in" in request.user.email:
                    # BITS Student -> redirect to Student Registration
                    return redirect('student_registration')
                else:
                    # not BITS Student -> redirect to Aspirant Registration
                    return redirect('aspirant_registration')
                    
    else:
        if "bits-pilani.ac.in" in request.user.email:
            # BITS Student -> redirect to Student Registration
            return redirect('student_registration')
        else:
            # not BITS Student -> redirect to Aspirant Registration
            return redirect('aspirant_registration')
        

@login_required
def student_registration(request):
    user = request.user
    email = user.email 
    
    if Student.objects.filter(user = request.user).exists():
        student = Student.objects.get(user = request.user)
        messages.success(request, 'Welcome, ' + student.name + '!')
        return redirect('home')
    elif Student.objects.filter(bits_email = email).exists():
        student = Student.objects.get(bits_email = email)
        student.user = request.user
        student.save()
    
    if request.method == "POST":
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            student = form.instance
            student.user = request.user
            student.bits_email = request.user.email
            student.save()
            student.extract_branches()
            student.save()
            
            messages.success(request, 'You have been registered successfully!', fail_silently=True)
            return redirect('home')
    else:
        form = StudentRegistrationForm()

    return render(request, 'main/studentRegistration.htm', {'form' : form, 'userName': user.first_name + " " + user.last_name})

@login_required
def update_student_profile(request):
    user = request.user
    if Student.objects.filter(user = request.user).exists():
        student = Student.objects.get(user = request.user)
        
        if request.method == "POST":
            form = StudentUpdateForm(request.POST, instance=student)
            
            if form.is_valid():
                print("ssup")
                student = form.instance
                print(request.POST)
                try:
                    on = request.POST["private_mode"]
                    student.private_mode = True 
                except:
                    student.private_mode = False 
                    
                student.save()
                
                messages.success(request, 'Details updated successfully!', fail_silently=True)
                return redirect('home')
        else:
            form = StudentUpdateForm()
            
        return render(request, 'main/studentUpdate.htm', {'form' : form, 'student': student})
    else:
        messages.error(request, 'Unauthorized access!', fail_silently=True)
        return redirect('home')

@login_required
def aspirant_registration(request):
    user = request.user
    
    if Aspirant.objects.filter(user = request.user).exists():
        aspirant = Aspirant.objects.get(user = request.user)
        messages.success(request, 'Hi, ' + aspirant.name + '!')
        return redirect('home')
    
    if request.method == "POST":
        form = AspirantRegistrationForm(request.POST)
        if form.is_valid():
            aspirant = form.instance
            aspirant.user = request.user
            aspirant.save()
            
            messages.success(request, 'You have been registered successfully!', fail_silently=True)
            return redirect('home')
    else:
        form = AspirantRegistrationForm()

    return render(request, 'main/aspirantRegistration.htm', {'form' : form, 'userName': user.first_name + " " + user.last_name})

