from django.contrib import admin

from .models import Users, Instructor, Course, Student, Course_Student

admin.site.register(Users)
admin.site.register(Instructor)
admin.site.register(Course)
admin.site.register(Student)
admin.site.register(Course_Student)
