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
)
admin.site.register(Branch)
admin.site.register(Subject)
admin.site.register(Attendance)
admin.site.register(Student)
admin.site.register(Class)
admin.site.register(Teacher)
admin.site.register(Student_Attendance)
admin.site.register(Teacher_Detail)