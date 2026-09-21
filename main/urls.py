from django.urls import path

from main.views import show_main
from main.views import show_experience, create_experience, get_experience_json, delete_experience, edit_experience
from main.views import show_education, create_education, get_education_json, delete_education, edit_education

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),

    path("experience/", show_experience, name="show_experience"),
    path("experience/add/", create_experience, name="create_experience"),
    path("api/experience/", get_experience_json, name="get_experience_json"),
    path("experience/<uuid:exp_id>/delete/", delete_experience, name="delete_experience"),
    path("experience/<uuid:exp_id>/edit/", edit_experience, name="edit_experience"),

    path("education/", show_education, name="show_education"),
    path("education/add/", create_education, name="create_education"),
    path("api/education/", get_education_json, name="get_education_json"),
    path("education/<uuid:edu_id>/delete/", delete_education, name="delete_education"),
    path("education/<uuid:edu_id>/edit/", edit_education, name="edit_education"),

    # path("projects/", show_projects, name="show_projects"),
]