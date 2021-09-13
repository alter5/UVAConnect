from allauth.account.signals import user_signed_up, user_logged_in
from django.dispatch import receiver
from .models import Profile, User, FriendsList
from urllib.parse import urlparse
from urllib.request import urlretrieve
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib import messages


@receiver(user_signed_up)
def create_profile(request, user, **kwargs):
    """ Listens to the allauth user_signed_up signal to automatically create a profile upon successful authentication """
    # Source: (Allauth) https://github.com/pennersr/django-allauth/blob/master/allauth/account/signals.py
    # Source: (Stackoverflow example) https://stackoverflow.com/questions/40684838/django-django-allauth-save-extra-data-from-social-login-in-signal

    userAllauth: User = user
    profile: Profile = Profile.objects.create(user=userAllauth)
    
    profile.full_name = userAllauth.get_full_name()
    profile.email = userAllauth.email
    profile.friends = FriendsList.objects.create(user = userAllauth)
    profile.googleProfileImageUrl = user.socialaccount_set.filter(provider='google')[0].extra_data['picture']

    # Profile is a foreign key in the User model
    userAllauth.profile.save()

@receiver(user_logged_in)
def logged_in(request, user, **kwargs):
    # Source: (Allauth) https://github.com/pennersr/django-allauth/blob/master/allauth/account/signals.py
    # Bug:  Logged_in executes immediately after user_signed_up receiver above, 
    #       and does not allow for create_profile to finish first due to threading

    if hasattr(user, 'profile'):
        # User logged_in should only be executed after the user profile has been created
        userAllauth: User = user
        profile = userAllauth.profile

        # Update user's profile image each time they login
        profile.googleProfileImageUrl = user.socialaccount_set.filter(provider='google')[0].extra_data['picture']

        userAllauth.profile.save()