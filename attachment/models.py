from django.db import models
import datetime
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)
# Create your models here.


class UserManager(BaseUserManager):

    def create_user(self, username, email, password=None):
        if username is None:
            raise TypeError('Users must have a username')
        if email is None:
            raise TypeError('Users must have a Email')

        user = self.model(

            username=username,
            email=self.normalize_email(email)

        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, password=None):

        user = self.create_user(
            email,
            username,
            password=password,

        )

        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    
    
    USER_TYPE_CHOICES = (

        ('admin', "Admin"),
        ('employer', "Employer"),
        ('supervisor', "Supervisor"),
        ('student', "Student"),
    )

    email = models.EmailField(max_length=100, unique=True)
    username = models.CharField(max_length=100)
    user_type = models.CharField(max_length=10)
    registration_number = models.CharField(max_length=255, unique=True)
    staff_number = models.CharField(max_length=255, unique=True)
    employee_id = models.CharField(max_length=255, unique=True)
    organisation = models.CharField(max_length=255)
    designation = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'user_type']

    objects = UserManager()

    def __str__(self):
        return self.email


class Student(models.Model):

    name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    course = models.CharField(max_length=255)
    year = models.IntegerField(blank=True, null=True)
    school = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    organisation = models.CharField(max_length=255)
    start_date = models.DateField(default=datetime.date.today)
    end_date = models.DateField(default=datetime.date.today)
    assessed_by_employer = models.BooleanField(default=False)
    assessed_by_lecturer = models.BooleanField(default=False)
    user = models.OneToOneField(
        User, primary_key=True, on_delete=models.CASCADE)


class LogBook(models.Model):
    date = models.DateField(auto_now=False)
    description = models.TextField(max_length=500)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

class Reports(models.Model):
    pdf_file  =  models.FileField(upload_to='files/')
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
