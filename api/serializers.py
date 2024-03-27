from rest_framework import serializers
from .models import User, Event

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    name = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'name')

    def create(self, validated_data):
        email = validated_data['email']
        username = email.split('@')[0]  # Extract the username from the email
        user = User.objects.create_user(
            username=username,
            email=email,
            password=validated_data['password'],
            name=validated_data['name']
        )
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