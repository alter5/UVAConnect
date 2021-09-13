from django.db import models
import random
from django.contrib.auth.models import User
class ChatRoom(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE,related_name="user1")
    user2 = models.ForeignKey(User, on_delete=models.CASCADE,related_name="user2")
    key = models.CharField(max_length=255, default="")
    def __str__(self):
        return self.user1.profile.full_name + "'s chat with "+ self.user2.profile.full_name
    def getMessages(self):  
        return Message.objects.filter(room=self.pk).order_by("timestamp")


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    content = models.TextField(unique=False, blank=False)
    room = models.ForeignKey(ChatRoom,on_delete=models.CASCADE )
    def __str__(self):
        return self.content

