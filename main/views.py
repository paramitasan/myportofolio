from django.shortcuts import render
from main.models import Experience
from main.models import Education

def show_main(request):
    context = {
        "name": "Paramita",
        "nickname": "Mita",
        "full_name": "Paramita Santoso",
        "npm": "2506554171",
        "study_program": "S1 Ilmu Komputer KKI",
        "bio": (
            "Hello, I'm Mita! I'm a curious and motivated CS student, "
            "eager to explore the tech world. "
            "Currenly diving into cyber security and data science."
        ),
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Paramita",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)

def show_education(request):
    context = {
        "name": "Paramita",
        "education_list": Education.objects.all(),
    }
    return render(request, "education.html", context)