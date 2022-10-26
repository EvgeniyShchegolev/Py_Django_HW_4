from django.views.generic import ListView
from django.shortcuts import render
from django.db.models import prefetch_related_objects

from .models import Student


def students_list(request):

    template = 'school/students_list.html'
    students = Student.objects.all()
    prefetch_related_objects(students, 'teachers')
    context = {'object_list': students}

    return render(request, template, context)
