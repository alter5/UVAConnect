from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from users.models import *
from chat.models import *
import time

def SpecificChatView(request, room_name):
    room = get_object_or_404(ChatRoom, key=room_name)
    if request.user.is_authenticated:
        storage = messages.get_messages(request)
        for m in storage:
            pass
        for m in list(storage._loaded_messages):
            del storage._loaded_messages[0]
        storage.used = True
        if room.user1 != request.user and room.user2 != request.user:
            return redirect('chat')
        else:
            chat_messages = room.getMessages()
            friends = {}
            friends2= {}
            for x in request.user.profile.friends.friend_list.all():
                print(x.profile.full_name)
                try: 
                    temp = ChatRoom.objects.get(user1=request.user, user2=x)
                    m = temp.getMessages()
                    if m.exists():
                        friends[x]= [temp.key,m.last().timestamp]
                    else:
                        friends2[x]=temp.key

                except:
                    print("Second try")
                    try:
                        temp = ChatRoom.objects.get(user1=x, user2=request.user)
                        m = temp.getMessages()
                        if m.exists():
                            friends[x]= [temp.key,m.last().timestamp]
                        else:
                            friends2[x] =temp.key
                    except:
                        print("Could not find room")
            friends = {x: y[0] for x, y in sorted(friends.items(), key=lambda item: item[1][1])}
            friends3 = {}
            for f in reversed(list(friends.keys())):
                friends3[f]=friends[f]
            for f in list(friends2.keys()):
                friends3[f] = friends2[f]
            context= {'friends':friends3,
            'room_name': room_name,
            'chat_messages': chat_messages}
            return render(request, "chat/chats.html", context)
    return render(request, "chat/chats.html")
    
def ChatView(request):
    if request.user.is_authenticated:
        friends = {}
        friends2= {}
        for x in request.user.profile.friends.friend_list.all():
            print(x.profile.full_name)
            try: 
                temp = ChatRoom.objects.get(user1=request.user, user2=x)
                m = temp.getMessages()
                if m.exists():
                    friends[x]= [temp.key,m.last().timestamp]
                else:
                    friends2[x]=temp.key
            except:
                print("Second try")
                try:
                    temp = ChatRoom.objects.get(user1=x, user2=request.user)
                    m = temp.getMessages()
                    if m.exists():
                        friends[x]= [temp.key,m.last().timestamp]
                    else:
                        friends2[x]=temp.key
                except:
                    print("Could not find room")
        friends = {x: y[0] for x, y in sorted(friends.items(), key=lambda item: item[1][1])}
        i, latest= 1, None
        friends3 = {}
        for f in reversed(list(friends.keys())):
            if i==1:
                latest = friends[f]
                i=0
            friends3[f]=friends[f]
        for f in list(friends2.keys()):
            friends3[f] = friends2[f]
        if friends3 =={}:
            messages.add_message(request, messages.WARNING, 'Start by making some friends!')
            context = {'friends':friends}
            return render(request, "chat/chats.html", context)
        elif latest ==None:
            latest = friends2[list(friends2.keys())[-1]]
        context= {'friends':friends3,
            'room_name': latest,
            'chat_messages': ChatRoom.objects.get(key=latest).getMessages()}
        return render(request, "chat/chats.html", context)
    return render(request, "chat/chats.html")
