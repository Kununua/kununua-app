from django.db import models

class User(models.Model):
    username = models.CharField(max_length=16, unique=True)
    password = models.CharField(max_length=255)
    name = models.CharField(max_length=40, blank=True)
    surname = models.CharField(max_length=60, blank=True)
    direction = models.CharField(max_length=255, blank=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=13, blank=True)

    def __str__(self):
        return self.username