from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Conversation(models.Model):
    user1 = models.ForeignKey(User, related_name='conversations1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name='conversations2', on_delete=models.CASCADE)

    def other_user(self, current_user):
        return self.user1 if self.user2 == current_user else self.user2
    
    def latest_message_time(self):
        latest_message = self.messages.order_by('-timestamp').first()
        return latest_message.timestamp if latest_message else None

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']