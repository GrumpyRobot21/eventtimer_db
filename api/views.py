from django.db.models import Q
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action
from .models import User, Event
from .serializers import UserSerializer, EventSerializer, UserProfileSerializer, ChangePasswordSerializer
import logging

class UserRegistrationViewSet(viewsets.ViewSet):
    logger = logging.getLogger(__name__)
    permission_classes = (permissions.AllowAny,)

    def create(self, request):
        self.logger.debug(f"Received registration request: {request.data}")
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            self.logger.debug("Serializer is valid")
            user = serializer.save()
            self.logger.debug(f"User created: {user}")
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def options(self, request, *args, **kwargs):
        # Handle OPTIONS request for CORS preflight
        return Response(status=status.HTTP_200_OK)

class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = Event.objects.filter(user=self.request.user)
        search_query = self.request.query_params.get('search', None)
        if search_query:
            queryset = queryset.filter(
                Q(eventCategory__icontains=search_query) |
                Q(details__icontains=search_query)
            )
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def options(self, request, *args, **kwargs):
        # Handle OPTIONS request for CORS preflight
        return Response(status=status.HTTP_200_OK)

class UserProfileViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get', 'put'])
    def me(self, request):
        if request.method == 'GET':
            serializer = UserProfileSerializer(request.user)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = UserProfileSerializer(request.user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['put'])
    def change_password(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            request.user.set_password(serializer.data.get('new_password'))
            request.user.save()
            return Response({'status': 'password changed'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['delete'])
    def delete_profile(self, request):
        request.user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def options(self, request, *args, **kwargs):
        # Handle OPTIONS request for CORS preflight
        return Response(status=status.HTTP_200_OK)
