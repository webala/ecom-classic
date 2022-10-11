from django.urls import include, path

from users.views import register_user

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('register', register_user, name='register')
]