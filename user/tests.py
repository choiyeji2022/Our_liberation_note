from unittest.mock import patch
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from diary.models import Note
from user.models import User, UserGroup


class UserTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            email="test@naver.com", password="aldud3015^^"
        )
        cls.group = UserGroup.objects.create(name="test", master=cls.user)
        # User를 group의 멤버로 추가
        cls.group.members.set([cls.user])
        cls.note = Note.objects.create(name="test", group=cls.group, category="1")
        cls.user_data = {"email": "test@naver.com", "password": "aldud3015^^"}

    def setUp(self):
        # 로그인 요청을 보내고, 액세스 토큰을 받아옴
        self.access_token = self.client.post(reverse("login"), self.user_data).data[
            "access"
        ]

    # 로그인 기능 테스트
    def test_signin(self):
        response = self.client.post(
            path=reverse("login"),
            data=self.user_data,
        )
        self.assertEquals(response.status_code, 200)

    # 사용자 정보 조회 기능 테스트
    def test_get_user(self):
        response = self.client.get(
            path=reverse("user_view"),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEquals(response.status_code, 200)

    # 사용자 정보 수정 기능 테스트
    def test_patch_user(self):
        response = self.client.patch(
            path=reverse("user_view"),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
            data={
                "check_password": "aldud3015^^",
                "new_password": "aldud3015^^^",
                "check_new_password": "aldud3015^^^",
            },
        )
        self.assertEquals(response.status_code, 200)

    # 사용자 계정 삭제 기능 테스트
    def test_delete_user(self):
        response = self.client.delete(
            path=reverse("user_view"),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEquals(response.status_code, 204)

    # 그룹 조회 기능 테스트
    def test_get_group(self):
        response = self.client.get(
            path=reverse("group"),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEquals(response.status_code, 200)

    # 그룹 상세 조회 기능 테스트
    def test_get_detail_group(self):
        url = self.group.get_absolute_url(category="group")
        response = self.client.get(
            path=url,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEquals(response.status_code, 200)

    # 그룹 상세 수정 기능 테스트
    def test_patch_detail_group(self):
        url = self.group.get_absolute_url(category="group")
        response = self.client.patch(
            path=url,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
            data={"name": "test_group2"},
        )
        self.assertEquals(response.status_code, 200)

    # 그룹 상세 삭제 기능 테스트
    def test_delete_detail_group(self):
        url = self.group.get_absolute_url(category="group")
        response = self.client.delete(
            path=url,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEquals(response.status_code, 204)

    # 마이 페이지 조회 기능 테스트
    def test_my_page(self):
        response = self.client.get(
            path=reverse("my_page"),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEquals(response.status_code, 200)

    # 사용자 리스트 조회 기능 테스트
    def test_user_list(self):
        response = self.client.get(
            path=reverse("user_list"),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEquals(response.status_code, 200)


# 카카오 로그인 테스트 클래스
class KakaoLoginTest(APITestCase):
    # requests.post와 requests.get을 모킹
    @patch("requests.post")
    @patch("requests.get")
    def test_kakao_login_success(self, mock_get, mock_post):
        # Mocking된 응답 설정
        mock_post.return_value.json.return_value = {
            "access_token": "mock_access_token",
        }

        mock_get.return_value.json.return_value = {
            "kakao_account": {"email": "test@naver.com"}
        }

        # 카카오 로그인 요청 테스트
        response = self.client.post(reverse("kakao_login"), data={"code": "mock_code"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)


# 구글 로그인 테스트 클래스
class GoogleLoginTest(APITestCase):
    # requests.post와 requests.get을 모킹
    @patch("requests.post")
    @patch("requests.get")
    def test_google_login_success(self, mock_get, mock_post):
        # Mocking된 응답 설정
        mock_post.return_value.json.return_value = {
            "access_token": "mock_access_token",
        }

        mock_get.return_value.json.return_value = {"email": "test@naver.com"}

        # 구글 로그인 요청 테스트
        response = self.client.post(reverse("google_login"), data={"code": "mock_code"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)


# 네이버 로그인 테스트 클래스
class NaverLoginTest(APITestCase):
    # requests.post와 requests.get을 모킹
    @patch("requests.post")
    @patch("requests.get")
    def test_google_login_success(self, mock_get, mock_post):
        # Mocking된 응답 설정
        mock_post.return_value.json.return_value = {
            "access_token": "mock_access_token",
        }

        mock_get.return_value.json.return_value = {
            "response": {"email": "test@naver.com"}
        }

        # 네이버 로그인 요청 테스트
        response = self.client.post(reverse("naver_login"), data={"code": "mock_code"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
