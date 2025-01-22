from rest_framework import serializers
from .models import Listing, Booking
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from rest_framework.exceptions import ValidationError
from django.utils import timezone
    
class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = ['listing_id', 'host_id', 'name', 'description', 'location', 'price_per_night', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
        
class BookingSerializer(serializers.ModelSerializer):
    total_price = serializers.ReadOnlyField()
    listing_name = serializers.CharField(source='listing_id.name', read_only=True)
    class Meta:
        model = Booking
        fields = ['booking_id', 'listing_name', 'user_id', 'start_date', 'end_date', 'total_price', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at', 'total_price']
        
    def validate(self, data):
        # Check if the start_date is before the end_date
        if data['start_date'] > data['end_date']:
            raise ValidationError('Start date must be before the end date')
        # Check if the dates are in the past
        if data['start_date'] < timezone.now().date() or data['end_date'] < timezone.now().date():
            raise ValidationError('Dates cannot be in the past')
        return data
    
    