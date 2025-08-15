# University Portal

Django application for managing students, teachers and courses.

## Installation

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Admin

Create superuser:

```bash
python manage.py createsuperuser
```

Then open `/admin/` to manage data.

## ORM examples

```python
from core.models import Student, Course, Enrollment
from django.db.models import Avg

# students of year 2023
Student.objects.filter(group__startswith="2023")

# courses without students
Course.objects.filter(enrollments__isnull=True)

# average grade for a student
Enrollment.objects.filter(student=some_student).aggregate(avg=Avg('grade'))
```
