from celery import shared_task
from django.contrib.auth import get_user_model

User = get_user_model()

@shared_task
def reset_weekly_kudos():
    User.objects.update(remaining_kudos=3)
    print("Weekly kudos reset completed.")
