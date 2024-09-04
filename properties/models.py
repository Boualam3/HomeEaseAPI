from core.models import Profile
from django.utils.text import slugify
from django.db import models
from django.core.exceptions import ValidationError


def validate_file_size(file):
    max_size_kb = 50
    if file.size > max_size_kb * 1024:
        raise ValidationError(f'Files cannot be larger than {max_size_kb} KB!')


class Category(models.Model):
    title = models.CharField(max_length=225)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']


class Collection(models.Model):
    title = models.CharField(max_length=225)
    featured_property = models.ForeignKey(
        'Property', on_delete=models.SET_NULL, null=True, related_name='+', blank=True
    )
    host = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='collections'
    )
    image = models.ImageField(
        upload_to='upload/collection_images/', null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']

# OPTIMIZE: I think about make Abstract Base Model for Property then create specific models for each type that inherit from this base model coz every type that will have many attributes that are not related to other types  and will ended up with lots of attributes in one model


class Property(models.Model):
    class PropertyType(models.TextChoices):
        HOME = 'HOME', 'Home'
        APARTMENT = 'APARTMENT', 'Apartment'
        CABIN = 'CABIN', 'Cabin'
        TENT = 'TENT', 'Tent'
    host = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='properties'
    )
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    property_type = models.CharField(
        max_length=50, choices=PropertyType.choices
    )
    collection = models.ForeignKey(
        Collection, on_delete=models.PROTECT, related_name='properties'
    )
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name='properties', null=True, blank=True
    )

    # TODO location address list , text choices
    location = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # per night
    number_of_bedrooms = models.IntegerField(null=True, blank=True)
    number_of_bathrooms = models.IntegerField(null=True, blank=True)
    property_size = models.IntegerField(
        null=True, blank=True)  # in square feet or meters
    amenities = models.TextField(null=True, blank=True)  # list of amenities
    last_update = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.get_property_type_display()})"


class PropertyImage(models.Model):
    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(
        upload_to='upload/images',
        # validators=[validate_file_size]
    )
