from django.contrib import admin

'''
username : qrcode
password : qrcode
'''
# Register your models here.
from django.contrib import admin
from .models import Student, Present

# Register your models here.
class SAdmin(admin.ModelAdmin):
    list_display = ['id', 'studentname', 'roll', 'email', 'mobile', 'dob', 'address', 'classes', 'blood', 'college' , 'password', 'status', 'qr']

class Pr(admin.ModelAdmin):
    list_display = ['id', 'studentname', 'roll', 'classes', 'mobile', 'college' , 'date']

admin.site.register(Student, SAdmin)
admin.site.register(Present, Pr)