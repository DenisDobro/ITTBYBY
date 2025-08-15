from django.db.models import Count, Avg
from django.shortcuts import render, get_object_or_404, redirect
from .models import Student, Teacher, Course, Enrollment
from .forms import EnrollmentForm


def index(request):
    courses = Course.objects.annotate(student_count=Count('enrollments'))
    courses_without_students = Course.objects.filter(enrollments__isnull=True)
    stats = {
        'total_students': Student.objects.count(),
        'avg_courses_per_student': Enrollment.objects.values('student').annotate(c=Count('id')).aggregate(avg=Avg('c'))['avg'],
    }
    return render(request, 'core/index.html', {
        'courses': courses,
        'courses_without_students': courses_without_students,
        'stats': stats,
    })


def student_list(request):
    year = request.GET.get('year')
    students = Student.objects.all()
    if year:
        students = students.filter(group__startswith=str(year))
    return render(request, 'core/student_list.html', {
        'students': students,
        'year': year,
    })


def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    enrollments = student.enrollments.select_related('course')
    avg_grade = enrollments.aggregate(avg=Avg('grade'))['avg']
    return render(request, 'core/student_detail.html', {
        'student': student,
        'enrollments': enrollments,
        'avg_grade': avg_grade,
    })


def course_list(request):
    courses = Course.objects.all()
    teacher_id = request.GET.get('teacher')
    start = request.GET.get('start')
    end = request.GET.get('end')
    if teacher_id:
        courses = courses.filter(teacher_id=teacher_id)
    if start:
        courses = courses.filter(start_date__gte=start)
    if end:
        courses = courses.filter(end_date__lte=end)
    return render(request, 'core/course_list.html', {
        'courses': courses,
    })


def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    students = Student.objects.filter(enrollments__course=course)
    return render(request, 'core/course_detail.html', {
        'course': course,
        'students': students,
    })


def enroll(request):
    if request.method == 'POST':
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = EnrollmentForm()
    return render(request, 'core/enroll_form.html', {'form': form})
