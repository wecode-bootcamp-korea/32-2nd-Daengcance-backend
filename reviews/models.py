from django.db   import models

from core.models import TimeStampModel

class Review(TimeStampModel):
    title     = models.CharField(max_length=100)
    content   = models.TextField(max_length=2000, blank=True)
    user      = models.ForeignKey('users.User', on_delete=models.CASCADE)
    petsitter = models.ForeignKey('petsitters.Petsitter', on_delete=models.CASCADE)

    class Meta:
        db_table = 'reviews'

class ReviewImage(models.Model):
    review_image_url = models.CharField(max_length=1000)
    review           = models.ForeignKey('Review', on_delete=models.CASCADE)

    class Meta:
        db_table = 'review_images'