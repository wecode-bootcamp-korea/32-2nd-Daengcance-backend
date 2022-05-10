from django.db   import models

from core.models import TimeStampModel

class User(TimeStampModel):
    kakao_id = models.BigIntegerField(default=0, unique=True)
    name     = models.CharField(max_length=45, null=True)
    nickname = models.CharField(max_length=45, null=True)
    email    = models.CharField(max_length=100, null=True)
    password = models.CharField(max_length=200, null=True)
    mobile   = models.CharField(max_length=45, null=True)

    class Meta:
        db_table = 'users'
