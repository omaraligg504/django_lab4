from django.db import models

# Create your models here.
class Link(models.Model):
    movieId=models.IntegerField(primary_key=True)
    imdbId=models.IntegerField(null=True,blank=True)
    tmdbId=models.IntegerField(null=True,blank=True)