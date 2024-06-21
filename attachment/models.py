import math
import datetime
from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)
# Create your models here.


class UserManager(BaseUserManager):

    def create_user(self, email, username,  password=None):
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
    
    # USER_TYPE_CHOICES = (

    #     ('admin', "Admin"),
    #     ('employer', "Employer"),
    #     ('supervisor', "Supervisor"),
    #     ('student', "Student"),
    # )

    email = models.EmailField(max_length=100, unique=True)
    username = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_lecturer = models.BooleanField(default=False)
    is_supervisor = models.BooleanField(default = False)
    is_student = models.BooleanField(default=False)
    updated_profile = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['username']
    
    USERNAME_FIELD = 'email'
    

    objects = UserManager()

    def get_user(self,object=None):
        if object == self:
            return self

    def __str__(self):
        return self.email
    
class Lecturer(models.Model):
    name = models.CharField(max_length=255)
    faculty = models.CharField(max_length=255)
    school = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    telephone = models.CharField(max_length=100)
    official_email = models.CharField(max_length=255)
    user = models.OneToOneField(
        User, primary_key=True, on_delete=models.CASCADE, default=None)
    
    def __str__(self) :
        return self.name

class OrganisationSupervisor(models.Model):
    user = models.OneToOneField(
        User, primary_key=True, on_delete=models.CASCADE, default=None)
    def __str__(self) :
        return self.user
    
class Student(models.Model):
    name = models.CharField(max_length=255)
    registration_number = models.CharField(max_length=255, unique=True)
    course = models.CharField(max_length=255)
    year = models.IntegerField(blank=True, null=True)
    department = models.CharField(max_length=255)
    organisation = models.CharField(max_length=255)
    class_code = models.CharField(max_length = 10)
    start_date = models.DateField(default=datetime.date.today)
    end_date = models.DateField(default=datetime.date.today)
    photo_url = models.ImageField(upload_to="images/")
    assessed_by_employer = models.BooleanField(default=False)
    assessed_by_lecturer = models.BooleanField(default=False)
    user = models.OneToOneField(
        User, primary_key=True, on_delete=models.CASCADE, default=None)
    lecturer = models.ForeignKey(Lecturer, on_delete=models.CASCADE, related_name='students', null=True)
    supervisor = models.ForeignKey(OrganisationSupervisor, on_delete=models.CASCADE,related_name='students', null=True)

    def sum_total(self):
        try:
            score_1 = self.organisationassessment.get_score()
            score_2 = self.lecturerassessment.total_marks()

        except AttributeError:
            return 0

        sum = ((score_1 + score_2))

        score =  sum / 90
        return int((score * 100))

    def grade(self):
        sum = self.sum_total()
        grade = None
        if sum >= 70:
            grade = 'A'
        elif sum >=60 and sum < 70:
            grade = 'B'
        elif sum >=50 and sum < 60:
            grade = 'C'
        elif sum >=40 and sum < 50:
            grade = 'D'
        else:
            grade = 'F'
        return grade
        

class LogBook(models.Model):
    date = models.DateField(auto_now=False)
    description = models.TextField(max_length=500)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

class Reports(models.Model):
    pdf_file  =  models.FileField(upload_to='files/')
    student = models.OneToOneField(Student, on_delete=models.CASCADE)

    def __str__(self):
        return self.pdf_file.name

class OrganisationAssessment(models.Model):
    punctuality = models.PositiveSmallIntegerField(blank=True)
    adherence_to_regulation = models.PositiveSmallIntegerField(blank=True)
    workmanship = models.PositiveSmallIntegerField(blank=True)
    adaptability =models.PositiveSmallIntegerField(blank=True)
    communication = models.PositiveSmallIntegerField(blank=True)
    reliability = models.PositiveSmallIntegerField(blank=True)
    teamwork = models.PositiveSmallIntegerField(blank=True)
    general_remarks = models.TextField(max_length=300)
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    

    def get_score(self):
        sum  = (self.punctuality + self.adherence_to_regulation + self.workmanship 
                 + self.adaptability + self.communication + self.reliability + self.teamwork) 
        

        return sum
    
class LecturerAssessment(models.Model):
    respect_to_authority = models.PositiveSmallIntegerField(blank=True)
    appearance_grooming = models.PositiveSmallIntegerField(blank=True)
    following_instructions = models.PositiveSmallIntegerField(blank=True)
    enthusiasm = models.PositiveSmallIntegerField(blank=True)
    acheivment = models.PositiveSmallIntegerField(blank=True)
    panctuality = models.PositiveSmallIntegerField(blank=True)
    team_player = models.PositiveSmallIntegerField(blank=True)
    intergration_into_team = models.PositiveSmallIntegerField(blank=True)
    interaction_ability = models.PositiveSmallIntegerField(blank=True)
    empathy = models.PositiveSmallIntegerField(blank=True)
    safety_awareness = models.PositiveSmallIntegerField(blank=True)
    professional_ethics_application = models.PositiveSmallIntegerField(blank=True)
    current_trends_awareness = models.PositiveSmallIntegerField(blank=True)
    quality_of_work = models.PositiveSmallIntegerField(blank=True)
    tasks_completion = models.PositiveSmallIntegerField(blank=True)
    adopt_new_skills = models.PositiveSmallIntegerField(blank=True)
    work_competence = models.PositiveSmallIntegerField(blank=True)
    reliability = models.PositiveSmallIntegerField(blank=True)
    innovation = models.PositiveSmallIntegerField(blank=True)
    written_communication_profiency = models.PositiveSmallIntegerField(blank=True)
    verbal_communication = models.PositiveSmallIntegerField(blank=True)
    modern_technology = models.PositiveSmallIntegerField(blank=True)
    trade_language = models.PositiveSmallIntegerField(blank=True)
    general_perception = models.PositiveSmallIntegerField(blank=True)
    general_remarks = models.TextField(max_length=300)
    student = models.OneToOneField(Student, on_delete=models.CASCADE)

    def total_marks(self):
        marks_scored = (self.respect_to_authority + self.appearance_grooming + self.following_instructions + self.enthusiasm 
                        + self.acheivment + self.panctuality + self.team_player + self.intergration_into_team + self.interaction_ability 
                        + self.empathy + self.safety_awareness + self.quality_of_work + self.tasks_completion + self.adopt_new_skills
                        + self.work_competence + self.reliability + self.innovation + self.written_communication_profiency
                        + self.verbal_communication + self.modern_technology + self.trade_language + self.general_perception)
        
        return marks_scored

class SupervisorComment(models.Model):
    week = models.CharField(max_length=10)
    comment = models.CharField(max_length=255)
    status = models.BooleanField(default=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)


class Internship(models.Model):

    organisation = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    logo = models.ImageField(upload_to="images/")
    time_stamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

