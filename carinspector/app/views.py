from django.shortcuts import render
from django.db import connection
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Brand, AppUser, Car, Specification, Review, Modification
from .serializers import BrandSerializer, RegisterSerializer, LoginSerializer, CarSerializer, SpecificationSerializer, ReviewSerializer, ModificationSerializer, AppUserSerializer


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

        try:
            with connection.cursor() as cursor:
                # Vérifier si l'email existe déjà
                cursor.execute('SELECT COUNT(*) FROM "AppUser" WHERE "email" = %s', [email])
                if cursor.fetchone()[0] > 0:
                    return Response({"detail": "Cet email est déjà utilisé."}, status=status.HTTP_400_BAD_REQUEST)

                # Vérifier si le username existe déjà
                cursor.execute('SELECT COUNT(*) FROM "AppUser" WHERE "username" = %s', [username])
                if cursor.fetchone()[0] > 0:
                    return Response({"detail": "Ce nom d'utilisateur est déjà pris."}, status=status.HTTP_400_BAD_REQUEST)

                hashed_password = make_password(password)

                cursor.execute(
                    '''
                    INSERT INTO "AppUser" ("email", "username", "password", "isSuperUser")
                    VALUES (%s, %s, %s, %s)
                    ''',
                    [email, username, hashed_password, False]
                )

            return Response({"message": "Utilisateur créé avec succès."}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    'SELECT "email", "username", "password", "isSuperUser" FROM "AppUser" WHERE "email" = %s',
                    [email]
                )
                user_data = cursor.fetchone()

                if user_data:
                    stored_email, stored_username, stored_password, is_super_user = user_data

                    # Vérifier le mot de passe haché
                    if check_password(password, stored_password):
                        # Générer les tokens JWT
                        refresh = RefreshToken.for_user(AppUser(email=stored_email))

                        return Response({
                            'refresh': str(refresh),
                            'access': str(refresh.access_token),
                            'username': stored_username,
                            'email': stored_email,
                            'isSuperUser': is_super_user
                        })

                return Response({'non_field_errors': ['Email ou mot de passe incorrect']}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'Successfully logged out'}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class SpecificationsByCarView(APIView):
    def get(self, request, model_name_car):
        try:
            with connection.cursor() as cursor:
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

            if not results:
                return Response({"error": "No specifications found for this car"}, status=status.HTTP_404_NOT_FOUND)

            # Resultats -> format JSON
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
                if row[13]:
                    specifications_dict[spec_id]["engines"].append({
                        "modelName": row[13],
                        "horsePower": row[14],
                        "position": row[15],
                        "price": row[16],
                        "brandName": row[17]
                    })

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
                "images": [{"image": row[5]} for row in rows if row[5]]
            }

            return Response(car_details, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SearchCarsView(APIView):
    def get(self, request):
        car_name = request.query_params.get("carName", "")
        car_brand = request.query_params.get("carBrand", "")
        car_engine = request.query_params.get("carEngine", "").lower()
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
                if row[5]:
                    cars[model_name]["images"].append({"image": row[5]})

            return Response(list(cars.values()), status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ReviewsBySpecificationView(APIView):
    def get(self, request, spec_id):
        try:
            with connection.cursor() as cursor:
                query = """
                    SELECT r."id", r."title", r."content", r."grade", r."date", u."username"
                    FROM "Review" r
                    INNER JOIN "AppUser" u ON r."emailUser" = u."email"
                    WHERE r."idSpecification" = %s
                """
                cursor.execute(query, [spec_id])
                reviews = cursor.fetchall()

            data = [
                {
                    "id": review[0],
                    "title": review[1],
                    "content": review[2],
                    "grade": review[3],
                    "date": review[4],
                    "username": review[5],
                }
                for review in reviews
            ]

            return Response(data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AddReviewView(APIView):
    def post(self, request):
        try:
            data = request.data
            current_date = now().date()

            if "date" in data and data["date"] > current_date:
                return Response(
                    {"error": "La date de la review ne peut pas être dans le futur."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO "Review" ("title", "content", "grade", "date", "idSpecification", "emailUser")
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING "id"
                    """,
                    [
                        data["title"],
                        data.get("content", ""),
                        data["grade"],
                        current_date,
                        data["idSpecification"],
                        data["emailUser"],
                    ],
                )
                review_id = cursor.fetchone()[0]

                cursor.execute(
                    """
                    SELECT "username" FROM "AppUser" WHERE "email" = %s
                    """,
                    [data["emailUser"]],
                )
                user_data = cursor.fetchone()
                username = user_data[0] if user_data else "Utilisateur inconnu"

            return Response(
                {
                    "id": review_id,
                    "title": data["title"],
                    "content": data.get("content", ""),
                    "grade": data["grade"],
                    "date": current_date,
                    "username": username,
                },
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class AddModificationView(APIView):
    def post(self, request):
        try:
            data = request.data

            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT 1 FROM "Car" WHERE "modelName" = %s
                    """,
                    [data["modelNameCar"]],
                )
                if cursor.fetchone() is None:
                    return Response({"error": "Car not found"}, status=status.HTTP_400_BAD_REQUEST)

            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT 1 FROM "AppUser" WHERE "email" = %s
                    """,
                    [data["emailUserSuggests"]],
                )
                if cursor.fetchone() is None:
                    return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)

            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO "Modification" ("text", "isAccepted", "modelNameCar", "emailUserSuggests", "emailUserManages")
                    VALUES (%s, %s, %s, %s, NULL)
                    RETURNING "id", "text", "isAccepted", "modelNameCar", "emailUserSuggests", "emailUserManages"
                    """,
                    [data["text"], None, data["modelNameCar"], data["emailUserSuggests"]],
                )
                modification = cursor.fetchone()

            return Response(
                {
                    "id": modification[0],
                    "text": modification[1],
                    "isAccepted": modification[2],
                    "modelNameCar": modification[3],
                    "emailUserSuggests": modification[4],
                    "emailUserManages": modification[5],
                },
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class GetModificationsView(APIView):
    def get(self, request):
        try:
            # Récupérer l'email utilisateur depuis les en-têtes de la requete axios
            email = request.headers.get("X-User-Email")
            if not email:
                return Response({"error": "Email utilisateur manquant"}, status=status.HTTP_400_BAD_REQUEST)

            query = """
                SELECT m."id", m."text", m."isAccepted", m."modelNameCar", m."emailUserSuggests", m."emailUserManages"
                FROM "Modification" m
                WHERE m."emailUserManages" IS NULL OR m."emailUserManages" = %s
            """
            with connection.cursor() as cursor:
                cursor.execute(query, [email])
                results = cursor.fetchall()

            modifications = [
                {
                    "id": row[0],
                    "text": row[1],
                    "isAccepted": row[2],
                    "modelNameCar": row[3],
                    "emailUserSuggests": row[4],
                    "emailUserManages": row[5],
                }
                for row in results
            ]

            return Response(modifications, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class UpdateModificationView(APIView):
    def put(self, request, modification_id):
        try:
            # Récupérer l'email utilisateur depuis les en-têtes de la requete axios
            email = request.headers.get("X-User-Email")
            if not email:
                return Response({"error": "Email utilisateur manquant"}, status=status.HTTP_400_BAD_REQUEST)

            data = request.data
            is_accepted = data.get("isAccepted")

            query = """
                UPDATE "Modification"
                SET "isAccepted" = %s, "emailUserManages" = %s
                WHERE "id" = %s
            """
            with connection.cursor() as cursor:
                cursor.execute(query, [is_accepted, email, modification_id])

            return Response({"message": "Modification mise à jour avec succès !"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserListView(APIView):
    def get(self, request):
        try:
            with connection.cursor() as cursor:
                cursor.execute('SELECT "email", "username", "isSuperUser" FROM "AppUser"')
                users = [
                    {"email": row[0], "username": row[1], "isSuperUser": row[2]}
                    for row in cursor.fetchall()
                ]
            return JsonResponse(users, safe=False, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CreateUserView(APIView):
    def post(self, request):
        try:
            email = request.data.get("email")
            username = request.data.get("username")
            password = request.data.get("password")
            is_superuser = request.data.get("isSuperUser", False)

            with connection.cursor() as cursor:
                cursor.execute(
                    '''
                    INSERT INTO "AppUser" ("email", "username", "password", "isSuperUser")
                    VALUES (%s, %s, %s, %s)
                    ''',
                    [email, username, password, is_superuser],
                )
            return JsonResponse({"message": "User created successfully!"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UpdateUserView(APIView):
    def put(self, request, email):
        try:
            username = request.data.get("username")
            is_superuser = request.data.get("isSuperUser")

            with connection.cursor() as cursor:
                cursor.execute(
                    '''
                    UPDATE "AppUser"
                    SET "username" = %s, "isSuperUser" = %s
                    WHERE "email" = %s
                    ''',
                    [username, is_superuser, email],
                )
            return JsonResponse({"message": "User updated successfully!"}, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class DeleteUserView(APIView):
    def delete(self, request, email):
        try:
            with connection.cursor() as cursor:
                cursor.execute('DELETE FROM "AppUser" WHERE "email" = %s', [email])
            return JsonResponse({"message": "User deleted successfully!"}, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
