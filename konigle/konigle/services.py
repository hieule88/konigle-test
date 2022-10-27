from datetime import timedelta
from django.db.models import Q
from django.utils import timezone

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.settings import api_settings

from unity.models import VisitorEmail
from unity.constants.visitor_emails import VisitorEmailStatusType, VisitorEmailIsSentType


def get_token(user):
    """Generate access token from user."""
    refresh = RefreshToken.for_user(user)
    return {
        "access_token": str(refresh.access_token),
        "refresh_token": str(refresh),
        'token_type': "Bearer",
        "expires_in": (
            timezone.now() + timedelta(api_settings.ACCESS_TOKEN_LIFETIME.days)
        ).timestamp(),
        "created_at": timezone.now(),
    }
