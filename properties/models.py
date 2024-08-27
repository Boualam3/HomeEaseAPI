from django.db import models
from django.core.exceptions import ValidationError


def validate_file_size(file):
    max_size_kb = 50
    if file.size > max_size_kb * 1024:
        raise ValidationError(f'Files cannot be larger than {max_size_kb} KB!')

# Create your models here.
class Property(models.Model):
     title = models.CharField(max_length=255)
     slug = models.SlugField()
     description=models.TextField()
     # location  optional
	# price  optional
	# number_of_rooms  optional
	# amenities  optional
     

class PropertyImage(models.Model):
    propertie = models.ForeignKey(
        Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(
        upload_to='upload/images',
        validators=[validate_file_size]
    )

class Collection(models.Model):
    title = models.CharField(max_length=225)
    featured_propertie = models.ForeignKey(
        Property, on_delete=models.SET_NULL, null=True, related_name='featured_in_collections', blank=True
     )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']