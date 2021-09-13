from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from users import views as user_views
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('home.urls')),
    path('chat/', include('chat.urls')),
    path('users/', include ('users.urls')),
    path('santa/', admin.site.urls),
    path('logout/', user_views.logoutView, name='logout'),
    # For Google allauth
    path('accounts/', include('allauth.urls')),
]

# This helper function allows you to "serve user-uploaded media files from MEDIA_ROOT using the django.views.static.serve() view."
#   More info: https://docs.djangoproject.com/en/3.1/howto/static-files/#serving-files-uploaded-by-a-user-during-development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)