from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    ROLE_CHOICES=(
        ('student','Student'),
        ('staff','Staff'),
    )

    role=models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='student'
    )

class StudentProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    hostel = models.ForeignKey(
        'hostels.Hostel',
        on_delete=models.CASCADE
    )

    room = models.ForeignKey(
        'hostels.Room',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.user.username


