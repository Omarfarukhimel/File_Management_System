from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    auth_token = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    create_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user.username)


class Userprofile(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='profile_pic/', default='default_pic/def.png', null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    phone_number = models.TextField(max_length=20)
    note = models.TextField(max_length=500, null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)
