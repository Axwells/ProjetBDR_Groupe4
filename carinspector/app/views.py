from django.shortcuts import render
from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Brand, AppUser, Car, Specification
from django.http import HttpResponse
from .serializers import BrandSerializer, RegisterSerializer, LoginSerializer, CarSerializer, SpecificationSerializer
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


class SpecificationsByCarView(APIView):
    def get(self, request, model_name_car):
        try:
            with connection.cursor() as cursor:
                # SQL Query to fetch specifications and their associated engines
                query = """
                    SELECT 
                        s."id" AS specification_id,
                        b."id" AS brake_id,
                        b."model" AS brake_model,
                        b."abs" AS brake_abs,
                        b."price" AS brake_price,
                        t."id" AS transmission_id,
                        t."type" AS transmission_type,
                        t."numberOfGears" AS transmission_gears,
                        t."drivetrain" AS transmission_drivetrain,
                        t."price" AS transmission_price,
                        p."id" AS performance_id,
                        p."maxSpeed" AS performance_max_speed,
                        p."zeroToHundredTime" AS performance_zero_to_hundred_time,
                        e."modelName" AS engine_model_name,
                        e."horsePower" AS engine_horse_power,
                        e."position" AS engine_position,
                        e."price" AS engine_price,
                        e."nameBrand" AS engine_brand_name
                    FROM "Specification" s
                    INNER JOIN "Brake" b ON s."idBrake" = b."id"
                    INNER JOIN "Transmission" t ON s."idTransmission" = t."id"
                    INNER JOIN "Performance" p ON s."idPerformance" = p."id"
                    LEFT JOIN "Specification_Engine" se ON s."id" = se."idSpecification"
                    LEFT JOIN "Engine" e ON se."modelNameEngine" = e."modelName"
                    WHERE s."modelNameCar" = %s
                    ORDER BY s."id", e."modelName"  -- Order by specification ID and engine name
                """
                cursor.execute(query, [model_name_car])
                results = cursor.fetchall()

            # If no specifications are found
            if not results:
                return Response({"error": "No specifications found for this car"}, status=status.HTTP_404_NOT_FOUND)

            # Format the results into JSON response
            specifications_dict = {}
            for row in results:
                spec_id = row[0]
                if spec_id not in specifications_dict:
                    specifications_dict[spec_id] = {
                        "id": row[0],
                        "brake": {
                            "id": row[1],
                            "model": row[2],
                            "abs": row[3],
                            "price": row[4]
                        },
                        "transmission": {
                            "id": row[5],
                            "type": row[6],
                            "numberOfGears": row[7],
                            "drivetrain": row[8],
                            "price": row[9]
                        },
                        "performance": {
                            "id": row[10],
                            "maxSpeed": row[11],
                            "zeroToHundredTime": row[12]
                        },
                        "engines": []
                    }
                # Add engine details if present
                if row[13]:
                    specifications_dict[spec_id]["engines"].append({
                        "modelName": row[13],
                        "horsePower": row[14],
                        "position": row[15],
                        "price": row[16],
                        "brandName": row[17]
                    })

            # Convert specifications_dict to a list
            specifications = list(specifications_dict.values())

            return Response(specifications, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CarDetailsView(APIView):
    def get(self, request, model_name_car):
        try:
            with connection.cursor() as cursor:
                query = """
                    SELECT 
                        c."modelName",
                        c."numberOfSeats",
                        c."releaseDate",
                        c."defaultPrice",
                        b."name" AS brand_name,
                        i."image" AS image_path
                    FROM "Car" c
                    INNER JOIN "Brand" b ON c."nameBrand" = b."name"
                    LEFT JOIN "Image" i ON c."modelName" = i."modelNameCar"
                    WHERE c."modelName" = %s
                """
                cursor.execute(query, [model_name_car])
                rows = cursor.fetchall()

            if not rows:
                return Response({"error": "Car not found"}, status=status.HTTP_404_NOT_FOUND)

            car_details = {
                "modelName": rows[0][0],
                "numberOfSeats": rows[0][1],
                "releaseDate": rows[0][2],
                "defaultPrice": rows[0][3],
                "brandName": rows[0][4],
                "images": [{"image": row[5]} for row in rows if row[5]]  # Collect all images
            }

            return Response(car_details, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SearchCarsView(APIView):
    def get(self, request):
        car_name = request.query_params.get("carName", "")
        car_brand = request.query_params.get("carBrand", "")
        car_engine = request.query_params.get("carEngine", "").lower()  # "essence" ou "electrique"
        car_power = request.query_params.get("carPower", None)

        try:
            with connection.cursor() as cursor:
                query = """
                    SELECT DISTINCT c."modelName", c."numberOfSeats", c."releaseDate", 
                                    c."defaultPrice", b."name" AS brandName, i."image"
                    FROM "Car" c
                    LEFT JOIN "Brand" b ON c."nameBrand" = b."name"
                    LEFT JOIN "Image" i ON c."modelName" = i."modelNameCar"
                    LEFT JOIN "Specification" s ON c."modelName" = s."modelNameCar"
                    LEFT JOIN "Specification_Engine" se ON s."id" = se."idSpecification"
                    LEFT JOIN "Engine" e ON se."modelNameEngine" = e."modelName"
                    LEFT JOIN "Gas" g ON e."modelName" = g."modelNameEngine"
                    LEFT JOIN "Electric" el ON e."modelName" = el."modelNameEngine"
                    WHERE (%s = '' OR c."modelName" ILIKE %s)
                      AND (%s = '' OR b."name" ILIKE %s)
                      AND (%s = '' OR (
                          CASE 
                              WHEN g."modelNameEngine" IS NOT NULL THEN 'essence'
                              WHEN el."modelNameEngine" IS NOT NULL THEN 'electrique'
                              ELSE NULL
                          END
                      ) = %s)
                      AND (%s IS NULL OR e."horsePower" >= %s)
                """
                params = [
                    car_name, f"%{car_name}%", 
                    car_brand, f"%{car_brand}%", 
                    car_engine, car_engine, 
                    car_power, car_power
                ]
                cursor.execute(query, params)
                results = cursor.fetchall()

            # Formater les résultats
            cars = {}
            for row in results:
                model_name = row[0]
                if model_name not in cars:
                    cars[model_name] = {
                        "modelName": row[0],
                        "numberOfSeats": row[1],
                        "releaseDate": row[2],
                        "defaultPrice": row[3],
                        "brandName": row[4],
                        "images": [],
                    }
                if row[5]:  # Ajouter l'image si elle existe
                    cars[model_name]["images"].append({"image": row[5]})

            return Response(list(cars.values()), status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
