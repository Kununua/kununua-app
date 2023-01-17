from django.db import models
from django.contrib.auth.models import AbstractUser

class KununuaUser(AbstractUser):
    phone_number = models.CharField(max_length=20, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures', blank=True, null=True)
    
    def __str__(self):
        return f"User[username: {self.username}, first_name: {self.first_name}, last_name: {self.last_name}, email: {self.email}]"