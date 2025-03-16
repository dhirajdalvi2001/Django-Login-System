from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers
from django.contrib.auth.models import User

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        try:
            user = User.objects.get(email=data['email'])
        except User.DoesNotExist:
            raise serializers.ValidationError({"email": "User with this email doesn't exist"})

        if not user.check_password(data['password']):
            raise serializers.ValidationError({"password": "Invalid credentials"})
        if user.is_active == False:
            raise serializers.ValidationError({"email": "User is not a active user, contact system administrator"})
        
        return {
            "user": {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "is_superadmin": user.is_superuser
            },
            "tokens": self.get_tokens_for_user(user),
        }

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)

        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }
    
class RefreshTokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    def validate(self, data):
        try:
            refresh = RefreshToken(data["refresh_token"])
            return {
                "access": str(refresh.access_token)
            }
        except Exception as ex:
            raise serializers.ValidationError("Invalid refresh token")
    
class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def validate(self, data):
        user = None
        try:
            user = User.objects.get(email=data['email'])
        except Exception as ex:
            print("user doesn't exist")
        if user:
            raise serializers.ValidationError({"email":"An account using this email is already created"})
        
        return data

    def create(self, validated_data):
        new_user = User.objects.create_user(**validated_data)
        return new_user
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id","username","email", "is_superuser", "first_name", "last_name", "is_active"]

class UserPatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id","username","email", "is_superuser", "first_name", "last_name", "is_active"]
    
    def validate(self, data):
        try:
            user_id = self.instance.id if self.instance else None
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise serializers.ValidationError({"errors": ["User does not exist"]})
        return data

class UserCreateUpdateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    is_superuser = serializers.BooleanField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    is_active = serializers.BooleanField(default=True)

    class Meta:
        model = User
        fields = ["id","username","email", "is_superuser", "first_name", "last_name", "is_active"]

    def validate(self, data):
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({"email": "User with this email already exists"})
    
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({"username": "User with this username already exists"})
        return data
    
    def create(self, validated_data):
        is_superuser = validated_data["is_superuser"]
        if is_superuser:
            new_user = User.objects.create_superuser(**validated_data)
        else: 
            new_user = User.objects.create_user(**validated_data)
        return new_user

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.is_superuser = validated_data.get('is_superuser', instance.is_superuser)

        instance.save() 
        return instance