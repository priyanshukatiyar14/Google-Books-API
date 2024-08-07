from . models import Users
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, UserLoginSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password, check_password
from rest_framework_simplejwt.tokens import RefreshToken,AccessToken

class UserView(ListCreateAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        return Users.objects.all()

    def post(self, request, *args, **kwargs):
        request.data['password'] = make_password(request.data['password'])
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserLoginView(ListCreateAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        try:
            email = request.data.get('email')
            password = request.data.get('password')
            if not email or not password:
                return Response({"error": "email and password are required"}, status=status.HTTP_400_BAD_REQUEST)
            user = Users.objects.filter(email=email).first()
            if not user:
                return Response({"error": "Invalid email"}, status=status.HTTP_400_BAD_REQUEST)
            if not check_password(password, user.password):
                return Response({"error": "Invalid password"}, status=status.HTTP_400_BAD_REQUEST)
            
            access_token = AccessToken.for_user(user)
            refresh_token = RefreshToken.for_user(user)
            return Response({
                "access_token": f"Bearer {str(access_token)}",
                "refresh_token": f"Bearer {str(refresh_token)}",
                "user": UserSerializer(user).data
            })
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

