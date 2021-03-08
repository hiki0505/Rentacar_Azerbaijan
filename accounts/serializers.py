from rest_framework import serializers
# from django.contrib.auth.models import User
from django.contrib.auth import authenticate

# User Serializer
from accounts.models import CustomUser
from cars.models import Car
from cars.serializers import CarSerializer


class ValidatePhoneSendOTPSerializer(serializers.Serializer):
    phone = serializers.CharField()


class ValidateOTPSerializer(serializers.Serializer):
    otp = serializers.CharField()


class UserDetailSerializer(serializers.ModelSerializer):

    cars = CarSerializer(many=True, read_only=True)


    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'phone', 'cars']


class UserSerializer(serializers.ModelSerializer):
    cars = serializers.PrimaryKeyRelatedField(many=True, queryset=Car.objects.all())

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'cars')


# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'phone', 'password', 'is_company')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        phone = data['phone']
        if CustomUser.objects.filter(phone=phone).exists():
            raise serializers.ValidationError({'phone': 'User with this phone already exists'})
        return data

    def create(self, validated_data):
        user = CustomUser.objects.create_user(validated_data['username'],
                                              validated_data['phone'],
                                              validated_data['password'],
                                              validated_data['is_company'])
        return user


# Login Serializer

class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = ('id', 'username', 'phone', 'password')
#         extra_kwargs = {'password': {'write_only': True}}
#
#         def create(self, validated_data):
#             user = CustomUser(
#                 username=validated_data['username'],
#                 phone=validated_data['phone']
#             )
#
#             user.set_password(validated_data['password'])
#             user.save()
#
#             return user

class ChangePasswordSerializer(serializers.Serializer):
    """
    Used for both password change (Login required) and
    password reset(No login required but otp required)
    not using modelserializer as this serializer will be used for for two apis
    """

    password_1 = serializers.CharField(required=True)
    # password_1 can be old password or new password
    password_2 = serializers.CharField(required=True)
    # password_2 can be new password or confirm password according to apiview


class ForgetPasswordSerializer(serializers.Serializer):
    """
    Used for resetting password who forget their password via otp varification
    """
    phone = serializers.CharField(required=True)
    password = serializers.CharField(required=True)