from django import forms 
from users.models import Student, Aspirant

class StudentRegistrationForm(forms.ModelForm):
    
    class Meta:
        model = Student
        fields = ('bits_id', 'name', 'campus', 'phone_number', 'fb_profile', 'contact_regarding', 'contact_time')
        
class StudentUpdateForm(forms.ModelForm):
    
    class Meta:
        model = Student
        fields = ('phone_number', 'contact_regarding', 'contact_time', 'private_mode')
 
class AspirantRegistrationForm(forms.ModelForm):
    
    class Meta:
        model = Aspirant
        fields = ('name',)
