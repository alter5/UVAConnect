from django.db import models
import random

# For extending the User class
from django.contrib.auth.models import User
from chat.models import *
from django.utils.crypto import get_random_string


hobbies = ("not-entered")
class Choice(models.Model):
    description = models.CharField(max_length=300)
    def __str__(self):
        return self.description

class FriendsList(models.Model):    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name ="user", blank=True, null=True)
    friend_list = models.ManyToManyField(User,blank=True, null=True)
    def __str__(self):
        return f'{self.user.profile.full_name} Friends'

class Profile(models.Model):

    # Each user will have one profile
    # Automatically created after successfully registering with allauth (see signals.py)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    profile_is_complete = models.BooleanField(default=False)
    full_name = models.CharField(max_length=255, default="")
    email = models.EmailField(max_length=255, null=False, blank=False, default="testing@testing.com")
    food = models.CharField(max_length=50, default = "")
    hobbies = models.ManyToManyField(Choice, blank=True)
    major = models.CharField(max_length=50, default="")
    movie = models.CharField(max_length=50, default="")
    bio = models.CharField(max_length= 10000, default = "")
    friends = models.OneToOneField('FriendsList', blank=True, null=True, on_delete=models.CASCADE)
    
    # Profile images are uploaded to an AWS S3 bucket (see settings.py)
    imageFile = models.ImageField(upload_to='profile-images', verbose_name='Profile Image', blank=True, null=True)
    # If no image is uploaded, use the user's Google profile image
    googleProfileImageUrl = models.URLField(null=True)
    

    def __str__(self):
        return f'{self.full_name}'
    def make_friend(self,other):
        if not other in self.friends.friend_list.all():
            self.friends.friend_list.add(other)
            self.save()
    def remove_friend(self, bob):
        if bob in self.friends.friend_list.all():
            self.friends.friend_list.remove(bob)
            self.friends.friend_list.save()
            bob.profile.friends.friend_list.remove(self)
            bob.profile.friends.friend_list.save()
    def is_mutual(self,bob):
        return bob in self.friends.friend_list.all()
    def getProfileImageURL(self):
        if self.imageFile:
            return self.imageFile.url
        # User has not uploaded a profile image
        return self.googleProfileImageUrl


class FriendRequest(models.Model):
    sender= models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    receiver= models.ForeignKey(User, on_delete=models.CASCADE, related_name="receiver")
    is_active = models.BooleanField(blank=True, null=False, default=True)
    def __str__(self):
        return self.sender.profile.full_name + "'s request to "+ self.receiver.profile.full_name
    def accept(self):
        self.sender.profile.make_friend(self.receiver)
        self.receiver.profile.make_friend(self.sender)
        ChatRoom.objects.create(user1=self.sender, user2=self.receiver, key=get_random_string(length=32))
        self.is_active=False
        self.save()
    def reject(self):
        self.is_active=False
        self.save()
    def cancel(self):
        self.is_active=False
        self.save()

