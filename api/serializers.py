from rest_framework import serializers
from .models import User, Event
import logging

class UserSerializer(serializers.ModelSerializer):
    logger = logging.getLogger(__name__)
    password = serializers.CharField(write_only=True)
    name = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'name')

    def create(self, validated_data):
        self.logger.debug(f"Creating user with data: {validated_data}")
        email = validated_data['email']
        username = email.split('@')[0]  # Extract the username from the email
        user = User.objects.create_user(
            username=username,
            email=email,
            password=validated_data['password'],
            name=validated_data['name']
        )
        self.logger.debug(f"User created: {user}")
        return user

class EventSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Event
        fields = ('id', 'eventCategory', 'details', 'duration', 'user', 'created_at')


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'email')

class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_current_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Current password is incorrect')
        return value