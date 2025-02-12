from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

from django.contrib.auth.models import User

from movieRaterApi.models import Movie, Rating
from movieRaterApi.serializers import MovieSerializer, RatingSerializer, UserSerializer

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    @action(detail=True, methods=['POST'])
    def rate_movie(self, request, pk=None):
        if 'rating' in request.data:
            movie = Movie.objects.get(id=pk)
            rating = request.data['rating']
            user = request.user

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
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def create(self, *args, **kwargs):
        response = {"message": "rating creation not allowed via this route"}
        return Response(response, status=status.HTTP_403_FORBIDDEN)

    def update(self, *args, **kwargs):
        response = {"message": "rating update not allowed via this route"}
        return Response(response, status=status.HTTP_403_FORBIDDEN)
