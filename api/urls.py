from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import UserRegistrationViewSet, EventViewSet, UserProfileViewSet

router = SimpleRouter(trailing_slash=False)
router.register(r'register', UserRegistrationViewSet, basename='user-register')
router.register(r'events', EventViewSet, basename='events')
router.register(r'profile', UserProfileViewSet, basename='profile')

urlpatterns = [
    path('', include(router.urls)),
]