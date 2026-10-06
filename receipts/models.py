import qrcode
from django.db import models
from laundry.models import LaundryBooking


class LaundryReceipt(models.Model):

    booking = models.OneToOneField(
        LaundryBooking,
        on_delete=models.CASCADE
    )

    qr_code = models.ImageField(
        upload_to='qr_codes/',
        blank=True,
        null=True
    )

    def save(self, *args, **kwargs):

        qr_data = str(self.booking.laundry_id)

        qr = qrcode.make(qr_data)

        file_name = f"qr_{self.booking.laundry_id}.png"

        from io import BytesIO
        from django.core.files import File

        buffer = BytesIO()
        qr.save(buffer, format='PNG')

        self.qr_code.save(
            file_name,
            File(buffer),
            save=False
        )

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Receipt - {self.booking.laundry_id}"