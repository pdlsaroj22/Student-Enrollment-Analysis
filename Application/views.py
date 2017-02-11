from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.views import generic
from django.template.context import RequestContext
from django.conf import settings
from .forms import CourseForm, UserForm, StudentForm, InstructorForm
import logging
from django.core.mail import send_mail
from .models import Course, Instructor, Student, Users, Course_Student
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.template.context_processors import request
import operator
from django.db.models import Q
from functools import reduce

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


def about(request):
    return render(request, 'Application/student/AboutUs.html', {'username': request.session['username']})


def about_us(request):
    return render(request, 'Application/instructor/AboutUs.html', {'username': request.session['username']})


def contact(request):
    return render(request, 'Application/student/contact.html', {'username': request.session['username']})


def contact_us(request):
    return render(request, 'Application/instructor/contact.html', {'username': request.session['username']})


def home(request):
    return render(request, 'Application/student/Home.html', {'username': request.session['username']})


def home_instructor(request):
    return render(request, 'Application/instructor/Home.html', {'username': request.session['username']})


# def signup(request):
#     return render(request, 'Application/student/Student.html')


def updatePassword(request):
    if request.session.has_key('username'):
        if request.method == 'GET':
            return render(request, 'Application/student/updatePassword.html', {'username': request.session['username']})
        elif request.method == 'POST':
            user = Users.objects.get(username=request.session['username'])
            current_password = request.POST['currentPassword']
            new_password = request.POST['newPassword']
            confirm_password = request.POST['confirmPassword']
            print(current_password)
            print(new_password)
            print(user.password)
            if current_password == user.password:
                if new_password == confirm_password:
                    user.password = new_password
                    user.save()
                    return render(request, 'Application/student/success.html',
                                  {"message": "Password Successfully changed"})
                else:
                    return render(request, 'Application/student/updatePassword.html', {"message": "Error: new and confirm password doesn't match", 'username': request.session['username']})
            else:
                return render(request, 'Application/student/updatePassword.html', {"message":"Error: Current password doesn't match.", 'username': request.session['username']})


def updatePasswordInstructor(request):
    if request.session.has_key('username'):
        if request.method =='GET':
            return render(request, 'Application/instructor/updatePassword.html', {'username': request.session['username']})
        elif request.method=='POST':
            user = Users.objects.get(username=request.session['username'])
            current_password = request.POST['currentPassword']
            new_password = request.POST['newPassword']
            confirm_password = request.POST['confirmPassword']
            print(current_password)
            print(new_password)
            print(user.password)
            if current_password == user.password:
                if new_password == confirm_password:
                    user.password = new_password
                    user.save()
                    return render(request, 'Application/instructor/success.html',
                                  {"message": "Password Successfully changed"})
                else:
                    return render(request, 'Application/instructor/updatePassword.html', {"message": "Error: New and confirm password doesn't match", 'username':request.session['username']})
            else:
                return render(request, 'Application/instructor/updatePassword.html', {"message":"Error:Current password doesn't match.",'username': request.session['username']})



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
            return render(request, "Application/student/Home.html", {'username': username})
        elif user[0].userRole == 'instructor':
            request.session['username'] = username
            request.session['id'] = user[0].id
            return render(request, "Application/instructor/Home.html", {'username': username})
    else:
        print("inside else")
        return render(request, "Application/login.html", {"message": "invalid credentials"})


def logout(request):
    request.session['username']={}
    request.session['id']={}
    return redirect('/')


def update(request):
    if request.session.has_key('username'):
        if request.method=='GET':
           # print(request.session['username'])
           user = Users.objects.filter(username=request.session['username'])
           # print(user)
           student = Student.objects.get(user=user)
           print(student)
           return render(request, 'Application/student/UpdateStudent.html',{'student':student, 'username': request.session['username']})
        elif request.method == 'POST':
            # studentForm = StudentForm(request.POST)
            # student = Student
            user = Users.objects.filter(username=request.session['username'])
            student=Student.objects.get(user=user)
            student.firstName = request.POST['firstname']
            student.lastName = request.POST['lastname']
            student.email = request.POST['email']
            student.address = request.POST['address']
            student.contact_number = request.POST['contact_number']
            student.save()
            return render(request, "Application/student/Home.html", {'users': request.session['username']})

def updateInstructor(request):
    if request.session.has_key('username'):
        if request.method == 'GET':
                        # print(request.session['username'])
            user = Users.objects.filter(username=request.session['username'])
                        # print(user)
            instructor = Instructor.objects.get(user=user)
            print(instructor)
            return render(request, 'Application/instructor/UpdateInfo.html', {'instructor': instructor, 'username': request.session['username']})
        elif request.method == 'POST':
                        # instructorForm = instructorForm(request.POST)
                        # instructor = instructor
            user = Users.objects.filter(username=request.session['username'])
            instructor = Instructor.objects.get(user=user)
            instructor.firstName = request.POST['firstname']
            instructor.lastName = request.POST['lastname']
            instructor.email = request.POST['email']
            instructor.address = request.POST['address']
            instructor.contact_number = request.POST['contact_number']
            instructor.save()
            return render(request, "Application/instructor/instructor.html",{'users': request.session['username']})


