# from datetime import timezone
from django.utils import timezone
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models import CheckConstraint, Q, F

class Brand(models.Model):
    name = models.CharField(max_length=50, primary_key=True, db_column="name")
    image = models.CharField(max_length=1030, null=True, blank=True, db_column="image")

    class Meta:
        db_table = "Brand"

class Car(models.Model):
    modelName = models.CharField(max_length=80, primary_key=True, db_column="modelName")
    numberOfSeats = models.PositiveIntegerField(db_column="numberOfSeats")
    releaseDate = models.DateField(db_column="releaseDate")
    defaultPrice = models.DecimalField(max_digits=12, decimal_places=2, db_column="defaultPrice")
    nameBrand = models.ForeignKey(
        Brand,
        on_delete=models.RESTRICT,
        db_column="nameBrand",
        related_name="cars"
    )

    class Meta:
        db_table = "Car"
        constraints = [
            CheckConstraint(
                check=Q(numberOfSeats__gte=1),
                name="CK_Car_numberOfSeats"
            ),
            CheckConstraint(
                check=Q(releaseDate__lte=timezone.now().date()),
                name="CK_Car_releaseDate"
            ),
            CheckConstraint(
                check=Q(defaultPrice__gt=0),
                name="CK_Car_defaultPrice"
            )
        ]

class Option(models.Model):
    name = models.CharField(max_length=100, primary_key=True, db_column="name")

    class Meta:
        db_table = "Option"

class CarOption(models.Model):
    modelNameCar = models.ForeignKey(Car, on_delete=models.CASCADE, db_column="modelNameCar")
    nameOption = models.ForeignKey(Option, on_delete=models.CASCADE, db_column="nameOption")
    optionPrice = models.DecimalField(max_digits=7, decimal_places=2, db_column="optionPrice")

    class Meta:
        db_table = "Car_Option"
        constraints = [
            CheckConstraint(check=Q(optionPrice__gte=0), name="CK_Car_Option_optionPrice")
        ]
        unique_together = (("modelNameCar", "nameOption"),)

class Image(models.Model):
    modelNameCar = models.ForeignKey(Car, on_delete=models.CASCADE, db_column="modelNameCar")
    image = models.CharField(max_length=1030, db_column="image")

    class Meta:
        db_table = "Image"
        unique_together = (("modelNameCar", "image"),)


class AppUser(models.Model):
    email = models.CharField(max_length=320, primary_key=True, db_column="email")
    username = models.CharField(max_length=80, db_column="username")
    password = models.CharField(max_length=80, db_column="password")
    isSuperuser = models.BooleanField(default=False, db_column="isSuperUser")

    class Meta:
        db_table = "AppUser"


class Modification(models.Model):
    id = models.AutoField(primary_key=True, db_column="id")
    text = models.CharField(max_length=500, db_column="text")
    isAccepted = models.BooleanField(null=True, db_column="isAccepted")
    modelNameCar = models.ForeignKey(Car, on_delete=models.CASCADE, db_column="modelNameCar")
    emailUserSuggests = models.ForeignKey(AppUser, on_delete=models.RESTRICT, db_column="emailUserSuggests", related_name="suggestedModifications")
    emailUserManages = models.ForeignKey(AppUser, on_delete=models.RESTRICT, db_column="emailUserManages", related_name="managedModifications")

    class Meta:
        db_table = "Modification"


class Category(models.Model):
    name = models.CharField(max_length=80, primary_key=True, db_column="name")

    class Meta:
        db_table = "Category"


class UserCategory(models.Model):
    emailUser = models.ForeignKey(AppUser, on_delete=models.CASCADE, db_column="emailUser")
    nameCategory = models.ForeignKey(Category, on_delete=models.CASCADE, db_column="nameCategory")

    class Meta:
        db_table = "User_Category"
        unique_together = (("emailUser", "nameCategory"),)


class Performance(models.Model):
    id = models.AutoField(primary_key=True, db_column="id")
    maxSpeed = models.PositiveIntegerField(db_column="maxSpeed")
    zeroToHundredTime = models.DecimalField(max_digits=4, decimal_places=2, db_column="zeroToHundredTime")

    class Meta:
        db_table = "Performance"
        constraints = [
            CheckConstraint(check=Q(maxSpeed__gt=0) & Q(maxSpeed__lte=600), name="CK_Performance_maxSpeed"),
            CheckConstraint(check=Q(zeroToHundredTime__gt=0), name="CK_Performance_zeroToHundredTime"),
        ]

class PositionEnum(models.TextChoices):
    FRONT = "front", "Front"
    MIDDLE = "middle", "Middle"
    REAR = "rear", "Rear"
    UNDERFLOOR = "underfloor", "Underfloor"

class Engine(models.Model):
    modelName = models.CharField(max_length=80, primary_key=True, db_column="modelName")
    horsePower = models.PositiveIntegerField(db_column="horsePower")
    position = models.CharField(max_length=20, choices=PositionEnum.choices, db_column="position")
    price = models.DecimalField(max_digits=9, decimal_places=2, db_column="price")
    nameBrand = models.ForeignKey(Brand, on_delete=models.RESTRICT, db_column="nameBrand")

    class Meta:
        db_table = "Engine"
        constraints = [
            CheckConstraint(check=Q(horsePower__gt=0) & Q(horsePower__lt=3000), name="CK_Engine_horsePower"),
            CheckConstraint(check=Q(price__gt=0), name="CK_Engine_price"),
        ]


