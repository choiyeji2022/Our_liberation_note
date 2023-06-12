from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

status_choice = (
    ("0", "활성화"),
    ("1", "비활성화"),
    ("2", "강제중지"),
    ("3", "삭제"),
)


class CheckEmail(models.Model):
    email = models.EmailField("인증용 이메일", max_length=100, unique=True)
    code = models.CharField("확인용 코드", max_length=6, unique=True)
    try_num = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)


# custom user model 사용 시 UserManager 클래스와 create_user, create_superuser 함수가 정의되어 있어야 함
class UserManager(BaseUserManager):
    def create_user(self, nickname, email, password=None):
        if not nickname:
            raise ValueError("Users must have a nickname")
        if not email:
            raise ValueError("Users must have an email")

        user = self.model(
            nickname=nickname,
            email=email
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    # python manage.py createsuperuser 사용 시 해당 함수가 사용됨
    def create_superuser(self, nickname, email, password=None):
        user = self.create_user(nickname=nickname, email=email, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    nickname = models.CharField("닉네임", max_length=100, unique=True)
    email = models.EmailField("이메일 주소", max_length=100, unique=True)
    username = models.CharField("이름", max_length=20)
    password = models.CharField("비밀 번호", max_length=128)
    join_date = models.DateTimeField("가입일", auto_now_add=True)

    # is_active가 False일 경우 계정이 비활성화됨
    is_active = models.BooleanField(default=True)

    # is_staff에서 해당 값 사용
    is_admin = models.BooleanField(default=False)

    # id로 사용 할 필드 지정.
    # 로그인 시 USERNAME_FIELD에 설정 된 필드와 password가 사용된다.
    USERNAME_FIELD = "nickname"

    # user를 생성할 때 입력받은 필드 지정, 일단 email로 설정했습니다
    REQUIRED_FIELDS = ["email"]

    objects = UserManager()  # custom user 생성 시 필요

    def __str__(self):
        return self.nickname

    # 로그인 사용자의 특정 테이블의 crud 권한을 설정, perm table의 crud 권한이 들어간다.
    # admin일 경우 항상 True, 비활성 사용자(is_active=False)의 경우 항상 False
    def has_perm(self, perm, obj=None):
        return True

    # 로그인 사용자의 특정 app에 접근 가능 여부를 설정, app_label에는 app 이름이 들어간다.
    # admin일 경우 항상 True, 비활성 사용자(is_active=False)의 경우 항상 False
    def has_module_perms(self, app_label):
        return True

    # admin 권한 설정
    @property
    def is_staff(self):
        return self.is_admin


class UserGroup(models.Model):
    members = models.ManyToManyField(
        User, verbose_name="멤버", related_name="user_group", blank=True
    )
    master = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="그룹장", related_name="master_group"
    )
    name = models.CharField("그룹 이름", max_length=30)
    created_at = models.DateTimeField("생성일", auto_now_add=True)
    updated_at = models.DateTimeField("업데이트", auto_now=True)
    status = models.CharField("상태", choices=status_choice, max_length=1, default="0")

    def __str__(self):
        return self.name


# 소셜 로그인
class OauthId(models.Model):
    access_token = models.CharField("토큰", max_length=255)
    provider = models.CharField("구분자", max_length=255)

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="회원")

    def __str__(self):
        return f"[아이디]{self.user.username}, [소셜 도메인]{self.provider}"