from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from ..models import Profile
from .serializers import ProfileListSerializer, ProfileSerializer
from .permissions import IsProfileOwner


class ProfileDetailView(APIView):
    permission_classes = [
        IsAuthenticated,
        IsProfileOwner,
    ]

    def get(self, request, pk):
        profile = get_object_or_404(Profile, user_id=pk)
        self.check_object_permissions(
            request,
            profile,
        )
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        profile = get_object_or_404(Profile, user_id=pk)

        self.check_object_permissions(request, profile)

        serializer = ProfileSerializer(profile, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BusinessProfilesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profiles = Profile.objects.filter(type="business")
        serializer = ProfileListSerializer(profiles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CustomerProfilesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profiles = Profile.objects.filter(type="customer")
        serializer = ProfileListSerializer(profiles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
