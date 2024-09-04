
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer as BaseUserSerializer
from rest_framework import serializers
from .models import Profile

# Cus=>Custom , when we use UserSerializer name it made conflict when openapi try to generate docs , so we give it unique name by add Cus ,for both classes


class CusUserCreateSerializer(BaseUserCreateSerializer):

    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'username', 'email',
                  'password', 'first_name', 'last_name',]


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['role', 'phone_number', 'street', 'city', 'zip']


class CusUserSerializer(BaseUserSerializer):
    profile = ProfileSerializer()

    def create(self, validated_data):
        profile_data = validated_data.pop('profile', None)
        user_instance = super().create(validated_data)
        # create profile obj when  profile data is provided
        if profile_data:
            # we might get request sent without any profile data so we used empty dictionary
            Profile.objects.create(user=user_instance, **(profile_data or {}))
        return user_instance

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)
        user_instance = super().update(instance, validated_data)

        # update or create profile if profile data is provided
        if profile_data:
            profile, created = Profile.objects.get_or_create(
                user=user_instance)
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()

        return user_instance

    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'username', 'email',
                  'first_name', 'last_name', 'profile']
