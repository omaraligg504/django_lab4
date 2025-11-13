from django.db import models

# Create your models here.
class Tag(models.Model):
    user_id=models.IntegerField(null=False)
    movie_id=models.ForeignKey('movies.movie',on_delete=models.CASCADE)
    tag=models.CharField()
    timestamp=models.BigIntegerField()
    class Meta:
        constraints =[
            models.UniqueConstraint(fields=['user_id','movie_id','tag'],name='unique_tag')
        ]