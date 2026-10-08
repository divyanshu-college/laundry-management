from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from users.models import StudentProfile
import uuid


class LaundryBooking(models.Model):

    STATUS_CHOICES = (
        ('booked', 'Booked'),
        ('received', 'Received'),
        ('washing', 'Washing'),
        ('ready', 'Ready'),
        ('collected', 'Collected'),
    )

    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE
    )

    laundry_id = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
        null=True
    )

    booking_date = models.DateTimeField(auto_now_add=True)

    total_clothes = models.PositiveIntegerField(
        default=0
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='booked'
    )

    def clean(self):

        if self.student_id:

            today = timezone.now().date()

            start_of_week = today - timezone.timedelta(
                days=today.weekday()
            )

            bookings_this_week = LaundryBooking.objects.filter(
                student=self.student,
                booking_date__date__gte=start_of_week
            ).exclude(
                id=self.id
            ).count()

            if bookings_this_week >= 2:
                raise ValidationError(
                    "You can make maximum 2 laundry bookings per week."
                )

    def __str__(self):
        return f"{self.student.user.username} - {self.laundry_id}"


class LaundryItem(models.Model):

    ITEM_CHOICES = (
        ('bedsheet', 'Bedsheet'),
        ('pillow_cover', 'Pillow Cover'),
        ('towel', 'Towel'),
        ('ac_towel', 'AC Towel'),
        ('salwar', 'Salwar'),
        ('kurta', 'Kurta'),
        ('lower_pajama', 'Lower Pajama'),
        ('jacket', 'Jacket'),
        ('sneakers', 'Sneakers'),
        ('jeans', 'Jeans'),
        ('tshirt', 'T-Shirt'),
        ('school_university_pant', 'School/University Pant'),
        ('school_university_shirt', 'School/University Shirt'),
        ('civil_pant', 'Civil Pant'),
        ('civil_shirt', 'Civil Shirt'),
        ('school_sweater', 'School Sweater'),
        ('school_coat', 'School Coat'),
        ('skirt', 'Skirt'),
        ('dupatta', 'Dupatta'),
        ('turban', 'Turban'),
        ('apron', 'Apron'),
        ('white_coat', 'White Coat'),
        ('upper_hoodie', 'Upper Hoodie'),
        ('small_blanket', 'Small Blanket'),
        ('big_blanket', 'Big Blanket'),
    )

    booking = models.ForeignKey(
        LaundryBooking,
        on_delete=models.CASCADE,
        related_name='items'
    )

    item_type = models.CharField(
        max_length=50,
        choices=ITEM_CHOICES
    )

    quantity = models.PositiveIntegerField(
        default=1
    )

    def clean(self):

        total_quantity = self.booking.items.exclude(
            id=self.id
        ).aggregate(
            total=models.Sum('quantity')
        )['total'] or 0

        total_quantity += self.quantity

        if total_quantity > 7:
            raise ValidationError(
                "Maximum 7 clothes are allowed in one laundry booking."
            )

    def save(self, *args, **kwargs):

        self.full_clean()

        super().save(*args, **kwargs)

        total = self.booking.items.aggregate(
            total=models.Sum('quantity')
        )['total'] or 0

        self.booking.total_clothes = total

        self.booking.save(
            update_fields=['total_clothes']
        )

    def delete(self, *args, **kwargs):

        booking = self.booking

        super().delete(*args, **kwargs)

        total = booking.items.aggregate(
            total=models.Sum('quantity')
        )['total'] or 0

        booking.total_clothes = total

        booking.save(
            update_fields=['total_clothes']
        )

    def __str__(self):
        return f"{self.item_type} - {self.quantity}"