from django.shortcuts import render
from main.models import Experience

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