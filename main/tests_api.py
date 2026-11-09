import uuid

from django.contrib.auth.models import Group, User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from main.models import Experience, Education


class ExperienceAPITest(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser(
            username="owner", password="test-password", email="owner@example.com",
        )
        self.visitor = User.objects.create_user(username="visitor", password="test-password")
        self.experience = Experience.objects.create(
            title="Backend Intern",
            description="Developed REST APIs",
            category="internship",
            started_at="2024-01-15T09:00:00Z",
        )
        self.list_url = reverse("api:experience-list")
        self.detail_url = reverse("api:experience-detail", args=[self.experience.id])
        self.star_url = reverse("api:experience-star", args=[self.experience.id])
        self.payload = {
            "title": "Software Engineer",
            "description": "Full-stack development",
            "category": "full-time",
            "thumbnail": "https://example.com/image.png",
            "started_at": "2024-01-15T09:00:00Z",
            "ended_at": "2024-12-31T18:00:00Z",
        }

    def test_public_list_and_detail(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["id"], str(self.experience.id))
        self.assertFalse(response.data[0]["is_starred"])
        self.assertNotIn("fields", response.data[0])
        self.assertEqual(self.client.get(self.detail_url).status_code, status.HTTP_200_OK)

    def test_search_and_empty_results(self):
        response = self.client.get(self.list_url, {"title": "Back"})
        self.assertEqual(len(response.data), 1)
        response = self.client.get(self.list_url, {"title": "not-found"})
        self.assertEqual(response.data, [])

    def test_missing_experience(self):
        url = reverse("api:experience-detail", args=[uuid.uuid4()])
        self.assertEqual(self.client.get(url).status_code, status.HTTP_404_NOT_FOUND)

    def test_guest_and_visitor_cannot_write(self):
        for user in (None, self.visitor):
            self.client.force_authenticate(user=user)
            self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, 403)
            self.assertEqual(self.client.patch(self.detail_url, {"title": "Changed"}, format="json").status_code, 403)
            self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
        self.assertEqual(Experience.objects.count(), 1)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Backend Intern")

    def test_owner_can_create(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Experience.objects.filter(pk=response.data["id"]).exists())

    def test_validation(self):
        self.client.force_authenticate(user=self.owner)
        for changes, field in [
            ({"title": "   "}, "title"),
            ({"title": '<img src="x" onerror="alert(1)">'}, "title"),
            ({"thumbnail": "not-a-valid-url"}, "thumbnail"),
        ]:
            response = self.client.post(self.list_url, {**self.payload, **changes}, format="json")
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn(field, response.data)
        self.assertEqual(Experience.objects.count(), 1)

    def test_patch_put_and_delete(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.patch(self.detail_url, {"title": "Changed"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.description, "Developed REST APIs")
        response = self.client.put(self.detail_url, {"title": "Incomplete"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.put(self.detail_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.content, b"")
        self.assertFalse(Experience.objects.filter(pk=self.experience.id).exists())

    def test_star_requires_login_and_toggles(self):
        self.assertEqual(self.client.post(self.star_url).status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.visitor)
        response = self.client.post(self.star_url)
        self.assertTrue(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 1)
        response = self.client.post(self.star_url)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 0)

    def test_computed_fields_are_read_only(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, {
            **self.payload, "star_count": 99, "is_starred": True,
            "starred_by_names": "forged", "starred_by": [self.visitor.id],
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(response.data["is_starred"])

    def test_staff_and_editor_cannot_manage_experiences(self):
        self.visitor.is_staff = True
        self.visitor.save()
        self.visitor.groups.add(Group.objects.create(name="Editor"))
        self.client.force_authenticate(user=self.visitor)
        response = self.client.patch(self.detail_url, {"title": "Changed"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_wrong_method(self):
        self.client.force_authenticate(user=self.owner)
        self.assertEqual(self.client.delete(self.list_url).status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_session_write_without_csrf_is_rejected(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username="owner", password="test-password"))
        response = client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Experience.objects.count(), 1)

    def test_session_write_with_csrf_succeeds(self):
        client = APIClient(enforce_csrf_checks=True)
        client.login(username="owner", password="test-password")
        page = client.get(self.list_url, HTTP_ACCEPT="text/html")
        self.assertEqual(page.status_code, status.HTTP_200_OK)
        token = client.cookies["csrftoken"].value
        response = client.post(
            self.list_url, self.payload, format="json", HTTP_X_CSRFTOKEN=token,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class EducationAPITests(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser("owner", password="pass12345")
        self.editor = User.objects.create_user("editor", password="pass12345")
        self.editor.groups.add(Group.objects.create(name="Editor"))
        self.regular = User.objects.create_user("regular", password="pass12345")

        self.record = Education.objects.create(
            institution_name="Universitas Indonesia",
            starting_year=2025,
            description="Original",
        )
        self.list_url = reverse("api:education-list")
        self.detail_url = reverse("api:education-detail", args=[self.record.id])
        self.star_url = reverse("api:education-star", args=[self.record.id])
        self.valid = {
            "institution_name": "ITB",
            "starting_year": 2020,
            "end_year": 2024,
            "description": "Robotics club",
        }

    # ---------- helpers ----------
    def assert_all_writes_rejected(self):
        self.assertEqual(self.client.post(self.list_url, self.valid, format="json").status_code, 403)
        self.assertEqual(
            self.client.patch(self.detail_url, {"description": "Hacked"}, format="json").status_code, 403)
        self.assertEqual(
            self.client.put(self.detail_url, self.valid, format="json").status_code, 403)
        self.assertEqual(self.client.delete(self.detail_url).status_code, 403)

        self.assertEqual(Education.objects.count(), 1)
        self.record.refresh_from_db()
        self.assertEqual(self.record.description, "Original")
        self.assertEqual(self.record.institution_name, "Universitas Indonesia")

    # ---------- visitor ----------
    def test_visitor_can_read_list_and_detail(self):
        self.assertEqual(self.client.get(self.list_url).status_code, 200)
        self.assertEqual(self.client.get(self.detail_url).status_code, 200)

    def test_visitor_cannot_write(self):
        self.assert_all_writes_rejected()

    # ---------- regular user ----------
    def test_regular_user_cannot_write(self):
        self.client.force_authenticate(self.regular)
        self.assert_all_writes_rejected()

    # ---------- editor ----------
    def test_editor_can_patch_but_not_create_or_delete(self):
        self.client.force_authenticate(self.editor)

        response = self.client.patch(self.detail_url, {"description": "Edited"}, format="json")
        self.assertEqual(response.status_code, 200)
        self.record.refresh_from_db()
        self.assertEqual(self.record.description, "Edited")

        self.assertEqual(self.client.post(self.list_url, self.valid, format="json").status_code, 403)
        self.assertEqual(Education.objects.count(), 1)

        self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
        self.assertTrue(Education.objects.filter(pk=self.record.pk).exists())

    # ---------- owner ----------
    def test_owner_can_create_update_and_delete(self):
        self.client.force_authenticate(self.owner)

        response = self.client.post(self.list_url, self.valid, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Education.objects.count(), 2)

        response = self.client.put(self.detail_url, self.valid, format="json")
        self.assertEqual(response.status_code, 200)
        self.record.refresh_from_db()
        self.assertEqual(self.record.institution_name, "ITB")

        self.assertEqual(self.client.delete(self.detail_url).status_code, 204)
        self.assertFalse(Education.objects.filter(pk=self.record.pk).exists())

    def test_missing_record_returns_404(self):
        url = reverse("api:education-detail", args=[uuid.uuid4()])
        self.assertEqual(self.client.get(url).status_code, 404)

    # ---------- validation ----------
    def test_year_below_2010_is_rejected(self):
        self.client.force_authenticate(self.owner)
        data = {**self.valid, "starting_year": 2009}
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("starting_year", response.data)
        self.assertEqual(Education.objects.count(), 1)

    def test_end_year_before_start_year_is_rejected(self):
        self.client.force_authenticate(self.owner)
        data = {**self.valid, "starting_year": 2024, "end_year": 2020}
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Education.objects.count(), 1)

    def test_end_year_is_optional(self):
        self.client.force_authenticate(self.owner)
        data = {**self.valid, "end_year": None}
        self.assertEqual(self.client.post(self.list_url, data, format="json").status_code, 201)

    def test_html_is_stripped_from_text(self):
        self.client.force_authenticate(self.owner)
        data = {**self.valid,
                "institution_name": "<b>ITB</b>",
                "description": "<script>alert(1)</script>Club"}
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, 201)
        saved = Education.objects.get(pk=response.data["id"])
        self.assertEqual(saved.institution_name, "ITB")
        self.assertNotIn("<", saved.description)

    def test_name_with_only_html_is_rejected(self):
        self.client.force_authenticate(self.owner)
        data = {**self.valid, "institution_name": "<b></b>"}
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Education.objects.count(), 1)

    # ---------- search ----------
    def test_search_filters_by_institution_name(self):
        Education.objects.create(institution_name="ITB", starting_year=2020, description="x")
        response = self.client.get(self.list_url, {"institution_name": "itb"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["institution_name"], "ITB")

    # ---------- star ----------
    def test_visitor_cannot_star(self):
        self.assertEqual(self.client.post(self.star_url).status_code, 403)
        self.assertEqual(self.record.starred_by.count(), 0)

    def test_regular_user_can_star_and_unstar(self):
        self.client.force_authenticate(self.regular)

        response = self.client.post(self.star_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["star_count"], 1)
        self.assertTrue(response.data["is_starred"])
        self.assertIn(self.regular, self.record.starred_by.all())

        response = self.client.post(self.star_url)
        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(self.record.starred_by.count(), 0)

    def test_star_always_uses_request_user(self):
        self.client.force_authenticate(self.regular)
        self.client.post(self.star_url, {"user": self.owner.pk}, format="json")
        self.assertEqual(list(self.record.starred_by.all()), [self.regular])


class EducationCSRFTests(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser("owner", password="pass12345")
        self.list_url = reverse("api:education-list")
        self.data = {
            "institution_name": "ITB", "starting_year": 2020,
            "end_year": None, "description": "Club",
        }
        self.client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(self.client.login(username="owner", password="pass12345"))

    def test_write_without_csrf_token_is_rejected(self):
        response = self.client.post(self.list_url, self.data, format="json")
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Education.objects.count(), 0)

    def test_write_with_csrf_token_succeeds(self):
        self.client.get(reverse("main:show_education"))   # sets cookie via @ensure_csrf_cookie
        token = self.client.cookies["csrftoken"].value
        response = self.client.post(
            self.list_url, self.data, format="json", HTTP_X_CSRFTOKEN=token)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Education.objects.count(), 1)