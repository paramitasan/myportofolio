from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from main.models import Experience, Education


class TestExperience(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="PBP Teaching Assistant",
            description="Help students understand web development.",
            category="part-time",
        )

    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertNotContains(response, self.experience.title)
        self.assertContains(response, f'href="{reverse("main:show_experience")}"')

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/a-page-that-does-not-exist/")

        self.assertEqual(response.status_code, 404)

    def test_experience_model(self):
        self.assertEqual(str(self.experience), "PBP Teaching Assistant")
        self.assertEqual(self.experience.category, "part-time")
        self.assertTrue(self.experience.is_ongoing)

    def test_experience_page(self):
        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertContains(response, self.experience.title)
        self.assertContains(response, self.experience.description)
        self.assertContains(response, "Part-Time")
        self.assertContains(response, "Ongoing")
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))

        self.assertContains(response, "No experience has been added yet.")

    def test_completed_experience(self):
        self.experience.ended_at = timezone.now()
        self.experience.save()
        response = self.client.get(reverse("main:show_experience"))

        self.assertFalse(self.experience.is_ongoing)
        self.assertContains(response, "Completed")
        self.assertNotContains(response, "Ongoing")

class TestEducation(TestCase):
    def setUp(self):
        # Assume present is 2033
        self.education = Education.objects.create(
            institution_name="MIT",
            starting_year="2029",
            end_year="2032",
            description="Activities and societies: member of MIT Code for Good," \
            " programming course teaching assistant"
        )

    # url is accessible, uses correct template
    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))
    
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertNotContains(response, self.education.institution_name)
        self.assertContains(response, f'href="{reverse("main:show_education")}"')
    
    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/a-page-that-does-not-exist/")

        self.assertEqual(response.status_code, 404)

    def test_education_model(self):
        self.assertEqual(self.education.institution_name, "MIT")
        self.assertIn("Code for Good", self.education.description)
        self.assertTrue(self.education.starting_year, "2029")
        self.assertTrue(self.education.end_year, "2032")

    # correct template used, model data appears
    def test_education_page(self):
        response = self.client.get(reverse("main:show_education"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "education.html")
        self.assertContains(response, self.education.institution_name)
        self.assertContains(response, self.education.description)
        self.assertContains(response, self.education.starting_year)
        self.assertContains(response, self.education.end_year)
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    # empty message appears
    def test_empty_education_page(self):
        Education.objects.all().delete()
        response = self.client.get(reverse("main:show_education"))

        self.assertContains(response, "No education has been added yet.")

    def test_present_education(self):
        Education.objects.all().delete()
        self.education = Education.objects.create(
            institution_name="NTU",
            starting_year="2030",
            description="Activities and societies: member of Marvel Club @ EEE"
        )
        response = self.client.get(reverse("main:show_education"))
        self.assertContains(response, "Present")