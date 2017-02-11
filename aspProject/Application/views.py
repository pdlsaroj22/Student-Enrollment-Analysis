from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.views import generic
from django.template.context import RequestContext
from .forms import CourseForm, UserForm, StudentForm, InstructorForm
import logging
from .models import Course, Instructor, Student, Users
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.template.context_processors import request

logger = logging.getLogger()


#
# class LoginView(generic.FormView):
#     template_name = 'Application/login.html'

# class UserProfileView(DetailView):
#     model = Users
#     slug_field = 'username'
#     template_name = "Application/student/index.html"

def index(request):
    return render(request, 'Application/login.html')


def signup(request):
    return render(request, 'Application/student/Student.html')


def instructor(request):
    return render(request, 'Application/instructor/instructor.html')


def updatePassword(request):
    return render(request, 'Application/student/updatePassword.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = Users.objects.filter(username=username, password=password)
        if not user:
            print("no user found")
            return render(request, "Application/login.html", {"message": "invalid credentials"})
        elif user[0].userRole == 'student':
            request.session['username'] = username
            request.session['id']= user[0].id
            return render(request, "Application/student/Student.html", {'users': username})
        elif user[0].userRole == 'instructor':
            request.session['username'] = username
            request.session['id'] = user[0].id
            return render(request, "Application/instructor/instructor.html", {'users': Users})
    else:
        print("inside else")
        return render(request, "Application/login.html", {"message": "invalid credentials"})


def studentDetail(request, id):
    if not request.user.is_authenticated():
        return render(request, 'Application/login.html')
    else:
        user = get_object_or_404(Users, pk=id)
        return render(request, 'Application/student/Student.html', {'user': user})


def instructorDetail(request, id):
    if not request.user.is_authenticated():
        return render(request, 'Application/login.html')
    else:
        user = get_object_or_404(Users, pk=id)
        return render(request, 'Application/instructor/instructor.html', {'user': user})

def logout(request):
    request.session['username']={}
    request.session['id']={}
    return redirect('/')


def update(request):
    if request.session.has_key('username'):
       #username = request.session['username']
        return render(request, 'Application/signup.html')
       #print("check")
    #else:
       # return render(request, 'Application/login.html')
        # if (request.session['username'] == Users.username):
        #     if request.method == 'GET':
        #         student = Student.objects.get(pk=id)
        #         return render_to_response("Application/student/UpdateStudent.html", {'student': student}, context_instance=RequestContext(request))

        #     if request.method == 'POST':
        #         print
        #         request.POST.get('firstname')
        #         student = Student.objects.get(pk=id)
        #         student.firstname = request.POST.get('firstname')
        #         student.lastname = request.POST.get('lastname')
        #         student.contact_number = request.POST.get('contact_number')
        #         student.email = request.POST.get('email')
        #         student.address = request.POST.get('address')
        #         student.save()
        #         return redirect('/admin/allstudents')
        # else:
        #     return redirect('/notfound')
            #return render(request, 'Application/student/UpdateInfo.html')
