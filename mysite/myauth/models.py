from django.contrib.auth.models import User
from django.db import models


def profile_directory_path(instance: "Profile", filename: str) -> str:
    return f'profiles/pk_{instance.pk}/avatar/{filename}'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    bio = models.TextField(max_length=500, blank=True)
    agreement_accepted = models.BooleanField(default=False)
    avatar = models.ImageField(null=True, blank=True, upload_to=profile_directory_path, default='profiles/default_image.png')

    def __str__(self):
        return f'Profile (pk={self.pk}, name={self.user.username}, user_pk={self.user.pk})'

