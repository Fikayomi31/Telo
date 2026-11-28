from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import RetrieveAPIView

from .serializers import TailorRegistrationSerializer, TailorLoginSerializer, TailorProfileSerializer


class TailorRegistrationView(generics.CreateAPIView):
    serializer_class = TailorRegistrationSerializer
    permission_classes = [AllowAny]

class TailorLoginView(generics.GenericAPIView):
    serializer_class = TailorLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.validated_data, status=status.HTTP_200_OK)

class TailorProfileView(RetrieveAPIView):
    serializer_class = TailorProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
    
