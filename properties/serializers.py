from rest_framework import serializers
from .models import Property, PropertyImage, Collection

# will use like that `serializer = PropertyImageSerializer(data=image_data, context={'property_id': property.id})`


class PropertyImageSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        property_id = self.context['property_id']

        return PropertyImage.objects.create(property_id=property_id, **validated_data)

    class Meta:
        model = PropertyImage
        fields = ['id', 'image']


class PropertySerializer(serializers.ModelSerializer):
    images = PropertyImageSerializer(many=True, read_only=True)

    class Meta:
        model = Property
        fields = [
            'id',
            'title',
            'slug',
            'description',
            'property_type',
            'collection',
            'location',
            'price',
            'number_of_bedrooms',
            'number_of_bathrooms',
            'property_size',
            'amenities',
            'images'
        ]
        read_only_fields = ['id', 'slug']


class CollectionSerializer(serializers.ModelSerializer):
    featured_property = PropertySerializer(
        read_only=True)  # get a specific property
    # lists all properties in the collection
    properties = PropertySerializer(many=True, read_only=True)

    class Meta:
        model = Collection
        fields = ['id', 'title', 'featured_property', 'properties']
        extra_kwargs = {'title': {'required': True}}

# class CollectionSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length=255)
