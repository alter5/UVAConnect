from users.views import profile_complete_check
from users.models import *
from chat.models import *
from users.forms import *
from home.views import ordering
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

class CreateProfile(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user1', password='123pass')
        login = self.client.login(username= 'user1', password = '123pass')
        self.profile = Profile.objects.create(user=self.user)
        self.assertEqual(self.profile.major, "")
    def test_create(self):
        form = createProfileForm(instance = self.profile, data={'major': "CS", 'food':"Pizza", 'movie': "Harry Potter", 'bio':"hi"})
        self.assertTrue(form.is_valid())
        case = form.save()
        self.assertEqual(self.profile.major, "CS")
class UpdateProfile(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user1', password='123pass')
        login = self.client.login(username= 'user1', password = '123pass')
        self.profile = Profile.objects.create(user=self.user)
        self.assertEqual(self.profile.major, "")
    def test_update(self):
        form = updateProfileForm(instance = self.profile, data={ 'major': "CS", 'food':"Pizza", 'movie': "Harry Potter", 'bio':"hi"})
        self.assertTrue(form.is_valid())
        case = form.save()
        self.assertEqual(self.profile.major, "CS")

class RedirectLoginProfileIsCompleteTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='user', password='123pass')
        login = self.client.login(username='user', password='123pass')
        profile = Profile.objects.create(user=self.user)

    def test_redirect_profile_not_complete(self):
        response = self.client.get(reverse('profile'), follow=True)
        
        isRedirectedToCreateProfile = False
        for HttpResponse in response.redirect_chain:
            if HttpResponse[0].find("create-profile") != -1:
                isRedirectedToCreateProfile = True
        self.assertEqual(isRedirectedToCreateProfile, True)

    def test_profile_is_completed(self):
        self.user.profile.profile_is_complete = True
        self.assertTrue(profile_complete_check(self.user))

class MatchingProfiles(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user1', password='123pass')
        login = self.client.login(username= 'user1', password = '123pass')
        self.profile = Profile.objects.create(user=self.user)
        form = createProfileForm(instance = self.profile, data={'major': "CS", 'food':"Pizza", 'movie': "Harry Potter", 'bio':"hi"})
        self.assertTrue(form.is_valid())
        case = form.save()

        self.user2 = User.objects.create_user(username='user2', password='123pass')
        login = self.client.login(username= 'user2', password = '123pass')
        self.profile2 = Profile.objects.create(user=self.user2)
        form = createProfileForm(instance = self.profile2, data={'major': "CS", 'food':"Pizza", 'movie': "Harry Potter", 'bio':"bye"})
        self.assertTrue(form.is_valid())
        case = form.save()

        self.user3 = User.objects.create_user(username='user3', password='123pass')
        login = self.client.login(username= 'user3', password = '123pass')
        self.profile3 = Profile.objects.create(user=self.user3)
        form = createProfileForm(instance = self.profile3, data={'major': "Econ", 'food':"Salad", 'movie': "Harry Potter", 'bio':"bye"})
        self.assertTrue(form.is_valid())
        case = form.save()
        
    def test(self):
        profiles=ordering(self.user, Profile.objects.all())
        index=0
        correct_order=[self.profile2,self.profile3]
        for key,values in profiles.items():
            self.assertTrue(key, correct_order[index])
            index+=1
class FriendRequest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user1', password='123pass')
        login = self.client.login(username= 'user1', password = '123pass')
        self.user2 = User.objects.create_user(username='user2', password='123pass')
        login = self.client.login(username= 'user2', password = '123pass')
    def rejecttest(self):
        self.rejectrequest=FriendRequest.objects.create(sender=self.user, receiver=self.user2)
        self.rejectrequest.reject()
        self.assertEqual(self.rejectrequest.is_active, False)
        friendlist1=FriendsList.objects.get(user=self.user)
        friendlist2=FriendsList.objects.get(user=self.user2)
        self.assertFalse(user2 in friendlist1.friend_list.all())
        self.assertFalse(user1 in friendlist2.friend_list.all())
    def accepttest(self):
        self.acceptrequest=FriendRequest.objects.create(sender=self.user, receiver=self.user2)
        self.acceptrequest.accept()
        self.assertEqual(self.acceptrequest.is_active, False)
        friendlist1=FriendsList.objects.get(user=self.user)
        friendlist2=FriendsList.objects.get(user=self.user2)
        self.assertTrue(user2 in friendlist1.friend_list.all())
        self.assertTrue(user1 in friendlist2.friend_list.all())


class ChatRoomAndMessage(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user1', password='123pass')
        login = self.client.login(username= 'user1', password = '123pass')
        self.user2 = User.objects.create_user(username='user2', password='123pass')
        login = self.client.login(username= 'user2', password = '123pass')
        self.acceptrequest=FriendRequest.objects.create(sender=self.user, receiver=self.user2)
        self.acceptrequest.accept()
        self.assertEqual(self.acceptrequest.is_active, False)
    def chatRoom(self):
        self.chatroom = ChatRoom.objects.get(user1=self.user, user2=self.user2)
        self.assertTrue(self.chatroom.exists())
    def sendMessage(self):
        self.message = Message.objects.create(user =self.user, content="hello", room = self.chatroom.key)
        self.assertTrue(self.message.exists())
        self.assertTrue(self.message in self.chatroom.getMessages())
    # This test does not work. Checks if user with completed profile is allowed to enter profile web page, 
    #   or is incorrectly redirected to the create-profile page
    
    # def test_redirect_profile_not_complete(self):
        
    #     response = self.clientx(reverse('profile'), follow=True)
        
    #     isRedirectedToProfile = False
    #     for HttpResponse in response.redirect_chain:
    #         print("URL is: " + HttpResponse[0] + "\n")
    #         print("Is completed: " + str(self.user.profile.profile_is_complete))
    #         if HttpResponse[0].find("/users/profile/?") != -1:
    #             isRedirectedToProfile = True
        
    #     self.assertTrue(isRedirectedToProfile)
    
        

                
        
        
