from django.db import models
from user_auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(default='default_profile.png', upload_to='profile_pictures/', blank=True, null=True)

    def __str__(self):
        return self.user.email
