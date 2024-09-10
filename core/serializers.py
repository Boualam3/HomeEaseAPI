import profile
from django.db import transaction
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer as BaseUserSerializer
from rest_framework import serializers
from .models import Profile, User

# Cus=>Custom , when we use UserSerializer name it made conflict when openapi try to generate docs , so we give it unique name by add Cus ,for both classes


class ProfileSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Profile
        fields = ['user_id', 'role', 'phone_number', 'street', 'city', 'zip']

    def create(self, validated_data):
        user = self.context.get('user')
        if not user:
            raise ValueError("User must be provided in the context")
        return Profile.objects.create(user=user, **validated_data)

# FIXME it is not possible to specify profile.role.HOST in registration coz user still not activated yet
# but its fine with GUEST role , in general the senario should register -> activate -> update role if is HOST otherwise is GUEST by default


class UserProfileSerializer(serializers.Serializer):
    role = serializers.ChoiceField(
        choices=Profile.Role.choices, default=Profile.Role.GUEST)
    phone_number = serializers.CharField(max_length=20, required=False)
    street = serializers.CharField(max_length=225, required=False)
    city = serializers.CharField(max_length=225, required=False)
    zip = serializers.DecimalField(
        max_digits=6, decimal_places=0, required=False)

    def create(self, validated_data):
        user = self.context.get('user')
        if not user:
            raise ValueError("User must be provided in the context")
        return Profile.objects.create(user=user, **validated_data)

    def update(self, instance, validated_data):
        # update profile fields , will not use it just in case we need it
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class CusUserCreateSerializer(BaseUserCreateSerializer):
    profile = UserProfileSerializer(required=False)

    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'username', 'email',
                  'password', 'first_name', 'last_name', 'profile']

    @transaction.atomic
    def create(self, validated_data):
        profile_data = validated_data.pop('profile', None)
        # create the user instance
        user = super().create(validated_data)

        # Create the profile if provided
        if profile_data:
            # pass user in context with creation of user
            ps = ProfileSerializer(data=profile_data, context={'user': user})
            if ps.is_valid():
                ps.create(profile_data)
        else:
            Profile.objects.create(user=user)
            # ProfileSerializer(data=profile_data, context={
            #                   'user': user}).is_valid(raise_exception=True)
            # ProfileSerializer.create(ProfileSerializer(
            #     data=profile_data, context={'user': user}), profile_data)

        return user

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        profile = ProfileSerializer(instance.profile).data
        repr['profile'] = profile
        return repr
    # def create(self, validated_data):
    #     profile_data = validated_data.pop('profile', None)
    #     # profile_obj = Profile.objects.create(user=self.id)
    #     user_instance = super().create(validated_data)
    #     # create profile obj when  profile data is provided
    #     profile_defaults = {
    #         "role": Profile.Role.GUEST,
    #         "phone_number": None,
    #         "street": None,
    #         "city": None,
    #         "zip": None
    #     }
    #     # we might get request sent without any profile data so we used empty dictionary
    #     if profile_data:
    #         profile_defaults.update(profile_data)
    #     Profile.objects.create(
    #         user=user_instance,
    #         **profile_defaults
    #     )
    #     return user_instance


class CusUserSerializer(BaseUserSerializer):
    profile = ProfileSerializer()

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)
        user_instance = super().update(instance, validated_data)

        # update or create profile if profile data is provided
        if profile_data:
            profile, created = Profile.objects.get_or_create(
                user=user_instance
            )
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()

        return user_instance

    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'username', 'email',
                  'first_name', 'last_name', 'profile']
