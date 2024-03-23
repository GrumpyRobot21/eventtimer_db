from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.UserRegistrationView.as_view(), name='user-register'),
    path('events/', views.EventListCreateView.as_view(), name='event-list-create'),
    path('events/<int:pk>/', views.EventRetrieveUpdateDestroyView.as_view(), name='event-retrieve-update-destroy'),
    path('profile/', views.UserProfileView.as_view(), name='user-profile'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),
    path('delete-profile/', views.DeleteProfileView.as_view(), name='delete-profile'),
]