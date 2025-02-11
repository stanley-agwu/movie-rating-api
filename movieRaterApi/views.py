from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from django.contrib.auth.models import User

from movieRaterApi.models import Movie, Rating
from movieRaterApi.serializers import MovieSerializer, RatingSerializer

# Create your views here.
class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    @action(detail=True, methods=['POST'])
    def rate_movie(self, request, pk=None):
        if 'rating' in request.data:
            movie = Movie.objects.get(id=pk)
            rating = request.data['rating']
            # user = request.user
            user = User.objects.get(id=1)

            try:
                movie_rating = Rating.objects.get(user=user.id, movie=movie.id)
                movie_rating.rating = rating
                movie_rating.save()
                serializer = RatingSerializer(rating, many=False)
                response = {"message": "movie rating updated successfully", "result": serializer.data}
                return Response(response, status=status.HTTP_200_OK)
            except:
                rating = Rating.objects.create(user=user, movie=movie, rating=rating)
                serializer = RatingSerializer(rating, many=False)
                response = {"message": "movie rating created successfully", "result": serializer.data}
                return Response(response, status=status.HTTP_200_OK)
        else:
            response = {"message": "rating not provided in request"}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)



class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer