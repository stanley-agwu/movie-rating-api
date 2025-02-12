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
    is_classified_adult_view = models.BooleanField(default=False)

    def num_of_ratings(self):
        ratings = Rating.objects.filter(movie=self)
        return len(ratings)

    def avg_ratings(self):
        ratings = Rating.objects.filter(movie=self)
        cum_ratings = 0
        for rating in ratings:
            cum_ratings += rating.rating
        return 0 if cum_ratings < 1 else cum_ratings / len(ratings)

    def __str__(self):
        return self.title

class Rating(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])

    class Meta:
        unique_together = (('user', 'movie'),)
