from django.utils.text import slugify
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from booking.models import Calendar
from booking.serializers import CalendarSerializer
from .models import Category, Property, PropertyImage, Collection, Review

# will use like that `serializer = PropertyImageSerializer(data=image_data, context={'property_id': property.id})`


class PropertyImageSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        property_id = self.context['property_id']

        return PropertyImage.objects.create(property_id=property_id, **validated_data)

    class Meta:
        model = PropertyImage
        fields = ['id', 'image']


"""
FIXME complete the following 
-1- modify create method to handle calendar object like we've do in user&profile
-2- update CalendarSerializer 
-2- add validation in CalendarSerializer
"""


class PropertySerializer(serializers.ModelSerializer):
    calendar = CalendarSerializer(required=False)

    # many list queryset , read only for get request
    images = PropertyImageSerializer(many=True, read_only=True)

    class Meta:
        model = Property
        fields = [
            'id',
            'slug',
            'title',
            'description',
            'property_type',
            'calendar',
            'collection',
            'category',
            'location',
            'price',
            'number_of_bedrooms',
            'number_of_bathrooms',
            'property_size',
            'amenities',
            'images'
        ]
        read_only_fields = ['id', 'slug']

    def validate(self, data):
        hosted_user_id = self.context['hosted_user_id']
        collection = data.get('collection')
        from_date = data.get('from_date')
        to_date = data.get('to_date')

        # check the collection belongs to the host
        if collection and collection.host_id != hosted_user_id:
            raise PermissionDenied(
                detail="You do not have permission to use this collection for the property."
            )

        # # validate to_date , at least one day after from_date
        # if to_date and from_date and to_date <= from_date:
        #     raise serializers.ValidationError({
        #         'to_date': "The 'to_date' must be at least one day after 'from_date'."
        #     })

        return data

    def create(self, validated_data):
        # add host_id to validated data
        validated_data['host_id'] = self.context['hosted_user_id']
        calendar_data = getattr(self, '_calendar', None)
        property = super().create(validated_data)
        if calendar_data:
            calendar = CalendarSerializer(data=calendar_data, context={
                                          'property_id': property.id})
            if calendar.is_valid():
                calendar.create(calendar_data)
        else:
            Calendar.objects.create(property=property)
        return property

    def update(self, instance, validated_data):
        # update slug only when title get changed
        if 'title' in validated_data and validated_data['title'] != instance.title:
            validated_data['slug'] = slugify(validated_data['title'])
        return super().update(instance, validated_data)

    def to_internal_value(self, data):
        calendar_data = data.pop('calendar', None)
        if calendar_data:
            self._calendar = calendar_data
        return super().to_internal_value(data)

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        calendar = CalendarSerializer(instance.calendar).data if hasattr(
            instance, 'calendar') else None
        repr['calendar'] = calendar
        return repr


class SimplePropertySerializer(serializers.ModelSerializer):
    # maybe will add images , then it view as slide in front-end , for now lets keep it simple
    class Meta:
        model = Property
        fields = ['id', 'title', 'price']


class CollectionSerializer(serializers.ModelSerializer):
    # we don't use PropertySerializer  coz we need only fewer data and thats what SimplePropertySerializer do
    featured_property = SimplePropertySerializer(
        read_only=True)  # get a specific property
    # lists all properties in the collection
    properties = SimplePropertySerializer(many=True, read_only=True)

    def validate(self, data):
        hosted_user_id = self.context.get('hosted_user_id')
        # permission denied if the current collection does not belong to the host
        if self.instance and self.instance.host.id != hosted_user_id:
            raise PermissionDenied(
                detail="You do not have permission to perform action on this collection."
            )

        return data

    def create(self, validated_data):
        hosted_user_id = self.context.get('hosted_user_id')
        return Collection.objects.create(host_id=hosted_user_id, **validated_data)

    class Meta:
        model = Collection
        fields = ['id', 'title', 'image', 'featured_property', 'properties']
        extra_kwargs = {'title': {'required': True}}


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title']

# TODO : Host also can add review for the guest so it will like that
# * => Guest for Property (we do  it)
# * => Host for Guest (not yet) but if we use nested route we should override djoser viewset and add it there
# * or we will add separate endpoint (no nested ) for reviews handle both cases with restriction in permissions


class ReviewSerializer(serializers.ModelSerializer):
    reviewer_name = serializers.CharField(read_only=True)

    def validate_rating(self, value):
        if not (1 <= int(value) <= 5):
            raise serializers.ValidationError(
                "Rating must be between 1 and 5.")
        return value

    def validate(self, data):
        # Get the property ID from the context
        property_id = self.context['property_id']
        user_profile_id = self.context['user_profile_id']

        if self.instance:
            return data  # when user update review will pass validation otherwise will check
        # check if  user has already posted a review for a property
        if Review.objects.filter(property_id=property_id, profile_id=user_profile_id).exists():
            raise serializers.ValidationError(
                "You have already posted a review for this property.")

        return data
    # def create(self, validated_data):
    #     property_id = self.context['property_id']
    #     reviewer_name = self.context.get('reviewer_name', 'Unknown')
    #     return Review.objects.create(property_id=property_id, reviewer_name=reviewer_name, **validated_data)

    # it works for both create/update
    def save(self, **kwargs):
        self.validated_data['property_id'] = self.context['property_id']
        self.validated_data['profile_id'] = self.context['user_profile_id']
        self.validated_data['reviewer_name'] = self.context.get(
            'reviewer_name', 'Unknown')
        return super().save(**kwargs)

    class Meta:
        model = Review
        fields = ['id', 'reviewer_name', 'rating', 'description', 'date']
