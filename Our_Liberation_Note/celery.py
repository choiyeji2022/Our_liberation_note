# from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
# from django.conf import settings
from Our_Liberation_Note import settings

from celery.schedules import crontab
from pathlib import Path
from datetime import timedelta


# Absolute filesystem path to the top-level project folder:
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

# settings.SECRET_KEY = 'django-insecure-s)=v9h_j$0^w#mhgp^3*^-0mivlqd-424o=u5txxidl0!=0@kr'


# 설정되어있는 경우 환경변수 'DJANGO_SETTINGS_MODULE'를 가리키게 한다.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Our_Liberation_Note.settings")


app = Celery("Our_Liberation_Note")

# Django 설정 파일에 있는 설정을 사용하도록 한다.
app.config_from_object('django.conf:settings', namespace='CELERY')


# 개별 앱중에서 작업자를 작동시킨다.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.broker_connection_retry_on_startup = True


app.conf.beat_schedule = {
    'delete_expired_emails': {
        'task': 'user.tasks.delete_expired_emails',
        # 'schedule': crontab(minute='*/15'), # 15분마다 실행
        'schedule': timedelta(seconds=1), # 임시로 설정해둔 시간 삭제할 예정
    },
}