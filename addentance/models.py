from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime


class Branch(models.Model):
    branch_name = models.CharField(max_length = 100)
    branch_abr = models.CharField(max_length = 7)
    
    def __str__(self):
        return self.branch_name
    



class Subject(models.Model):
    subject_name = models.CharField(max_length = 100)
    subject_abbr = models.CharField(max_length = 5)

    def __str__(self):
        return self.subject_abbr
    
class Student(models.Model):
    first_name  = models.CharField(max_length = 100)
    last_name  = models.CharField(max_length = 100)
    roll_no  = models.CharField(max_length = 100)
    
    def __str__(self):
        return self.first_name

class Teacher(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,blank=True, null=True)
    first_name  = models.CharField(max_length = 100)
    last_name  = models.CharField(max_length = 100)
    faculty_id  = models.CharField(max_length = 100)

    def __str__(self):
        return self.first_name


class Teacher_Detail(models.Model):
    teacher = models.ForeignKey('Teacher',on_delete=models.CASCADE,blank=True, null=True)
    subject = models.ForeignKey('Subject',on_delete=models.CASCADE,blank=True, null=True)
    classes = models.ManyToManyField('Class')

    def __str__(self):
        return f"{self.teacher.faculty_id} for {self.subject.subject_name}"

class AttendanceTimestamp(models.Model):
    student  = models.ForeignKey('Student',on_delete=models.CASCADE,blank=True, null=True)
    subject = models.ForeignKey('Subject',on_delete=models.CASCADE,blank=True, null=True)
    present = models.BooleanField()
    timestamp = models.DateTimeField()

    def __str__(self):
        return f"{self.student} for {self.subject.subject_name} on {self.timestamp}"
    


class Attendance(models.Model):
    student  = models.ForeignKey('Student',on_delete=models.CASCADE,blank=True, null=True)
    subject = models.ForeignKey('Subject',on_delete=models.CASCADE,blank=True, null=True)
    detailed_attendance = models.ManyToManyField('AttendanceTimestamp',blank=True)
    not_attended = models.IntegerField(default=0)
    total = models.IntegerField(default=0)

    def __str__(self):
        return  f"Attendance of {self.student.roll_no} for {self.subject.subject_abbr}"

    def attendance(self):
        try:
            attendance = ( (self.total - self.not_attended) / self.total )* 100 

        except :
            attendance=0
        return round(attendance,2)

class Student_Attendance(models.Model):
    student = models.ForeignKey('Student',on_delete=models.CASCADE,blank=True, null=True)
    attendance = models.ManyToManyField('Attendance')
    class_s = models.ForeignKey('Class',on_delete=models.CASCADE,blank=True, null=True)

    def __str__(self):
        return  f"Attendance of {self.student.roll_no} "

    
class Class(models.Model):
    academic_year = models.PositiveIntegerField(
            validators=[
                MinValueValidator(1900), 
                MaxValueValidator(datetime.datetime.now().year)],
            help_text="Use the following format: <YYYY>")
    semester =  models.PositiveIntegerField(
            validators=[
                MinValueValidator(1), 
                MaxValueValidator(8)],
    )
    division = models.CharField(max_length=2, blank=True, null=True)
    branch = models.ForeignKey('Branch',on_delete=models.CASCADE)
    students = models.ManyToManyField('Student')

    def __str__(self):
        return self.branch.branch_name







    