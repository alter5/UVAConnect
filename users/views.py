from django.contrib.auth.models import User
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from django.urls.base import reverse_lazy
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from .forms import *
from users.models import *
from chat.models import *
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.auth import logout
import json


def profile_complete_check(user):
    # Used in the @user_passes_test decorator
    # Source: (Django website) https://docs.djangoproject.com/en/3.1/topics/auth/default/#limiting-access-to-logged-in-users-that-pass-a-test
    try:
        return user.profile.profile_is_complete
    except:
        return False


@user_passes_test(profile_complete_check, login_url=reverse_lazy('create-profile'))
def profile(request):
    profile = request.user.profile

    if request.method == 'POST':
        p_form = updateProfileForm(
            request.POST, request.FILES, instance=request.user.profile)

        if p_form.is_valid():
            p_form.save(commit=False)
            hobbies = p_form.cleaned_data['hobbies']
            for x in profile.hobbies.all():
                if x not in hobbies:
                    profile.hobbies.remove(x)
            for x in hobbies:
                profile.hobbies.add(x)
            profile.major = p_form.cleaned_data['major']
            profile.food = p_form.cleaned_data['food']
            profile.movie = p_form.cleaned_data['movie']
            profile.bio = p_form.cleaned_data['bio']
            profile.imageFile = p_form.cleaned_data['imageFile']
            profile.save()

            messages.add_message(request, messages.SUCCESS, 'Your profile was updated successfully')

            redirect('profile')
    else:
        p_form = updateProfileForm(instance=request.user.profile)

    context = {
        'p_form': p_form
    }
    return render(request, 'users/profile.html', {'form': p_form})


def create_profile(request):
    storage = messages.get_messages(request)
    for m in storage:
        pass
    for m in list(storage._loaded_messages):
        del storage._loaded_messages[0]
    storage.used = True
    # create a dictionary with instances
    profile = request.user.profile
    # except Profile.DoesNotExist:
    #    profile = Profile(user=request.user)
    if request.method == 'GET':
        form = createProfileForm(
            # initial={
            # 'full_name': User.profile.full_name,
            # 'email': User.profile.email
            # }
        )
    else:
        form = createProfileForm(
            request.POST,
            request.FILES
            # initial={
            # 'full_name': User.profile.full_name,
            # 'email': User.profile.email
            # },
        )
        if form.is_valid():
            #cur_profile = form.save(commit=False)
            hobbies = form.cleaned_data['hobbies']
            for x in hobbies:
                profile.hobbies.add(x)
            profile.major = form.cleaned_data['major']
            profile.food = form.cleaned_data['food']
            profile.movie = form.cleaned_data['movie']
            profile.bio = form.cleaned_data['bio']
            profile.profile_is_complete = True
            profile.imageFile = form.cleaned_data['imageFile']
            profile.save()

            messages.add_message(request, messages.SUCCESS, 'You have successfully created a new profile')
            #cur_profile.user = request.user
            #cur_profile.user.profile_is_complete = True
            # cur_profile.save()
            # form.save()
            #request.user.profile.profile_is_complete = True
            # change user.profile is complete field
            # to true
        if not form.is_valid:
            print(form.errors)
        return HttpResponseRedirect(reverse('index'))
    return render(request, 'users/create-profile.html', {'form': form})

# authenticated == LOGIN_REDIRECT_URL
def authenticated(request):
    if (profile_complete_check(request.user)):
        # If a user's profile is completed, redirect them to the index
        return HttpResponseRedirect(reverse('index'))
    # Profile has not been completed
    return HttpResponseRedirect(reverse('create-profile'))

#helper
def get_friend_request(sender, receiver):
    try:
        return FriendRequest.objects.get(sender=sender, receiver=receiver, is_active=True)
    except FriendRequest.DoesNotExist:
        return False 
# Followed youtube tutorial, https://www.youtube.com/watch?v=hyJO4mkdwuM
#status, 0 meaning the user and profile are friends
#        1 meaning the two are not friends and the other had sent a request over
#        2 meaning the two are not friends and the user had sent a request over
#        3 meaning the two are not friends and no request was sent over

def profile_detail(request, profile_id):
    profile = get_object_or_404(Profile, pk=profile_id)
    fr, fr2 = get_friend_request(profile.user,request.user), get_friend_request(request.user, profile.user)
    frid= -1
    if profile.is_mutual(request.user):
        status =0
        status_display="Friends"
        try: 
            temp = ChatRoom.objects.get(user1=request.user, user2=profile.user)
        except:
            try:
                temp = ChatRoom.objects.get(user1=profile.user, user2=request.user)
            except:
                print("Room not found")
        return render(request, 'users/individual_profile.html', {'profile': profile, 'status':status, 'status_display': status_display, 'frid':frid, 'chatroom':temp.key})
    elif fr:
        frid=fr.pk
        status=1
        status_display="Accept Friend Request"
    elif fr2:
        frid=fr2.pk
        status=2
        status_display="Pending Friend Request"
    else:
        status =3
        status_display = "Send Friend Request"
    return render(request, 'users/individual_profile.html', {'profile': profile, 'status':status, 'status_display': status_display, 'frid':frid})

def send_friend_request(request, *args, **kwargs):
    user = request.user
    payload= {}
    if request.method =='POST' and user.is_authenticated:
        email= request.POST.get("receiver_user")
        if email:
            receiver=User.objects.get(email=email)
            if len(FriendRequest.objects.filter(sender=user, receiver=receiver, is_active=False))==0:
                friend_request = FriendRequest(sender=user, receiver = receiver)
                friend_request.save()
                payload['response']= "Sent"
    return HttpResponse(json.dumps(payload), content_type = "application/json")

def accept_friend_request(request, *args, **kwargs):
    print("hello")
    user = request.user
    payload= {}
    if request.method =='GET' and user.is_authenticated:
        frid= kwargs.get("friend_request_id")
        if frid:
            friend_request = FriendRequest.objects.get(pk= frid)
            friend_request.accept()
            payload['response']= "Accepted"
    return HttpResponse(json.dumps(payload), content_type = "application/json")

def reject_friend_request(request, *args, **kwargs):
    user = request.user
    payload= {}
    if request.method =='GET' and user.is_authenticated:
        frid= kwargs.get("friend_request_id")
        if frid:
            friend_request = FriendRequest.objects.get(pk= frid)
            friend_request.reject()
            payload['response']= "Rejected"
    return HttpResponse(json.dumps(payload), content_type = "application/json")

def logoutView(request):
    messages.add_message(request, messages.SUCCESS, 'You have been signed out')
    # Logout the user
    logout(request)
    # Redirect them to the index
    return HttpResponseRedirect(reverse('index'))
