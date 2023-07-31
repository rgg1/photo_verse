from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Notification

# Create your views here.

@login_required
def notifications_view(request):
    notifications = Notification.objects.filter(user=request.user)
    notifications.update(read=True)  # set all notifications to read
    return render(request, 'notifications/notifications.html', {'notifications': notifications})