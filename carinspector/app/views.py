from django.shortcuts import render
from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Brand, AppUser
from django.http import HttpResponse
from .serializers import BrandSerializer, RegisterSerializer, LoginSerializer
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

# from app.mixins import ModelViewSet #soit on le crée soit ça tej

# from rest_framework import mixins

#résoudre import


# class BrandViewSet(ModelViewSet):
#     serializer_class = None
#     permission_classes = (None,)
#     queryset = Brand.objects.all()

#     def get_queryset(self):
#         queryset = super().get_queryset()
#         return queryset

# def brands(request):
#     brands = Brand.objects.all()
#     return render(request, 'app/brands.html', {'brands': brands})

class BrandListView(APIView):
    def get(self, request):
        brands = Brand.objects.raw('SELECT * FROM "Brand"')

        data = [{'name': brand.name, 'image': brand.image} for brand in brands]

        return Response(data)


class RegisterView(APIView):
    def post(self, request):
        email = request.data.get('email')
        username = request.data.get('username')
        password = request.data.get('password')

        # Vérifiez si l'email ou le nom d'utilisateur existent déjà
        if AppUser.objects.filter(email=email).exists():
            return Response({"detail": "Cet email est déjà utilisé."}, status=status.HTTP_400_BAD_REQUEST)
        if AppUser.objects.filter(username=username).exists():
            return Response({"detail": "Ce nom d'utilisateur est déjà pris."}, status=status.HTTP_400_BAD_REQUEST)

        # Créer un nouvel utilisateur
        user = AppUser.objects.create_user(email=email, username=username, password=password)
        user.save()

        return Response({"message": "Utilisateur créé avec succès."}, status=status.HTTP_201_CREATED)



class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        # Debugging
        print(f"Email: {email}, Password: {password}")

        # Authentification
        user = authenticate(request, username=email, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'username': user.username  # Include the username in the response
            })
        else:
            print("Authentication failed")
            return Response({'non_field_errors': ['Invalid email or password']}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'Successfully logged out'}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
