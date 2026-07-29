from .models import Activity

def log_activity(user, action_type, message):
    Activity.objects.create(
        user=user,
        action_type=action_type,
        message=message
    )