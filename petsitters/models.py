from django.db   import models

from core.models import TimeStampModel

class Petsitter(TimeStampModel):
    name        = models.CharField(max_length=45)
    title       = models.CharField(max_length=150)
    price       = models.DecimalField(max_digits=8, decimal_places=2)
    grade       = models.CharField(max_length=45)
    information = models.TextField(max_length=2000)
    address     = models.CharField(max_length=100)
    longitude   = models.DecimalField(max_digits=9, decimal_places=6)
    latitude    = models.DecimalField(max_digits=9, decimal_places=6)
    types       = models.ManyToManyField('Type', through='PetsitterType')

    class Meta:
        db_table = 'petsitters'

class PetsitterImage(models.Model):
    petsitter_image_url = models.CharField(max_length=1000)
    petsitter_id        = models.ForeignKey('petsitter', on_delete=models.CASCADE)

    class Meta:
        db_table = 'petsitter_images'

class Type(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'types'

class PetsitterType(models.Model):
    petsitter_id = models.ForeignKey('Petsitter', on_delete=models.CASCADE)
    type_id      = models.ForeignKey('Type', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'petsitter_types'

class Comment(TimeStampModel):
    content      = models.CharField(max_length=1000, blank=True)
    user_id      = models.ForeignKey('users.User', on_delete=models.CASCADE)
    petsitter_id = models.ForeignKey('Petsitter', on_delete=models.CASCADE)

    class Meta:
        db_table = 'comments' 