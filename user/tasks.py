import datetime

from celery import shared_task

from .models import CheckEmail


@shared_task
def delete_expired_emails():
    # 만료된 이메일을 조회하기
    expired_emails = CheckEmail.objects.filter(
        created_at__lte=datetime.datetime.now() - datetime.timedelta(minutes=5)
    )

    # 만료된 이메일을 삭제
    num_deleted = expired_emails.delete()[0]
    print(f"{num_deleted} expired email(s) deleted.")


__all__ = ("delete_expired_emails",)
