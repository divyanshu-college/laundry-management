from django.db import models


class Hostel(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Room(models.Model):
    hostel = models.ForeignKey(
        Hostel,
        on_delete=models.CASCADE
    )

    room_number = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.hostel.name} - {self.room_number}"