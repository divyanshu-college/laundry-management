from rest_framework import serializers
from .models import LaundryBooking, LaundryItem


class LaundryItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = LaundryItem
        fields = [
            'item_type',
            'quantity'
        ]


class LaundryBookingSerializer(serializers.ModelSerializer):

    items = LaundryItemSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = LaundryBooking
        fields = [
            'laundry_id',
            'student',
            'booking_date',
            'total_clothes',
            'status',
            'items'
        ]
        read_only_fields = [
            'laundry_id',
            'booking_date',
            'total_clothes',
            'status'
        ]