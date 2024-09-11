from rest_framework import serializers
from .models import Booking, Order

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'checkin', 'checkout', 'number_guests', 'status', 'property', 'profile']


class OrderSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        booking_id = self.context['booking_id']
        return Order.objects.create(booking_id=booking_id, **validated_data)
    
    class Meta:
        model = Order
        fields = ['id', 'total_amount', 'vat', 'fees', 'discount', 'booking']
    