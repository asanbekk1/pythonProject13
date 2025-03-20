from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, ConfirmationCode

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            is_active=False  # Пользователь неактивен до подтверждения
        )
        # Генерируем код подтверждения
        code = ConfirmationCode.generate_code()
        ConfirmationCode.objects.create(user=user, code=code)
        return user

class UserConfirmationSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6)

    def validate(self, data):
        code = data.get('code')
        try:
            confirmation_code = ConfirmationCode.objects.get(code=code)
            user = confirmation_code.user
            user.is_active = True  # Активируем пользователя
            user.save()
            confirmation_code.delete()  # Удаляем код после подтверждения
            return user
        except ConfirmationCode.DoesNotExist:
            raise serializers.ValidationError("Invalid confirmation code.")

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username, password=password)
        if user and user.is_active:  # Проверяем, что пользователь активен
            return user
        raise serializers.ValidationError("Invalid credentials or user is not active.")