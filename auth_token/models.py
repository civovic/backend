from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import CIEmailField

GENDER_MALE = 'F'
GENDER_FEMALE = 'M'
GENDER_CHOICES = (
    (GENDER_MALE, 'Male'),
    (GENDER_FEMALE, 'Female')
)


# Create your models here.
class User(AbstractUser):
    # pass
    email = models.EmailField(
        _("email address"),
        unique=True,
        error_messages={
            "unique": _("A user with that email address already exists."),
        },
    )
    mobile_phone_number = models.CharField(max_length=20, unique=True)
    birth_date = models.DateTimeField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)


