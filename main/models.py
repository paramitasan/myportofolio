import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

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
    started_at = models.DateTimeField(blank=True, null=True)
    ended_at = models.DateTimeField(blank=True, null=True)
    starred_by = models.ManyToManyField(
        User, related_name="starred_experience", blank=True
    )

    def __str__(self):
        return self.title

    @property
    def is_ongoing(self):
        return self.ended_at is None

class Education(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    institution_name = models.CharField(max_length=255)
    starting_year = models.PositiveIntegerField(
        blank=True, null=True,
        validators=[MinValueValidator(2010),MaxValueValidator(2100)]
    )
    end_year = models.PositiveIntegerField(
        blank=True, null=True,
        validators=[MinValueValidator(2010),MaxValueValidator(2100)]
    )
    description = models.TextField(max_length=400, default="")