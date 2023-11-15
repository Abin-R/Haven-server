# utils.py

from  subscription.models import SubcribedUsers

def get_user_role(user):
    try:
        sub = SubcribedUsers.objects.get(user=user)
    except SubcribedUsers.DoesNotExist:
        sub = None

    if user.is_superuser:
        return 'admin'
    elif sub and sub.is_premium:
        return 'premium'
    elif sub and sub.is_super:
        return 'super'
    else:
        return 'user'
