import os
import sys

# import dotenv

# django-dotenv를 사용하는 경우, 프로젝트 시작 부분에 환경 변수를 로드할 수 있도록 설정
# dotenv.read_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Our_Liberation_Note.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    # dotenv.read_dotenv()
    main()
