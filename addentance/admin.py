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

    list_display = ('student','not_attended','total')
    actions = ['set_total_0', ]

    def set_total_0(self, request, queryset):
        queryset.update(total=0,not_attended = 0)


admin.site.register(Branch)
admin.site.register(Subject)
admin.site.register(Attendance,AttendanceAdmin)
admin.site.register(Student)
admin.site.register(Class)
admin.site.register(Teacher)
admin.site.register(Student_Attendance)
admin.site.register(Teacher_Detail)
admin.site.register(AttendanceTimestamp)