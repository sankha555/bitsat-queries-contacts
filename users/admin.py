from django.contrib import admin
from users.models import Student, Aspirant

admin.site.register([Student, Aspirant])