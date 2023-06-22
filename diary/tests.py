from django.urls import reverse
from rest_framework.test import APITestCase

from user.models import User, UserGroup

from .models import Note, PhotoPage, PlanPage, Stamp


class NoteTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            email="test@naver.com", password="aldud3015^^"
        )
        cls.data = {"email": "test@naver.com", "password": "aldud3015^^"}
        cls.group = UserGroup.objects.create(name="test", master=cls.user)
        cls.note = {"name": "test", "category": "1", "group": "1"}

    def setUp(self):
        self.access_token = self.client.post(reverse("login"), self.data).data["access"]

    def test_post_note(self):
        response = self.client.post(
            path=reverse("note_post"),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
            data=self.note,
        )

        self.assertEquals(response.status_code, 201)

    def test_get_note(self):
        response = self.client.get(
            path=reverse("note_post"),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
            data=self.note,
        )
