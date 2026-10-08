from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import LaundryBooking, LaundryItem
from .serializers import LaundryBookingSerializer
from receipts.models import LaundryReceipt


class LaundryBookingCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        # Logged-in student
        student = request.user.studentprofile

        items = request.data.get('items')

        # Items check
        if not items:
            return Response(
                {"error": "Items are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Total clothes calculate
        total_clothes = 0

        for item in items:
            total_clothes += item['quantity']

        # Maximum 7 clothes
        if total_clothes > 7:
            return Response(
                {"error": "Maximum 7 clothes are allowed"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Booking create
        booking = LaundryBooking.objects.create(
            student=student,
            total_clothes=total_clothes
        )

        # Receipt + QR automatically create
        LaundryReceipt.objects.create(
            booking=booking
        )

        # Clothes create
        for item in items:

            LaundryItem.objects.create(
                booking=booking,
                item_type=item['item_type'],
                quantity=item['quantity']
            )

        # Response
        serializer = LaundryBookingSerializer(booking)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


class MyLaundryBookingsView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        # Logged-in student ki profile
        student = request.user.studentprofile

        # Us student ki bookings
        bookings = LaundryBooking.objects.filter(
            student=student
        ).order_by('-booking_date')

        serializer = LaundryBookingSerializer(
            bookings,
            many=True
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )