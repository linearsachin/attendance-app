from django.shortcuts import render
from django.views.generic import View
from .models import Teacher , Class,Attendance,Student_Attendance,Teacher_Detail,Subject
# Create your views here.
class HomeView(View):
    def get(self,request,*args,**kwargs):
        try : 
            teacher = Teacher.objects.get(user= request.user)
            
        except:
            teacher = None
        teacher_dets =  Teacher_Detail.objects.filter(teacher=teacher)
        print(teacher_dets)
        context = {
            'teacher' : teacher,
            'detail': teacher_dets,
        }
        return render(request , "home.html", context)


class ClassView(View):
    def get(self,request,pk,subject_pk,*args,**kwargs):
        # try:
        class_ = Class.objects.get(pk= pk)
        teacher = Teacher.objects.get(user= request.user)

        student_attendance = Student_Attendance.objects.filter(class_s = class_)
        subject_check = Subject.objects.get(pk = subject_pk)
        for attendance in student_attendance.attendance.all():
            if attendance.subject == subject_check:
                attendance_   = attendance
        print(attendance_)
        context = {
            'attendances':student_attendance,
            'class':class_
        }
        return render(request , "indiv_class.html", context)
        



# class AttendanceView(View):
#     def get(self,request,pk,*args,**kwargs):
#         try:
#             class_ = Class.objects.get(pk= pk)
#         except:
#             class_= None
#         context = {
#             'class':class_
#         }
#         return render(request , "indiv_class.html", context)