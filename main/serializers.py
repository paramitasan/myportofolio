from django.utils.html import strip_tags
from rest_framework import serializers

from main.models import Experience, Education


class ExperienceSerializer(serializers.ModelSerializer):
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    starred_by_names = serializers.SerializerMethodField()
    is_ongoing = serializers.BooleanField(read_only=True)

    class Meta:
        model = Experience
        fields = [
            "id", "title", "description", "category",
            "thumbnail", "started_at", "ended_at", "is_ongoing",
            "star_count", "is_starred", "starred_by_names",
        ]
        read_only_fields = ["id", "is_ongoing"]

    def validate_title(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Title can't be empty.")
        return value

    def validate_description(self, value):
        return strip_tags(value).strip()

    def validate(self, attrs):
        started = attrs.get("started_at", getattr(self.instance, "started_at", None))
        ended = attrs.get("ended_at", getattr(self.instance, "ended_at", None))
        if started and ended and ended <= started:
            raise serializers.ValidationError(
                {"ended_at": "End date must be after the start date."}
            )
        return attrs

    def get_star_count(self, obj):
        return obj.starred_by.count()

    def get_is_starred(self, obj):
        request = self.context.get("request")
        if request is None or not request.user.is_authenticated:
            return False
        return request.user in obj.starred_by.all()

    def get_starred_by_names(self, obj):
        return ", ".join(user.username for user in obj.starred_by.all())


class EducationSerializer(serializers.ModelSerializer):
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    starred_by_names = serializers.SerializerMethodField()

    class Meta:
        model = Education
        fields = [
            "id", "institution_name",
            "starting_year", "end_year", "description",
            "star_count", "is_starred", "starred_by_names",
        ]
        read_only_fields = ["id"]

    def validate_institution_name(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Institution name can't be empty.")
        return value

    def validate_description(self, value):
        return strip_tags(value).strip()

    def validate(self, attrs):
        start = attrs.get("starting_year", getattr(self.instance, "starting_year", None))
        end = attrs.get("end_year", getattr(self.instance, "end_year", None))
        if start and end and end < start:
            raise serializers.ValidationError(
                {"end_year": "End year can't be before the starting year."}
            )
        return attrs
    
    def get_star_count(self, obj):
        return obj.starred_by.count()
    
    def get_is_starred(self, obj):
        request = self.context.get("request")
        if request is None or not request.user.is_authenticated:
            return False
        return request.user in obj.starred_by.all()
    
    def get_starred_by_names(self, obj):
        return ", ".join(user.username for user in obj.starred_by.all())