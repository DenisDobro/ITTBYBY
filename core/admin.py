from django.contrib import admin
from .models import Student, Teacher, Course, Enrollment


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email", "group")
    search_fields = ("first_name", "last_name", "email", "group")
    list_filter = ("group",)


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "position", "email")
    search_fields = ("first_name", "last_name", "email")


class EnrollmentInline(admin.TabularInline):
    model = Enrollment
    extra = 1


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("name", "teacher", "start_date", "end_date")
    search_fields = ("name", "teacher__first_name", "teacher__last_name")
    list_filter = ("teacher",)
    inlines = [EnrollmentInline]


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("student", "course", "enrolled_at", "grade")
    search_fields = ("student__first_name", "student__last_name", "course__name")
    list_filter = ("course", "student")
