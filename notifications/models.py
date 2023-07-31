from django.db import models
from django.conf import settings
from accounts.models import UserProfile
import pytz

# Create your models here.

class Notification(models.Model):
    MESSAGE = 'message'
    FOLLOW = 'follow'
    LIKE = 'like'
    COMMENT = 'comment'

    CHOICES = [
        (MESSAGE, 'Message'),
        (FOLLOW, 'Follow'),
        (LIKE, 'Like'),
        (COMMENT, 'Comment'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    extra_id = models.IntegerField(null=True, blank=True)
    extra_info = models.CharField(max_length=255, blank=True)
    read = models.BooleanField(default=False)
    timezone = models.CharField(max_length=50, choices=[(tz, tz) for tz in pytz.common_timezones], null=True)

    def save(self, *args, **kwargs):
        if not self.pk:  # Only set timezone during the first save.
            user_profile = UserProfile.objects.get(user=self.user)
            self.timezone = user_profile.timezone
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']  # newest notifications first