def getAllCourses(request):
    if request.session.has_key('username'):
        courses = Course.objects.all().order_by('id')
        user = Users.objects.filter(username=request.session['username'])
        student = Student.objects.get(user=user)
        fees_paid = student.fees_paid
        print(fees_paid)
        enrolledCourses = Course_Student.objects.filter(student=student)
        courses_set = set()
        if len(courses_set):
            courses_set.clear()
        for c in courses:
            courses_set.add(c.course_name)
        print(courses_set)
        enrolled_course_set = set()
        if len(enrolled_course_set):
            enrolled_course_set.clear()
        for en in enrolledCourses:
            enrolled_course_set.add(en.course.course_name)
        print(enrolled_course_set)
        not_enrolled_course_set = set()
        if len(not_enrolled_course_set):
            not_enrolled_course_set.clear()
        not_enrolled_course_set = courses_set - enrolled_course_set
        not_enrolled_course_set = list(not_enrolled_course_set)
        print(not_enrolled_course_set)
        query = reduce(operator.or_, (Q(course_name__contains=item) for item in not_enrolled_course_set))
        print(query)
        not_enrolled_courses = Course.objects.filter(query)
        print("Not enrolled courses:", not_enrolled_courses)
        paginator = Paginator(courses, 10)
        try:
            page = int(request.GET.get('page', '1'))
        except:
            page = 1

        try:
            courses = paginator.page(page)
        except(EmptyPage, InvalidPage):
            courses = paginator.page(paginator.num_pages)

        return render(request, "Application/student/allcourses.html",
                                  {'not_enrolled_courses': not_enrolled_courses, 'username': request.session['username'], 'fees_paid': fees_paid})
    else:
        return redirect('/nofound')

def getMyCourses(request):
    if request.session.has_key('username'):
        user = Users.objects.filter(username=request.session['username'])
        student = Student.objects.get(user=user)
        enrolledCourses = Course_Student.objects.filter(student=student)
        print("-------------testing------------")
        print(enrolledCourses)
        # for c in enrolledCourses:
        #     subject = 'Course Enrollment Confirmation'
        #     message = 'You are enrolled in \n ' + c.course.course_name
        #     from_email = settings.EMAIL_HOST_USER
        #     to_list = [student.email]
        #     print(student.email)
        #     send_mail(subject, message, from_email, to_list, fail_silently= True)
        #     print(c.course.course_name, c.course.course_code)
        # print(courses)
        paginator = Paginator(enrolledCourses, 10)
        try:
            page = int(request.GET.get('page', '1'))
        except:
            page = 1

        try:
            courses = paginator.page(page)
        except(EmptyPage, InvalidPage):
            courses = paginator.page(paginator.num_pages)

        return render(request, "Application/student/mycourses.html",
                                  {'enrolledCourses':enrolledCourses, 'username': request.session['username']},
                                  context_instance=RequestContext(request))
    else:
        return redirect('/nofound')


def myClasses(request):
    if request.session.has_key('username'):
        user = Users.objects.filter(username=request.session['username'])
        instructor = Instructor.objects.get(user=user)
        myCourses = Course.objects.filter(instructor= instructor)
        return render(request, "Application/instructor/myCourses.html",
                      {'myCourses': myCourses, 'username': request.session['username']},
                      context_instance=RequestContext(request))


def viewStudents(request, id):
    if request.session.has_key('username'):
        user = Users.objects.filter(username=request.session['username'])
        instructor = Instructor.objects.get(user=user)
        course = Course.objects.get(pk=id, instructor = instructor )
        print (course)
        courseStudent = Course_Student.objects.filter(course = course)
        paginator = Paginator(courseStudent, 10)

        try:
            page = int(request.GET.get('page', '1'))
        except:
            page = 1

        try:
            courseStudent = paginator.page(page)
        except(EmptyPage, InvalidPage):
            courseStudent = paginator.page(paginator.num_pages)
        return render(request, "Application/instructor/viewStudent.html",
                      {'viewStudent': courseStudent, 'username': request.session['username']},
                      context_instance=RequestContext(request))


def doEnrollement(request, name, id):
    if request.session.has_key('username'):
        user = Users.objects.filter(username=request.session['username'])
        student = Student.objects.get(user=user)
        # print("name", name, "id", id)
         # = Course.objects.filter(id=student)
        course = Course.objects.get(pk=id, course_name=name)
        print(student, course)
        student_course = Course_Student()
        student_course.student = student
        student_course.course = course
        student_course.save()
        return redirect('/view_all_courses')
        # enrolledCourses = Course_Student.objects.filter(student=student)
        # return render(request, 'Application/student/success.html',
        #               {"message": "Successfully enrolled to "+name})
    else:
        return redirect('/nofound')


def removeEnrollment(request, id):
    if request.session.has_key('username'):
        # user = Users.objects.filter(username=request.session['username'])
        print(id)
        courseStudent = Course_Student.objects.get(pk=id)
        print(courseStudent)
        courseStudent.delete()

        return redirect("/my_courses")
    else:
        return redirect('/notfound')