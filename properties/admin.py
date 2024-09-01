from django.contrib import admin
from .models import Property, Category, Collection, PropertyImage


admin.site.register(Category)
admin.site.register(Collection)
admin.site.register(PropertyImage)
admin.site.register(Property)
