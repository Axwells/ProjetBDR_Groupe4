from django.shortcuts import render
from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Brand, AppUser, Car
from django.http import HttpResponse
from .serializers import BrandSerializer, RegisterSerializer, LoginSerializer, CarSerializer
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


class CarsByBrandView(APIView):
    def get(self, request, brand_name):
        # Requête SQL brute avec INNER JOIN
        query = """
            SELECT 
                c."modelName" AS modelName,
                c."numberOfSeats" AS numberOfSeats,
                c."releaseDate" AS releaseDate,
                c."defaultPrice" AS defaultPrice,
                c."nameBrand" AS nameBrand,
                i."id" AS image_id,
                i."image" AS image_path
            FROM 
                "Car" c
            INNER JOIN 
                "Image" i
            ON 
                c."modelName" = i."modelNameCar"
            WHERE 
                c."nameBrand" = %s
        """
        # Exécution de la requête SQL brute
        with connection.cursor() as cursor:
            cursor.execute(query, [brand_name])
            rows = cursor.fetchall()

        # Structuration des résultats
        cars = {}
        for row in rows:
            model_name = row[0]
            if model_name not in cars:
                cars[model_name] = {
                    'modelName': row[0],
                    'numberOfSeats': row[1],
                    'releaseDate': row[2],
                    'defaultPrice': row[3],
                    'nameBrand': row[4],
                    'images': []
                }
            cars[model_name]['images'].append({'id': row[5], 'image': row[6]})

        # Conversion des résultats en liste
        cars_list = list(cars.values())

        return Response(cars_list, status=status.HTTP_200_OK)