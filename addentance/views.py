from django.shortcuts import render,redirect
from django.views.generic import View
import datetime
from django.utils import timezone
import pytz
import csv
from django.http import HttpResponse


from .models import Teacher , Class,Attendance,Student_Attendance,Teacher_Detail,Subject,Student,AttendanceTimestamp
# Create your views here.
class HomeView(View):
    def get(self,request,*args,**kwargs):
        try : 
            teacher = Teacher.objects.get(user= request.user)
            
        except:
            teacher = None
        teacher_dets =  Teacher_Detail.objects.filter(teacher=teacher)

        context = {
            'teacher' : teacher,
            'detail': teacher_dets,
        }
        return render(request , "home.html", context)


class ClassView(View):
    def get(self,request,pk,subject_pk,*args,**kwargs):

        class_ = Class.objects.get(pk= pk)
        teacher = Teacher.objects.get(user= request.user)
        subject = Subject.objects.get(pk=subject_pk)
        try:
            teacher_dets  = Teacher_Detail.objects.get(teacher=teacher, subject=subject)

        except:
            teacher_dets = None
        
        if teacher_dets is not None:
            for class__ in teacher_dets.classes.all():
                if class_==class__:
                    class_= class__
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
        

class MarkAttendanceView(View):
    def get(self,request,pk,subject_pk,*args,**kwargs):
        class_ = Class.objects.get(pk= pk)
        teacher = Teacher.objects.get(user= request.user)
        subject = Subject.objects.get(pk=subject_pk)
        try:
            teacher_dets  = Teacher_Detail.objects.get(teacher=teacher, subject=subject)

        except:
            teacher_dets = None
        
        if teacher_dets is not None:
            for class__ in teacher_dets.classes.all():
                if class_==class__:
                    class_= class__
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
        _class_ =  Class.objects.get(pk = pk)
        lists=request.POST.getlist('attendance-absent-set')
        lecture_date = request.POST.get('lecture-date')
        lecture_time = request.POST.get('lecture-time')
        lecture_datetime1 = lecture_date + ' '+ lecture_time
        lecture_datetime=datetime.datetime.strptime(lecture_datetime1,'%Y-%m-%d %H:%M').astimezone(pytz.timezone('Asia/Kolkata'))
        print(type(lecture_datetime))
        subject = Subject.objects.get(pk=subject_pk)
        for student_pk in lists:
            student = Student.objects.get(pk = student_pk)
            AttendanceTimestamp.objects.create(
                student = student,
                subject= subject,
                present  = False,
                timestamp = (lecture_datetime),
            )
            attendtime = AttendanceTimestamp.objects.filter(
                student = student,
                subject= subject,
                present  = False,
            ).order_by('-timestamp')[0]
            attend = Attendance.objects.get(student= student,subject=subject)
            attend.detailed_attendance.add(attendtime)
            attend.total += 1
            attend.not_attended +=1
            attend.save()
        for student in _class_.students.all():
            if str(student.pk) not in lists:
                AttendanceTimestamp.objects.create(
                student = student,
                subject= subject,
                present  = True,
                timestamp = (lecture_datetime),
                )
                attendtime = AttendanceTimestamp.objects.filter(
                student = student,
                subject= subject,
                present  = True,
                ).order_by('-timestamp')
                attend = Attendance.objects.get(student= student,subject=subject)
                attend.detailed_attendance.add(attendtime[0])
                attend.total += 1
                attend.save()

        
            
        return redirect('home')
 

class DetailedAttendance(View):
    def get(self,request,class_pk,subject_pk,*args,**kwargs):
        class_ = Class.objects.get(pk=class_pk)
        subject = Subject.objects.get(pk=subject_pk) 
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






def export_users_csv(self,class_pk,subject_pk,*args,**kwargs):
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
        tag.append(time.timestamp)
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






    


    # students = Student.objects.all().values_list('first_name','last_name','roll_no')
    # for student in students:
    #     writer.writerow(student)

    return response