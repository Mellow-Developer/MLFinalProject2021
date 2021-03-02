import datetime
from django.contrib.auth.models import AbstractUser
from django.db import models


class Listing(models.Model):
    title = models.CharField(max_length=64)
    long_title = models.CharField(max_length=128)
    toxicity = models.TextField()


class Comment(models.Model):
    listing_id = models.IntegerField(default=0)
    user_id = models.ForeignKey(Listing, on_delete=models.CASCADE)
    comment = models.TextField()
    cm_time = models.DateTimeField(default=datetime.datetime.today())
