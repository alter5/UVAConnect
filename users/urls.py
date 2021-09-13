from django.urls import path
from users import views as user_views
from django.views.generic import TemplateView

urlpatterns = [
    path('create-profile/', user_views.create_profile, name='create-profile'),
    path('profile/', user_views.profile, name='profile'),
    path('authenticated/', user_views.authenticated, name='authenticated'),
    path('<int:profile_id>/', user_views.profile_detail, name='detail'),
    path('friend_request/', user_views.send_friend_request, name="friend_request"),
    path('accept_friend_request/<friend_request_id>/', user_views.accept_friend_request, name="accept"),
    path('reject_friend_request/<friend_request_id>/', user_views.reject_friend_request, name="reject"),


]
