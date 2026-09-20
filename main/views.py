from django.shortcuts import get_object_or_404, redirect, render
from main.models import Experience, Education
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from main.forms import EducationForm
from portofolio import settings

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
    json_response = get_education_json(request)

    education = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    education = [edu.object for edu in education]
    institution_name_query = request.GET.get("institution_name", "").strip()

    context = {
        "name": "Paramita",
        "education_list": education,
        "institution_name_query": institution_name_query,
    }
    return render(request, "education.html", context)

def create_education(request):
    form = EducationForm(request.POST or None)

    if request.method == "POST":
        user_passcode = request.POST.get("passcode", "")
        if user_passcode != settings.SECRET_PASSCODE:
            messages.error(request, "Incorrect passcode: no authority to add education records.")
            context = {
                "name": "Paramita",
                "form": form,
            }
            return render(request, "education_form.html", context)

        if form.is_valid():
            form.save()
            messages.success(request, "Education record has successfully been added!")
            return redirect("main:show_education")

    context = {
        "name": "Paramita",
        "form": form,
    }
    return render(request, "education_form.html", context)

def get_education_json(request):
    edu = Education.objects.all()
    institution_name_query = request.GET.get("institution_name", "").strip()

    if institution_name_query:
        edu = edu.filter(institution_name__icontains=institution_name_query)

    edu_json = serializers.serialize("json", edu)
    return HttpResponse(edu_json, content_type="application/json")

def delete_education(request, edu_id):
    edu = get_object_or_404(Education, pk=edu_id)

    if request.method == "POST":
        user_passcode = request.POST.get("passcode", "")
        if user_passcode == settings.SECRET_PASSCODE:
            edu.delete()
            messages.success(request, "Education record has successfully been deleted.")
        else:
            messages.error(request, "Incorrect passcode: no authority to delete education records.")
        return redirect("main:show_education")

    return redirect("main:show_education")