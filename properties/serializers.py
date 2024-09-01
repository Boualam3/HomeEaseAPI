from rest_framework import serializers
from .models import Category, Property, PropertyImage, Collection

# will use like that `serializer = PropertyImageSerializer(data=image_data, context={'property_id': property.id})`


class PropertyImageSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        property_id = self.context['property_id']

        return PropertyImage.objects.create(property_id=property_id, **validated_data)

    class Meta:
        model = PropertyImage
        fields = ['id', 'image']


class PropertySerializer(serializers.ModelSerializer):
    # many list queryset , read only for get request
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


class SimplePropertySerializer(serializers.ModelSerializer):
    # maybe will add images , then i view as slide in front-end , for now lets keep it simple
    class Meta:
        model = Property
        fields = ['id', 'title', 'price']


class CollectionSerializer(serializers.ModelSerializer):
    # we don't use PropertySerializer  coz we need only fewer data and thats what SimplePropertySerializer do ,
    featured_property = SimplePropertySerializer(
        read_only=True)  # get a specific property
    # lists all properties in the collection
    properties = SimplePropertySerializer(many=True, read_only=True)

    class Meta:
        model = Collection
        fields = ['id', 'title', 'image', 'featured_property', 'properties']
        extra_kwargs = {'title': {'required': True}}


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title']
# class CollectionSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length=255)
