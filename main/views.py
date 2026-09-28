from django.shortcuts import get_object_or_404, redirect, render
from main.models import Experience, Education
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core import serializers
from django.http import HttpResponse
from main.forms import ExperienceForm, EducationForm
from portofolio import settings
import datetime

def show_main(request):
    last_login = request.COOKIES.get('last_login', 'No active login session / Cookie not found')
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
        "last_login": last_login,
    }
    return render(request, "index.html", context)


# experience
def get_experience_json(request):
    exp = Experience.objects.all()
    title_query = request.GET.get("title", "").strip()

    if title_query:
        exp = exp.filter(title__icontains=title_query)

    exp_json = serializers.serialize("json", exp, use_natural_foreign_keys=True)
    return HttpResponse(exp_json, content_type="application/json")

def show_experience(request):
    json_response = get_experience_json(request)
    
    experience = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    experience = [exp.object for exp in experience]
    title_query = request.GET.get("title", "").strip()
    
    context = {
        "name": "Paramita",
        "experience_list": experience,
        "title_query": title_query,
        }
    return render(request, "experience.html", context)

@login_required(login_url="/login/")
def create_experience(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    
    form = ExperienceForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Experience has successfully been added!")
            return redirect("main:show_experience")

    context = {
        "name": "Paramita",
        "form": form,
        "is_edit": False,  #To differentiate between [create] & edit
    }
    return render(request, "experience_form.html", context)

@login_required(login_url="/login/")
def edit_experience(request, exp_id):
    if not request.user.is_superuser:
        raise PermissionDenied

    exp = get_object_or_404(Experience, pk=exp_id)
    form = ExperienceForm(request.POST or None, instance=exp)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Experience has successfully been updated!")
            return redirect("main:show_experience")

    context = {
        "name": "Paramita",
        "form": form,
        "is_edit": True,  # To differentiate between create & [edit]
    }
    return render(request, "experience_form.html", context)

@login_required(login_url="/login/")
def delete_experience(request, exp_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    
    exp = get_object_or_404(Experience, pk=exp_id)

    if request.method == "POST":
        exp.delete()
        messages.success(request, "Experience has successfully been deleted.")

    return redirect("main:show_experience")

@login_required(login_url="/login/")
def toggle_star_experience(request, exp_id):
    exp = get_object_or_404(Experience, pk=exp_id)

    if request.method == "POST":
        if request.user in exp.starred_by.all():
            exp.starred_by.remove(request.user)
        else:
            exp.starred_by.add(request.user)

    return redirect("main:show_experience")


# education
def get_education_json(request):
    edu = Education.objects.all()
    institution_name_query = request.GET.get("institution_name", "").strip()

    if institution_name_query:
        edu = edu.filter(institution_name__icontains=institution_name_query)

    edu_json = serializers.serialize("json", edu)
    return HttpResponse(edu_json, content_type="application/json")

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

@login_required(login_url="/login/")
def create_education(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    
    form = EducationForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Education record has successfully been added!")
            return redirect("main:show_education")

    context = {
        "name": "Paramita",
        "form": form,
        "is_edit": False,  #To differentiate between [create] & edit
    }
    return render(request, "education_form.html", context)

@login_required(login_url="/login/")
def edit_education(request, edu_id):
    if not request.user.is_superuser:
        raise PermissionDenied

    edu = get_object_or_404(Education, pk=edu_id)
    form = EducationForm(request.POST or None, instance=edu)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Education record has successfully been updated!")
            return redirect("main:show_education")

    context = {
        "name": "Paramita",
        "form": form,
        "is_edit": True,  # To differentiate between create & [edit]
    }
    return render(request, "education_form.html", context)

@login_required(login_url="/login/")
def delete_education(request, edu_id):
    if not request.user.is_superuser:
        raise PermissionDenied

    edu = get_object_or_404(Education, pk=edu_id)

    if request.method == "POST":
        edu.delete()
        messages.success(request, "Education record has successfully been deleted.")

    return redirect("main:show_education")


# Authentication, session, cookies
def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Account created successfully. Please log in.")
        return redirect("main:login")

    context = {
        "name": "Paramita",
        "form": form,
    }
    return render(request, "register.html", context)

def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        response = redirect("main:show_main")
        response.set_cookie('last_login', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return response

    context = {
        "name": "Paramita",
        "form": form,
    }
    return render(request, "login.html", context)

def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie('last_login')
    return response