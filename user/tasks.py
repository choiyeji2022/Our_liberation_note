from celery import shared_task
from .models import CheckEmail
import datetime


# delete_expired() 메서드 사용한 코드
@shared_task
def delete_expired_emails():
    # 만료된 이메일을 삭제
    num_deleted = CheckEmail.objects.delete_expired()[0]
    print(f"{num_deleted} expired email(s) deleted.")

__all__ = ("delete_expired_emails",)


#================================================================================


# def delete_expired_emails():
    # 만료된 이메일 코드들 조회하기
    # expired_emails = CheckEmail.objects.filter(
        # created_at__lte=datetime.datetime.now() - datetime.timedelta(minutes=5)
    # )

    # 만료된 이메일 코드들 삭제
    # num_deleted = expired_emails.delete()[0]
    # print(f"{num_deleted} expired email(s) deleted.")

# 외부로 공개되는 식별자의 목록을 지정하는 매직 메소드
# tasks.py에서만 사용되는 메소드를 지정할 수 있음
# 외부에서 사용되면 안되는 메서드를 지정할 때 __all__ 속성을 사용해 제한할 수 있음
