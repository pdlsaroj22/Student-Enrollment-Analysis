from django.db import models


class Users(models.Model):
    username = models.CharField(max_length=50, blank=False, null=False,)
    password = models.CharField(max_length=50, blank=False, null=False)
    userRole = models.CharField(max_length=20, blank=False, null=False)

    def __str__(self):
        return self.username + '-' + self.userRole


class Instructor(models.Model):
    firstName = models.CharField(max_length=50, blank=False, null=False)
    lastName = models.CharField(max_length=50, blank=False, null=False)
    address = models.CharField(max_length=50, blank=False, null=False)
    email = models.CharField(max_length=50, blank=False, null=False)
    contact_number = models.CharField(max_length=50, blank=False, null=False)
    user = models.ForeignKey(Users)


    def __str__(self):
        return self.firstName+' '+self.lastName

class Course(models.Model):
    course_name = models.CharField(max_length=50, blank=False, null=False)
    course_code = models.CharField(max_length=50, blank=False, null=False)
    course_fee = models.BigIntegerField(blank=False, null=False, default=0)
    instructor = models.ForeignKey(Instructor)


    def __str__(self):
        return self.course_name +'-'+self.course_code


class Student(models.Model):
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    contact_number = models.CharField(max_length=50)
    user = models.ForeignKey(Users)
    fees_paid = models.BooleanField(blank=False, null=False, default=False)


    def __str__(self):
        return self.firstName+ ' '+self.lastName


class Course_Student(models.Model):
    course = models.ForeignKey(Course)
    student = models.ForeignKey(Student)


    def __str__(self):
        return self.student.user.username + '-'+ self.course.course_code

