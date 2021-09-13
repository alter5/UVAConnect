from typing import Dict
from django.shortcuts import render
from django.urls.base import reverse_lazy
from users.views import profile, profile_complete_check
from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse
from django.contrib import messages

from users.models import *
from queue import PriorityQueue
import spacy
import random



#@user_passes_test(profile_complete_check, login_url=reverse_lazy('create-profile'))
#Smaller distance value for similar profiles

def ordering(user, profiles):
    ordered = PriorityQueue()
    ordered_list = []
    all_distance = []
    #speed up
    nlp = spacy.load('en_core_web_sm',  disable=['parser', 'ner'])
    u_hobby = user.profile.hobbies.all()
    u_food = nlp(user.profile.food.split(" ")[0])
    u_movie = nlp(user.profile.movie.split(" ")[0])
    u_major = nlp(user.profile.major.split(" ")[0])
    for profile in profiles:
        if profile.email != user.profile.email:
            #Number of similar hobbies
            distance = float(- len([hobby for hobby in u_hobby if hobby in profile.hobbies.all()]))
            #Distance of word vectors
            #Food
            p_food = nlp(profile.food.split(" ")[0])
            if p_food!="Undeclared" and u_food!="Undeclared":
                distance -= u_food.similarity(p_food)
            #Movies
            p_movie = nlp(profile.food.split(" ")[0])
            if p_movie!="Undeclared" and u_movie!="Undeclared":
                distance -= u_major.similarity(p_movie)
            #Major
            p_major = nlp(profile.food.split(" ")[0])
            if p_major!="Undeclared" and u_major!="Undeclared":
                distance -= u_major.similarity(p_major)
            #random to take care of the possibility in which the first distance value is the same
            #avoids comparing profiles
            ordered.put((distance + random.uniform(-0.001, 0.001), profile))
            all_distance.append(distance + random.uniform(-0.001, 0.001))
    while not ordered.empty():
         ordered_list.append(ordered.get()[1])
    # calculate similarity 
    all_distance.sort()
    all_distance = [-dist*100/((len(u_hobby)+len(u_food)+len(u_movie)+len(u_major))) for dist in all_distance]
    all_distance = [round(dist, 2) for dist in all_distance]
    dictionary = dict(zip(ordered_list, all_distance))
    return dictionary


def IndexView(request):

    if request.user.is_authenticated:
        storage = messages.get_messages(request)
        for m in storage:
            pass
        for m in list(storage._loaded_messages):
            del storage._loaded_messages[0]
        storage.used = True
        request_profiles=[]
        requests= FriendRequest.objects.filter(receiver=request.user, is_active=True)
        for r in requests:
            request_profiles.append(r.sender.profile)
        profiles = Profile.objects.all()
        profiles = ordering(request.user, profiles)
        top_three_profiles: dict = getTopThreeProfiles(profiles)
        context= {'profiles':profiles, "top_three":top_three_profiles, 'request_profiles':request_profiles}
        return render(request, "home/index.html", context)
    return render(request, "home/index.html")

def getTopThreeProfiles(profiles: dict):
    # Get top 4 profiles
    top_three = profiles.keys()
    top_three = list(top_three)[:3]

    # Store top 4 profiles into a new dict
    top_three_profiles: dict = dict()
    for p in top_three:
        top_three_profiles[p] = profiles[p]
        # Remove top 4 profiles from main profiles dict
        profiles.pop(p, None)
    return top_three_profiles