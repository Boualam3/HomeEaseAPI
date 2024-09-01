from turtle import title
from django import forms
from django.contrib import admin
from .models import Property, Category, Collection, PropertyImage


class PropertyAdminForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        property_type = cleaned_data.get('property_type')
        number_of_bedrooms = cleaned_data.get('number_of_bedrooms')
        number_of_bathrooms = cleaned_data.get('number_of_bathrooms')
        category = cleaned_data.get('category')
        collection = cleaned_data.get('collection')

        if not category:
            # Create a default category
            default_category_title = 'Beaches'
            category, created = Category.objects.get_or_create(
                title=default_category_title)
            # Assign the created category to the cleaned_data
            cleaned_data['category'] = category

            # Handle collection creation
        if not collection:
            # Create a default collection
            default_collection_title = 'Summer'
            # Ensure no property is featured in the default collection
            collection, created = Collection.objects.get_or_create(
                title=default_collection_title,
                defaults={'featured_property': None}
            )
            # Assign the created collection to the cleaned_data
            cleaned_data['collection'] = collection
        return cleaned_data

    def save(self, commit=True):
        # Custom logic before saving
        instance = super().save(commit=False)
        # Example of setting a default value
        if not instance.category:
            instance.category, created = Category.objects.get_or_create(
                title='Beaches')
        if not instance.collection:
            instance.collection, created = Collection.objects.get_or_create(
                title='Summer')
        if commit:
            instance.save()
        return instance


# NOTICE: This class just to create property object in Admin interface
class PropertyAdmin(admin.ModelAdmin):
    form = PropertyAdminForm

    def save_model(self, request, obj, form, change):
        # Custom logic before saving
        if not obj.category:
            obj.category, created = Category.objects.get_or_create(
                title='Beaches')
        if not obj.collection:
            obj.collection, created = Collection.objects.get_or_create(
                title='Summer')
        obj.save()


admin.site.register(Category)
admin.site.register(Collection)
admin.site.register(PropertyImage)

admin.site.register(Property, PropertyAdmin)
