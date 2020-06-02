from django.shortcuts import render,redirect
from django.views.generic import View
import datetime
from django.utils import timezone
import pytz
import csv
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import Teacher , Class,Attendance,Student_Attendance,Teacher_Detail,Subject,Student,AttendanceTimestamp

def isTeacher(class_,teacher,subject):
        '''
        This function checks if the teacher is assigned to the particular class
        it takes a Class object, a Subject object and a Teacher object (models)
        '''
        try:
            teacher_dets  = Teacher_Detail.objects.get(teacher=teacher, subject=subject) #getting the specific teacher detail
        except:
            teacher_dets = None
        
        if teacher_dets is not None:
            for class__ in teacher_dets.classes.all():
                if class_==class__:
                        return True
        return False


class HomeView(LoginRequiredMixin,View):
    def get(self,request,*args,**kwargs):
        '''
        renders a home page for teachers with listing all the classes assigned to them
        '''
        try : 
            teacher = Teacher.objects.get(user= request.user)
            teacher_dets =  Teacher_Detail.objects.filter(teacher=teacher)
        except:
            teacher = None
            return render()
        

        context = {
            'teacher' : teacher,
            'detail': teacher_dets,
        }
        return render(request , "home.html", context)


class ClassView(LoginRequiredMixin,View):
    def get(self,request,pk,subject_pk,*args,**kwargs):
        '''
        class view which takes 2 essential arguments: pk (class pk), subject_pk
        and it renders a table for every student with their attendance percentage and other details
        '''
        class_ = Class.objects.get(pk= pk)
        teacher = Teacher.objects.get(user= request.user)
        subject = Subject.objects.get(pk=subject_pk)

        if isTeacher(class_,teacher,subject):
            student_attendance = Student_Attendance.objects.filter(class_s = class_)
            context = {
                'subject_pk' : int(subject_pk),
                'subject':subject,
                'attendances':student_attendance,
                'class':class_
            }
            return render(request , "indiv_class.html", context )
        else:
            return redirect('home')
        

class MarkAttendanceView(LoginRequiredMixin,View):
    '''
    the most important function of this app
    this page is for marking attendance 
    it takes a class with the assigned teacher(user) and renders a list of student in the class (checkboxes)
    first select the date and time of the lecture and then
    you just have to select the student which are absent and submit the response
    '''
    def get(self,request,pk,subject_pk,*args,**kwargs):
        class_ = Class.objects.get(pk= pk)
        teacher = Teacher.objects.get(user= request.user)
        subject = Subject.objects.get(pk=subject_pk)
        
        if isTeacher(class_,teacher,subject):
            attendance = []
            for student in class_.students.all():
                attendance1 = Attendance.objects.get(student = student, subject=subject)
                attendance.append(attendance1)
            context = {
                'subject':subject,
                'students':attendance,
                'class':class_,
            }
            return render(request , "mark_attendance.html", context)
        else:
            return redirect('home')

    def post(self,request,pk,subject_pk,*args, **kwargs):
        _class_ =  Class.objects.get(pk = pk) #getting Class object
        lists=request.POST.getlist('attendance-absent-set') # list of absent students
        lecture_date = request.POST.get('lecture-date') # getting the date of lecture 
        lecture_time = request.POST.get('lecture-time') # getting the time of lecture
        lecture_datetime1 = lecture_date + ' '+ lecture_time  
        lecture_datetime=datetime.datetime.strptime(lecture_datetime1,'%Y-%m-%d %H:%M') # converting the str into datetime object
        subject = Subject.objects.get(pk=subject_pk) #Subject object
        for student_pk in lists: 
            '''
            looping through the absent student list and creating 
            an AttendanceTimestamp object for the particular student
            marking them ABSENT
            '''
            student = Student.objects.get(pk = student_pk)
            AttendanceTimestamp.objects.create(
                student = student,
                subject= subject,
                present  = False,
                timestamp = (lecture_datetime),
            )
            attendtime = AttendanceTimestamp.objects.get(
                student = student,
                subject= subject,
                timestamp = (lecture_datetime),

            )
            attend = Attendance.objects.get(student= student,subject=subject)
            attend.detailed_attendance.add(attendtime)
            attend.total += 1
            attend.not_attended +=1
            attend.save()
        for student in _class_.students.all():
            '''
            looping through the students not in the  list and creating 
            an AttendanceTimestamp object for the particular student
            marking them PRESENT
            '''
            if str(student.pk) not in lists:
                AttendanceTimestamp.objects.create(
                student = student,
                subject= subject,
                    timestamp = (lecture_datetime),
                )
                attendtime = AttendanceTimestamp.objects.get(
                    student = student,
                    subject= subject,
                    timestamp = (lecture_datetime)
                )
                attend = Attendance.objects.get(student= student,subject=subject)
                attend.detailed_attendance.add(attendtime)
                attend.total += 1
                attend.save()
        return redirect('detailed-attendance',pk,subject_pk )

