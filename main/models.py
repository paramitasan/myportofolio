import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

def validate_date_min_year(value):
    if value.year < 2010:
        raise ValidationError("Ensure year is greater than or equal to 2010.")

class Experience(models.Model):
    EXPERIENCE_CHOICES = [
        ("internship", "Internship"),
        ("research", "Research"),
        ("volunteer", "Volunteer"),
        ("part-time", "Part-Time"),
        ("full-time", "Full-Time"),
        ("freelance", "Freelance"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, default='')
    description = models.TextField(max_length=100, default="")
    category = models.CharField(
        max_length=20,
        choices=EXPERIENCE_CHOICES,
        default="full-time",
    )
    thumbnail = models.URLField(blank=True, null=True)
    started_at = models.DateTimeField(validators=[validate_date_min_year])
    ended_at = models.DateTimeField(
        blank=True, null=True, validators=[validate_date_min_year]
    )
    starred_by = models.ManyToManyField(
        User, related_name="starred_experience", blank=True
    )

    def __str__(self):
        return self.title

    def clean(self):
        super().clean()
        if self.started_at and self.ended_at and self.ended_at < self.started_at:
            raise ValidationError({"ended_at": "End date can't be before the start date."})

    @property
    def is_ongoing(self):
        return self.ended_at is None

class Education(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    institution_name = models.CharField(max_length=255)
    starting_year = models.PositiveIntegerField(
        validators=[MinValueValidator(2010),MaxValueValidator(2100)]
    )
    end_year = models.PositiveIntegerField(
        blank=True, null=True,
        validators=[MinValueValidator(2010),MaxValueValidator(2100)]
    )
    description = models.TextField(max_length=400, default="")
    starred_by = models.ManyToManyField(
        User, related_name="starred_education", blank=True
    )

    def clean(self):
        super().clean()
        if self.starting_year and self.end_year and self.end_year < self.starting_year:
            raise ValidationError({"end_year": "End year can't be before the starting year."})