from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

GENRES = {
    "AC": "Action",
    "BI": "Biography",
    "CO": "Comedy",
    "CR": "Crime",
    "FA": "Fantasy",
    "MY": "Mystery",
    "FI": "Fiction",
    "SA": "Satire",
    "SF": "Sci Fi",
    "DR": "Drama",
    "HR": "Horror",
    "RO": "Romance",
    "TH": "Thriller",
    "WR": "War",
    "HS": "History",
    "AD": "Adventure",
    "AN": "Animation",
    "DC": "Documentary",
    "WE": "Western",
    "PN": "Pornography",
}

# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=32)
    description = models.TextField(max_length=300)
    director = models.CharField(max_length=32, blank=True)
    year_of_release = models.DateTimeField(blank=True, null=True)
    genre = models.CharField(max_length=2, choices=GENRES)
    is_classified_adults_only = models.BooleanField(default=False)

class Rating(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])

    class Meta:
        unique_together = (('user', 'movie'),)
        #index_together = (('user', 'movie'),)
