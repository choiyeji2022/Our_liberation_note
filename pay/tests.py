from unittest.mock import patch

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from diary.models import Note
from user.models import User, UserGroup


class TossTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            email="test@naver.com", password="aldud3015^^"
        )
        cls.group = UserGroup.objects.create(name="test", master=cls.user)
        cls.note = Note.objects.create(name="test", group=cls.group, category="1")

        cls.user_data = {"email": "test@naver.com", "password": "aldud3015^^"}

    def setUp(self):
        self.access_token = self.client.post(reverse("login"), self.user_data).data[
            "access"
        ]

    # requests.post 함수를 모킹하기 위한 데코레이터
    @patch("requests.post")
    def test_toss_success(self, mock_post):
        # Mocking된 응답 설정
        mock_post.return_value.json.return_value = {
            "paymentKey": "mock_payment_key",
            "orderId": "mock_order_id",
            "suppliedAmount": 100,
            "totalAmount": 100,
            "vat": 10,
            "requestedAt": "20230622",
            "orderName": "mock_order_name",
        }

        # Toss 결제 확인 요청을 보냄
        response = self.client.get(
            reverse("success"),
            data={
                "orderId": "mock_order_id",
                "amount": 100,
                "paymentKey": "mock_payment_key",
                "note_id": self.note.id,
            },
            HTTP_AUTHORIZATION_TOKEN=self.access_token,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("res", response.json())
