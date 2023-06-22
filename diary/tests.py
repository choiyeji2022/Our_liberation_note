from django.urls import reverse
from rest_framework.test import APITestCase

from user.models import User, UserGroup

from .models import Note, PlanPage


class NoteTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            email="test@naver.com", password="aldud3015^^"
        )
        cls.group = UserGroup.objects.create(name="test", master=cls.user)
        cls.note = Note.objects.create(name="test", group=cls.group, category="1")
        cls.user_data = {"email": "test@naver.com", "password": "aldud3015^^"}
        cls.note_data = {"name": "test2", "category": "1", "group": "1"}

    def setUp(self):
        # 각 테스트 케이스 실행 전에 로그인하고 토큰을 받아옴
        self.access_token = self.client.post(reverse("login"), self.user_data).data[
            "access"
        ]

    def test_post_note(self):
        # Note 생성에 대한 테스트
        response = self.client.post(
            path=reverse("note_post"),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
            data=self.note_data,
        )
        self.assertEquals(response.status_code, 201)

    def test_get_note(self):
        # Note 조회에 대한 테스트
        url = self.group.get_absolute_url()
        response = self.client.get(
            path=url, HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
        )
        self.assertEquals(response.status_code, 200)

    def test_get_detail_note(self):
        # Note 상세 조회에 대한 테스트
        url = self.note.get_absolute_url()
        response = self.client.get(
            path=url, HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
        )
        self.assertEquals(response.status_code, 200)

    def test_patch_detail_note(self):
        # Note 수정에 대한 테스트
        url = self.note.get_absolute_url()
        response = self.client.patch(
            path=url,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
            data=self.note_data,
        )
        self.assertEquals(response.status_code, 200)

    def test_delete_detail_note(self):
        # Note 삭제에 대한 테스트
        url = self.note.get_absolute_url()
        response = self.client.delete(
            path=url, HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
        )
        self.assertEquals(response.status_code, 204)


class PlanTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # 테스트를 위한 초기 데이터 설정
        cls.user = User.objects.create_user(
            email="test@naver.com", password="aldud3015^^"
        )
        cls.group = UserGroup.objects.create(name="test", master=cls.user)
        cls.note = Note.objects.create(name="test", group=cls.group, category="1")
        cls.plan = PlanPage.objects.create(
            title="test", diary=cls.note, start="2022-12-12"
        )
        cls.user_data = {"email": "test@naver.com", "password": "aldud3015^^"}
        cls.note_data = {"name": "test2", "category": "1", "group": "1"}
        cls.plan_data = {
            "plan_set": [{"title": "스타벅스 리버사이드팔당DT점", "start": "2023-12-17"}]
        }

    def setUp(self):
        # 각 테스트 케이스 실행 전에 로그인하고 토큰을 받아옴
        self.access_token = self.client.post(reverse("login"), self.user_data).data[
            "access"
        ]

    def test_get_plan(self):
        # Plan 조회에 대한 테스트
        url = self.note.get_absolute_url(category="plan")
        response = self.client.get(
            path=url, HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
        )
        self.assertEquals(response.status_code, 200)

    def test_post_plan(self):
        # Plan 생성에 대한 테스트
        url = self.note.get_absolute_url(category="plan")
        response = self.client.post(
            path=url,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
            data=self.plan_data,
        )
        self.assertEquals(response.status_code, 200)

    def test_delete_plan(self):
        # Plan 삭제에 대한 테스트
        url = self.note.get_absolute_url(category="plan")
        response = self.client.delete(
            path=url,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEquals(response.status_code, 204)

    def test_get_detail_plan(self):
        # Plan 상세 조회에 대한 테스트
        url = self.plan.get_absolute_url()
        response = self.client.get(
            path=url, HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
        )
        self.assertEquals(response.status_code, 200)

    def test_patch_detail_plan(self):
        # Plan 수정에 대한 테스트
        url = self.plan.get_absolute_url()
        response = self.client.patch(
            path=url,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
            data={"title": "test"},
        )
        self.assertEquals(response.status_code, 200)

    def test_delete_detail_plan(self):
        # Plan 상세 삭제에 대한 테스트
        url = self.plan.get_absolute_url()
        response = self.client.delete(
            path=url, HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
        )
        self.assertEquals(response.status_code, 204)
