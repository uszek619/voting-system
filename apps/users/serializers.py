from rest_framework import serializers
from .models import CustomUser, UserBody, UserCadence
from django.core.mail import send_mail
from django.conf import settings

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'role', 'organization', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']


class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'first_name', 'last_name', 'password', 'role', 'organization']
    
    def create(self, validated_data):
        email = validated_data['email']
        
        # Generate password if not provided
        if 'password' not in validated_data:
            password = CustomUser.generate_password()
            validated_data['password'] = password
        else:
            password = validated_data.pop('password')
        
        # Create user
        user = CustomUser.objects.create_user(**validated_data)
        user.set_password(password)
        user.created_by = self.context['request'].user
        user.save()
        
        # Send email with credentials
        self._send_credentials_email(email, user.username, password)
        
        return user
    
    def _send_credentials_email(self, email, username, password):
        """Send login credentials to user email"""
        subject = 'Powitanie w systemie głosowania!'
        message = f"""
        Witaj w systemie głosowania młodzieżowych rad i organizacji!
        
        Twoje dane logowania:
        Email: {email}
        Login: {username}
        Hasło: {password}
        
        Adres systemu: http://localhost:3000
        
        Zalecamy zmianę hasła po pierwszym logowaniu.
        """
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])


class UserBodySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBody
        fields = ['id', 'user', 'body', 'joined_at']
        read_only_fields = ['id', 'joined_at']


class UserCadenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCadence
        fields = ['id', 'user', 'cadence', 'joined_at']
        read_only_fields = ['id', 'joined_at']