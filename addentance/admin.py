from django.contrib import admin

# Register your models here.
from .models import ( Branch,
Subject,
Attendance,
Student,
Class,
Teacher,
Student_Attendance,
Teacher_Detail,
AttendanceTimestamp,
)


class AttendanceAdmin(admin.ModelAdmin):

    list_display = ('student','subject','not_attended','total')
    list_filter = ['student']
    actions = ['set_total_0', ]

    def set_total_0(self, request, queryset):
        queryset.update(total=0,not_attended = 0)

class TeacherAdmin(admin.ModelAdmin):
    list_display = ('teacher','subject',)
    actions = ['create_attendance', ]
    def create_attendance(self,request,queryset):
        for teacher in queryset:
            for class_ in teacher.classes.all():
                for student in class_.students.all():
                    Attendance.objects.create(
                        student=student,
                        subject=teacher.subject,
                    )
                    attendance =Attendance.objects.get(student=student,subject=teacher.subject)
                    student_attend = Student_Attendance.objects.get(student=student)
                    student_attend.attendance.add(attendance)
                    student_attend.save()



admin.site.register(Branch)
admin.site.register(Subject)
admin.site.register(Attendance,AttendanceAdmin)
admin.site.register(Student)
admin.site.register(Class)
admin.site.register(Teacher)
admin.site.register(Student_Attendance)
admin.site.register(Teacher_Detail,TeacherAdmin)
admin.site.register(AttendanceTimestamp)