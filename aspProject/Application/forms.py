from django import forms
from .models import Course, Users, Student, Instructor


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('course_name', 'course_code', 'course_fee', 'instructor')
        
        
class UserForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ("username", "password", "userRole")
        
        
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ("firstName", "lastName", "address", "email", "contact_number")


class InstructorForm(forms.ModelForm):
    class Meta:
        model = Instructor
        fields = ("firstName", "lastName", "address", "email", "contact_number")