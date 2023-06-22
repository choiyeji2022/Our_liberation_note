from django.urls import reverse
from rest_framework.test import APITestCase
from user.models import User, UserGroup
from .models import Payment, Subscribe
from diary.models import Note


class TossTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            email="test@naver.com", password="aldud3015^^"
        )
        cls.group = UserGroup.objects.create(name="test", master=cls.user)
        cls.note = Note.objects.create(name="test", group=cls.group, category="1")

    def setUp(self):
        self.access_token = self.client.post(reverse("login"), self.user_data).data[
            "access"
        ]

    

