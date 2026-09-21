from django import forms
from django.forms import ModelForm
from main.models import Education, Experience

class EducationForm(ModelForm):
    class Meta:
        model = Education
        fields = [
            "institution_name",
            "starting_year",
            "end_year",
            "description",
        ]

        labels = {
            "institution_name": "Institution Name",
            "starting_year": "Education Starting Year",
            "end_year": "Education End Year",
            "description": "Activities and Societies",
        }

        widgets = {
            "institution_name": forms.TextInput(
                attrs={
                    "placeholder": "Institution name, e.g. Universitas Indonesia", #hint text
                    "maxlength": 255,
                }
            ),
            "starting_year": forms.TextInput(
                attrs={
                    "placeholder": "Starting year, e.g. 2026",
                    "maxlength": 4,
                }
            ),
            "end_year": forms.TextInput(
                attrs={
                    "placeholder": "End year (leave it blank if ongoing)",
                    "maxlength": 4,
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "placeholder": "Describe the activities done in this institution!",
                    "rows": 4,
                }
            ),
        }

class ExperienceForm(ModelForm):
    class Meta:
        model = Experience
        fields = [
            "title",
            "description",
            "category",
            "thumbnail",
            "started_at",
            "ended_at",
        ]

        labels = {
            "title": "Job Title",
            "description": "What You Did",
            "category": "Employment Type",
            "thumbnail": "Thumbnail link",
            "started_at": "Start Date",
            "ended_at": "End Date",
        }

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "placeholder": "Example: Teaching Assistant",
                    "maxlength": 255,
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "placeholder": "Describe the activities you've done in this institution!",
                    "rows": 4,
                }
            ),
            "category": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "thumbnail": forms.URLInput(
                attrs={
                    "placeholder": "Example: https://drive.google.com/...",
                }
            ),
            "started_at": forms.DateInput(
                attrs={
                    "type": "date",
                }
            ),
            "ended_at": forms.DateInput(
                attrs={
                    "type": "date",
                }
            ),            
        }