def changeAttendance(self,class_pk,subject_pk,attend_pk):
    '''
    changing a specific attendance with a click from present to absent and vice versa (AttendanceTimestamp)
    '''
    attendanceTime = AttendanceTimestamp.objects.get(pk = attend_pk)
    attendance_history = Attendance.objects.get(detailed_attendance= attendanceTime)
    print(attendance_history)
    if attendanceTime.present:
        attendance_history.not_attended+=1
        attendanceTime.present=False
    else:
        attendanceTime.present=True
        attendance_history.not_attended-=1
    attendance_history.save()
    attendanceTime.save()
    return redirect('detailed-attendance',class_pk,subject_pk,)


class Defaulters(LoginRequiredMixin,View):
    '''
    creates a list(table) of students having attendance less than 75% ( variable in future updates)
    with their details
    '''
    def get(self,request,class_pk,subject_pk,*args,**kwargs):
        class_ = Class.objects.get(pk = class_pk)
        teacher = Teacher.objects.get(user= request.user)
        subject = Subject.objects.get(pk=subject_pk)
        
        if isTeacher(class_,teacher,subject):

            defaulters = []

            for student in class_.students.all():
                attendance  = Attendance.objects.get(student=student,subject=subject)
                if attendance.is_defaulter(): 
                    defaulters.append(attendance)
            context = {
                'class':class_,
                'subject':subject,
                'defaulters':defaulters,
            }
            return render(request,"defaulters.html",context)
        else:
            return redirect('home')
    

class DetailedAttendance(LoginRequiredMixin,View):
    '''
    renders a page based according to specific class with all the details with time and date
    '''
    def get(self,request,class_pk,subject_pk,*args,**kwargs):
        class_ = Class.objects.get(pk=class_pk)
        teacher = Teacher.objects.get(user= request.user)
        subject = Subject.objects.get(pk=subject_pk)
        
        if isTeacher(class_,teacher,subject):
            attendances = []
            for student in class_.students.all():
                attend = Attendance.objects.get(student =student,subject=subject)
                attendances.append(attend)
    
            context = {
                'attendance':attendances,
                'class':class_,
                'subject':subject,
                'last_attendance':attend,

            }
            return render(request,"detailed_atendance.html", context)
        else:
            return redirect('home') #render a error 404 not found template





@login_required 
def export_users_csv(self,class_pk,subject_pk,*args,**kwargs):
    '''
    exports data into CSV of specific class with attendance
    '''
    class_ = Class.objects.get(pk=int(class_pk))
    subject = Subject.objects.get(pk=subject_pk) 
    attendances = []
    for student in class_.students.all():
        attend_ = Attendance.objects.get(student =student,subject=subject)
        attendances.append(attend_)


    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="attendance.csv"'
    writer = csv.writer(response)
    tag = ['first_name','last_name','roll_no']
    for time in attend_.detailed_attendance.all():
        tag.append(time.timestamp.astimezone(pytz.timezone('Asia/Kolkata')))
    writer.writerow(tag)

    attendances = []
    for student in class_.students.all():
        attend = Attendance.objects.get(student =student,subject=subject)
        attendances.append(attend)

    for student in attendances:
        absentees = [student.student.first_name,student.student.last_name,student.student.roll_no]
        for day in student.detailed_attendance.all():
            if day.present:
                absentees.append("P")
            else:
                absentees.append("A")
        writer.writerow(absentees)

    return response




