from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Profile
from .serializers import ProfileSerializer


class ProfileDetailView(APIView):
    def get(self, request, pk):
        profile = get_object_or_404(Profile, user_id=pk)

        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
