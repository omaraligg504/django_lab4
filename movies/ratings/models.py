from django.db import models
# Create your models here.
class Rating(models.Model):
    user_id=models.IntegerField(null=False)
    movie_id=models.ForeignKey('movies.Movie',on_delete=models.CASCADE)
    rating=models.DecimalField(max_digits=2,decimal_places=1)
    timestamp=models.BigIntegerField()
    class Meta:
       constraints = [
            models.UniqueConstraint(fields=['user_id', 'movie_id'], name='unique_rating')
       ]