class Gas(models.Model):
    modelNameEngine = models.OneToOneField(Engine, on_delete=models.CASCADE, primary_key=True, db_column="modelNameEngine")
    numberOfCylinders = models.PositiveIntegerField(db_column="numberOfCylinders")
    engineDisplacement = models.DecimalField(max_digits=3, decimal_places=1, db_column="engineDisplacement")

    class Meta:
        db_table = "Gas"
        constraints = [
            CheckConstraint(check=Q(numberOfCylinders__gte=0) & Q(numberOfCylinders__lte=18), name="CK_Gas_numberOfCylinders")
        ]

class Electric(models.Model):
    modelNameEngine = models.OneToOneField(Engine, on_delete=models.CASCADE, primary_key=True, db_column="modelNameEngine")
    maxPower = models.PositiveIntegerField(db_column="maxPower")
    batteryDistanceCapacity = models.PositiveIntegerField(db_column="batteryDistanceCapacity")

    class Meta:
        db_table = "Electric"
        constraints = [
            CheckConstraint(check=Q(maxPower__gt=0), name="CK_Electric_maxPower"),
            CheckConstraint(check=Q(batteryDistanceCapacity__gt=0), name="CK_Electric_batteryDistanceCapacity"),
        ]

class TransmissionTypeEnum(models.TextChoices):
    AUTOMATIC = "automatic", "Automatic"
    MANUAL = "manual", "Manual"

class DrivetrainEnum(models.TextChoices):
    RWD = "rwd", "RWD"
    FWD = "fwd", "FWD"
    AWD = "awd", "AWD"
    FOURWD = "4wd", "4WD"

class Transmission(models.Model):
    id = models.AutoField(primary_key=True, db_column="id")
    type = models.CharField(max_length=10, choices=TransmissionTypeEnum.choices, db_column="type")
    numberOfGears = models.PositiveIntegerField(db_column="numberOfGears")
    drivetrain = models.CharField(max_length=5, choices=DrivetrainEnum.choices, db_column="drivetrain")
    price = models.DecimalField(max_digits=8, decimal_places=2, db_column="price")

    class Meta:
        db_table = "Transmission"
        constraints = [
            CheckConstraint(check=Q(numberOfGears__gt=0) & Q(numberOfGears__lte=10), name="CK_Transmission_numberOfGears"),
            CheckConstraint(check=Q(price__gt=0), name="CK_Transmission_price"),
        ]

class Specification(models.Model):
    id = models.AutoField(primary_key=True, db_column="id")
    modelNameCar = models.ForeignKey(Car, on_delete=models.CASCADE, db_column="modelNameCar")
    idBrake = models.ForeignKey("Brake", on_delete=models.RESTRICT, db_column="idBrake")
    idTransmission = models.ForeignKey(Transmission, on_delete=models.RESTRICT, db_column="idTransmission")
    idPerformance = models.ForeignKey(Performance, on_delete=models.RESTRICT, db_column="idPerformance")

    class Meta:
        db_table = "Specification"


class Brake(models.Model):
    id = models.AutoField(primary_key=True, db_column="id")
    model = models.CharField(max_length=80, db_column="model")
    abs = models.BooleanField(db_column="abs")
    price = models.DecimalField(max_digits=7, decimal_places=2, db_column="price")

    class Meta:
        db_table = "Brake"
        constraints = [
            CheckConstraint(check=Q(price__gt=0), name="CK_Brake_price"),
        ]

class SpecificationEngine(models.Model):
    idSpecification = models.ForeignKey("Specification", on_delete=models.CASCADE, db_column="idSpecification")
    modelNameEngine = models.ForeignKey("Engine", on_delete=models.RESTRICT, db_column="modelNameEngine")

    class Meta:
        db_table = "Specification_Engine"
        unique_together = (("idSpecification", "modelNameEngine"),)


class Review(models.Model):
    id = models.AutoField(primary_key=True, db_column="id")
    title = models.CharField(max_length=30, db_column="title")
    content = models.CharField(max_length=1000, null=True, blank=True, db_column="content")
    grade = models.PositiveIntegerField(db_column="grade")
    date = models.DateField(db_column="date")
    idSpecification = models.ForeignKey("Specification", on_delete=models.CASCADE, db_column="idSpecification")
    emailUser = models.ForeignKey("AppUser", on_delete=models.RESTRICT, db_column="emailUser")

    class Meta:
        db_table = "Review"
        constraints = [
            CheckConstraint(check=Q(grade__gt=0) & Q(grade__lte=5), name="CK_Review_grade"),
            CheckConstraint(check=Q(date__lte=timezone.now().date()), name="CK_Review_date"),
        ]


class CategorySpecification(models.Model):
    nameCategory = models.ForeignKey("Category", on_delete=models.RESTRICT, db_column="nameCategory")
    idSpecification = models.ForeignKey("Specification", on_delete=models.CASCADE, db_column="idSpecification")

    class Meta:
        db_table = "Category_Specification"
        unique_together = (("idSpecification", "nameCategory"),)
