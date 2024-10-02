from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer as BaseUserSerializer
from rest_framework import serializers
from core.constants import LANGUAGES, Role
from .models import Profile, User


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['role', 'phone_number', 'street', 'city', 'languages']

    """
    # we are not use in our profile creation , instead we use the direct Profile.objects.create method
    def create(self, validated_data):
        user = self.context.get('user')
        if not user:
            raise ValueError("User must be provided in the context")
        return Profile.objects.create(user=user, **validated_data)
    """


class CusUserCreateSerializer(BaseUserCreateSerializer):
    # Optional profile data during registration
    profile = ProfileSerializer(required=False)

    class Meta(BaseUserCreateSerializer.Meta):
        fields = BaseUserCreateSerializer.Meta.fields + \
            ('first_name', 'last_name', 'profile')

    def create(self, validated_data):
        profile_data = getattr(self, '_profile_data', None)
        # create user
        user = super().create(validated_data)

        profile_validated_data = {'user_id': user.id}
        # If profile data is provided, will validate profile data and update profile_validated_data , else will create default profile with user_id
        if profile_data:
            ps = ProfileSerializer(data=profile_data)
            if ps.is_valid():
                profile_validated_data.update(ps.validated_data)

        Profile.objects.create(**profile_validated_data)

        return user

    def to_internal_value(self, data):
        profile_data = data.pop('profile', None)
        intern = super().to_internal_value(data)
        # store profile data temporarily to access to it in create method
        if profile_data:
            self._profile_data = profile_data

        return intern

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        # serialize the profile n attach it in user json representation
        profile = ProfileSerializer(instance.profile).data if hasattr(
            instance, 'profile') else None
        repr['profile'] = profile
        return repr


class CusUserSerializer(BaseUserSerializer):
    profile = ProfileSerializer()

    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'username', 'email',
                  'first_name', 'last_name', 'profile']

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)
        user_instance = super().update(instance, validated_data)

        # Update or create profile if profile data is provided
        if profile_data:
            profile, created = Profile.objects.get_or_create(
                user=user_instance
            )
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()

        return user_instance

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        profile = ProfileSerializer(instance.profile).data
        repr['profile'] = profile
        return repr
