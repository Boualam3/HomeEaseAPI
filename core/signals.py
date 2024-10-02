# from django.dispatch import receiver

# from core.serializers import ProfileSerializer
# from rest_framework.exceptions import ValidationError
# from .models import Profile

# # from .serializers import UserProfileSerializer
# from djoser.signals import user_registered

# If we wan to use this signal then we need to make request.data dict Mutable for add profile_data into it coz request is immuable object
# @receiver(user_registered)
# def create_user_profile(sender, user, request, **kwargs):

#     profile_data = request.data.get('profile', {})
#     if profile_data:
#         ps = ProfileSerializer(data=profile_data, context={'user': user})

#         if ps.is_valid():
#             ps.save(user=user)
#         else:
#             raise ValidationError(f"Invalid profile data: {ps.errors}")
#     else:
#         # otherwise create profile n associate it with user
#         Profile.objects.create(user=user)
