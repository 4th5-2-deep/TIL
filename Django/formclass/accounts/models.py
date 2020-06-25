from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import Thumbnail
from django.conf import settings


class Profile(models.Model):
    nickname = models.CharField(max_length=20, blank=True)
    image = ProcessedImageField(
                            blank=True,
                            upload_to='profile/image/',
                            processors=[
                                Thumbnail(300, 300),
                            ],
                            format='png',
                        )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
