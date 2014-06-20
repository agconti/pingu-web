# -*- coding: utf-8 -*-
# Import the AbstractUser model
from django.contrib.auth.models import AbstractUser

# Import the basic Django ORM models library
from django.db import models
from PIL import Image
import os

from django.core.files.storage import default_storage as storage


# Subclass AbstractUser
class User(AbstractUser):
    profile_picture = models.ImageField('Profile Picture',
                                        upload_to='avatars',
                                        blank=True)

    def __unicode__(self):
        return self.username
