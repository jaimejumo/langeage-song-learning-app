from django.shortcuts import render

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import OrderBy
import random

from song_models.models import Song, SongUser
from .serializers import SongSerializer, SongUserSerializer

# Create your views here

class SongViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Song.objects.all().order_by('id')
    serializer_class = SongSerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['get'])
    def random(self, request):
        songs = Song.objects.all()
        if not songs.exists():
            return Response(
                {'detail': 'No songs available'},
                status=status.HTTP_404_NOT_FOUND
            )
        song = random.choice(list(songs))
        serializer = self.get_serializer(song)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def top(self, request):
        n = request.query_params.get('n', 3)
        try:
            n = int(n)
        except (ValueError, TypeError):
            return Response(
                {'detail': 'Invalid value for n'},
                status=status.HTTP_400_BAD_REQUEST
            )
        songs = Song.objects.all().order_by('-number_times_played')[:n]
        serializer = self.get_serializer(songs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def search(self, request):
        title = request.query_params.get('title', None)
        if title is None:
            return Response(
                {'detail': 'title parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        songs = Song.objects.filter(title__icontains=title)
        if not songs.exists():
            return Response(
                {'detail': 'No songs found'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(songs, many=True)
        return Response(serializer.data)


class SongUserViewSet(viewsets.ModelViewSet):
    serializer_class = SongUserSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        return SongUser.objects.filter(
            user=self.request.user
        ).order_by('id')

    def perform_create(self, serializer):
        song = serializer.validated_data['song']
        user = self.request.user
        existing = SongUser.objects.filter(song=song, user=user).first()
        if existing:
            existing.correct_guesses = serializer.validated_data.get(
                'correct_guesses', existing.correct_guesses)
            existing.wrong_guesses = serializer.validated_data.get(
                'wrong_guesses', existing.wrong_guesses)
            existing.save()
        else:
            serializer.save(user=user)