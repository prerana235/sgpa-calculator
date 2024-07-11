from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.utils.datastructures import MultiValueDictKeyError
from .models import Scheme, Branch, Sem, Subject

def welcome(request):
    return render(request, 'welcome.html')

def calculate(request):
    schemes = Scheme.objects.all()
    branches = Branch.objects.all()
    semesters = Sem.objects.all()

    context = {
        'schemes': schemes,
        'branches': branches,
        'semesters': semesters,
    }
    
    return render(request, 'calculate.html', context)

def fetch_subjects(request):
    scheme_id = request.GET.get('scheme')
    branch_id = request.GET.get('branch')
    semester_id = request.GET.get('semester')

    try:
        subjects = Subject.objects.filter(
            sem__branch__scheme_id=scheme_id,
            sem__branch_id=branch_id,
            sem_id=semester_id
        )
        subjects_data = [
            {
                'course_id': subject.sub_id,
                'title': subject.sub_name,
                'credits': subject.credits,
                'max_marks': subject.max_marks
            }
            for subject in subjects
        ]
        return JsonResponse(subjects_data, safe=False)
    except Subject.DoesNotExist:
        return JsonResponse([], safe=False)

def add(request):
    sgpa = None
    if request.method == "POST":
        total_credits = 0
        total_points = 0
        num_subjects = int(request.POST.get('numSubjects', 0))  # Get the number of subjects from the form

        for i in range(1, num_subjects + 1):
            marks = int(request.POST.get(f'marks{i}', 0))
            credits = int(request.POST.get(f'credits{i}', 0))
            grade_point = convert_marks_to_grade_point(marks)
            total_points += grade_point * credits
            total_credits += credits

        if total_credits > 0:
            sgpa = total_points / total_credits

    return render(request, "add.html", {'sgpa': sgpa})
def convert_marks_to_grade_point(marks):
    if marks >= 90:
        return 10
    elif marks >= 80:
        return 9
    elif marks >= 70:
        return 8
    elif marks >= 60:
        return 7
    elif marks >= 50:
        return 6
    elif marks >= 40:
        return 5
    else:
        return 0

def cgpa(request):
    return render(request, 'cgpa.html')
