from django.conf.urls import url
from . import views

app_name = 'Application'

urlpatterns = [
    url(r'^$', views.index,name='index'),
    url(r'^login$', views.login, name='login'),
    # url(r'^(?P<id>[0-9]+)/$', views.studentDetail, name='student'),
    # url(r'^(?P<id>[0-9]+)/$', views.instructorDetail, name='instructor'),
    url(r'^Student$', views.update, name='update'),
    url(r'^Instructor$', views.updateInstructor, name='updateInstructor'),
    url(r'^edit$', views.update, name='edit'),
    url(r'^change$', views.updatePassword, name='change_password'),
    url(r'^change_password$', views.updatePassword, name='change_password'),
    url(r'^changeInstructor$', views.updatePasswordInstructor, name='change_password_Instructor'),
    url(r'^change_password_Instructor$', views.updatePasswordInstructor, name='change_password_Instructor'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^view_all_courses$', views.getAllCourses, name='view_all_courses'),
    url(r'^myCourses$', views.myClasses, name='my_classes'),
    url(r'^my_courses$', views.getMyCourses, name='my_courses'),
    url(r'^student/enroll/(?P<name>[\w|\W]+)/(?P<id>\d+)$',views.doEnrollement, name='student_enroll'),
    url(r'^student/remove/(?P<id>\d+)$',views.removeEnrollment, name='remove_enrollment'),
    url(r'^instructor/view/(?P<id>\d+)$', views.viewStudents, name='view_student'),
    url(r'^About$', views.about, name='About_us'),
    url(r'^About_us$', views.about_us, name='About_us_instructor'),
    url(r'^Contact$', views.contact, name='Contact'),
    url(r'^Contact_us$', views.contact_us, name='Contact_us'),
    url(r'^Home$', views.home, name='Home'),
    url(r'^Home_Instructor$', views.home_instructor, name='Home_instructor'),
    # url(r'^Application/(?P<pk>[0-9]+)/$', views.login, name='login')
]
