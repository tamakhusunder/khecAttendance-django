from django.contrib import admin
from .models import Profile,AttendanceTb,Holiday

# Register your models here.

# @admin.register(School)
# class SchoolAdmin(admin.ModelAdmin):
# 	list_display=('code','fullName','shortName','email','contact','address','active','createdDate','updatedDate')

admin.site.register(Profile)
admin.site.register(AttendanceTb)
admin.site.register(Holiday)