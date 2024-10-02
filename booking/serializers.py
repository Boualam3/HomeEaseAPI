from .models import Calendar
from rest_framework.serializers import ModelSerializer



class CalendarSerializer(ModelSerializer):
	class Meta:
		model = Calendar
		fields = '__all__'
     # will follow same way of user & profile implementation  