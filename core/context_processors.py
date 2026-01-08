from core.models import CustomUser


def pending_registrations_count(request):
    """Add pending registrations count to context for admin users"""
    pending_count = 0
    
    if request.user.is_authenticated and request.user.is_admin():
        pending_count = CustomUser.objects.filter(
            user_type='customer',
            is_approved=False
        ).count()
    
    return {
        'pending_count': pending_count,
    }
