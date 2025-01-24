DROP TABLE IF EXISTS "Brand" CASCADE;
CREATE TABLE "Brand"(
	"name" VARCHAR(50),
	"image" VARCHAR(1030),
	CONSTRAINT "PK_Brand" PRIMARY KEY("name")
);

DROP TABLE IF EXISTS "Car" CASCADE;
CREATE TABLE "Car"(
	"modelName" VARCHAR(80),
	"numberOfSeats" INT NOT NULL,
	"releaseDate" DATE NOT NULL,
	"defaultPrice" DECIMAL(12,2) NOT NULL,
	"nameBrand" VARCHAR(50) NOT NULL,
	CONSTRAINT "PK_Car" PRIMARY KEY("modelName"),
	CONSTRAINT "FK_Car_nameBrand" FOREIGN KEY ("nameBrand") REFERENCES "Brand"("name") ON UPDATE CASCADE ON DELETE RESTRICT,
	CONSTRAINT "CK_Car_numberOfSeats" CHECK ("numberOfSeats" >= 1),
	CONSTRAINT "CK_Car_releaseDate" CHECK ("releaseDate" <= CURRENT_DATE),
	CONSTRAINT "CK_Car_defaultPrice" CHECK ("defaultPrice" > 0)
);

DROP TABLE IF EXISTS "Option" CASCADE;
CREATE TABLE "Option"(
	"name" VARCHAR(100),
	CONSTRAINT "PK_Option" PRIMARY KEY("name")
);

DROP TABLE IF EXISTS "Car_Option";
CREATE TABLE "Car_Option"(
	"modelNameCar" VARCHAR(80),
	"nameOption" VARCHAR(100),
	"optionPrice" DECIMAL(7,2) NOT NULL,
	CONSTRAINT "PK_Car_Option" PRIMARY KEY("modelNameCar", "nameOption"),
	CONSTRAINT "FK_Car_Option_nameOption" FOREIGN KEY ("nameOption") REFERENCES "Option"("name") ON UPDATE CASCADE ON DELETE CASCADE,
	CONSTRAINT "FK_Car_modelNameCar" FOREIGN KEY ("modelNameCar") REFERENCES "Car"("modelName") ON UPDATE CASCADE ON DELETE CASCADE,
	CONSTRAINT "CK_Car_Option_optionPrice" CHECK ("optionPrice" >= 0)
);

DROP TABLE IF EXISTS "Image";
CREATE TABLE "Image"(
	"modelNameCar" VARCHAR(80),
	"image" VARCHAR(1030),
	CONSTRAINT "PK_Image" PRIMARY KEY("modelNameCar", "image"),
	CONSTRAINT "FK_Image_modelNameCar" FOREIGN KEY ("modelNameCar") REFERENCES "Car"("modelName") ON UPDATE CASCADE ON DELETE CASCADE
);

DROP TABLE IF EXISTS "AppUser" CASCADE;
CREATE TABLE "AppUser"(
	"email" VARCHAR(320),
	"username" VARCHAR(80) NOT NULL,
	"password" VARCHAR(128) NOT NULL,
	"isSuperUser" BOOLEAN NOT NULL DEFAULT FALSE,
	"last_login" VARCHAR(10) DEFAULT NULL,
	CONSTRAINT "PK_User" PRIMARY KEY("email")
);

DROP TABLE IF EXISTS "Modification";
CREATE TABLE "Modification"(
	"id" SERIAL,
	"text" VARCHAR(500) NOT NULL,
	"isAccepted" BOOLEAN,
	"modelNameCar" VARCHAR(80) NOT NULL,
	"emailUserSuggests" VARCHAR(320),
	"emailUserManages" VARCHAR(320),
	CONSTRAINT "PK_Modification" PRIMARY KEY ("id"),
	CONSTRAINT "FK_Modification_modelNameCar" FOREIGN KEY ("modelNameCar") REFERENCES "Car"("modelName") ON UPDATE CASCADE ON DELETE CASCADE,
	CONSTRAINT "FK_Modification_emailUserSuggests" FOREIGN KEY ("emailUserSuggests") REFERENCES "AppUser"("email") ON UPDATE CASCADE ON DELETE SET NULL,
	CONSTRAINT "FK_Modification_emailUserManages" FOREIGN KEY ("emailUserManages") REFERENCES "AppUser"("email") ON UPDATE CASCADE ON DELETE SET NULL
);

DROP TABLE IF EXISTS "Category" CASCADE;
CREATE TABLE "Category"(
	"name" VARCHAR(80),
	CONSTRAINT "PK_Category" PRIMARY KEY ("name")
);

DROP TABLE IF EXISTS "User_Category";
CREATE TABLE "User_Category"(
	"emailUser" VARCHAR(320),
	"nameCategory" VARCHAR(80),
	CONSTRAINT "PK_User_Category" PRIMARY KEY ("emailUser", "nameCategory"),
	CONSTRAINT "FK_User_Category_emailUser" FOREIGN KEY ("emailUser") REFERENCES "AppUser"("email") ON UPDATE CASCADE ON DELETE CASCADE,
	CONSTRAINT "FK_User_Category_nameCategory" FOREIGN KEY ("nameCategory") REFERENCES "Category"("name") ON UPDATE CASCADE ON DELETE CASCADE
);

DROP TABLE IF EXISTS "Performance" CASCADE;
CREATE TABLE "Performance"(
	"id" SERIAL,
	"maxSpeed" INT NOT NULL,
	"zeroToHundredTime" DECIMAL(4,2) NOT NULL,
	CONSTRAINT "PK_Performance" PRIMARY KEY ("id"),
	CONSTRAINT "CK_Performance_maxSpeed" CHECK ("maxSpeed" > 0 AND "maxSpeed" <= 600),
	CONSTRAINT "CK_Performance_zeroToHundredTime" CHECK ("zeroToHundredTime" > 0)
);

DROP TYPE IF EXISTS "POSITION_ENUM" CASCADE;
CREATE TYPE "POSITION_ENUM" AS ENUM('front', 'middle', 'rear', 'underfloor');

DROP TABLE IF EXISTS "Engine" CASCADE;
CREATE TABLE "Engine"(
	"modelName" VARCHAR(80),
	"horsePower" INT NOT NULL,
	"position" "POSITION_ENUM" NOT NULL,
	"price" DECIMAL(9,2) NOT NULL,
	"nameBrand" VARCHAR(50) NOT NULL,
	CONSTRAINT "PK_Engine" PRIMARY KEY ("modelName"),
	CONSTRAINT "FK_Engine_nameBrand" FOREIGN KEY ("nameBrand") REFERENCES "Brand"("name") ON UPDATE CASCADE ON DELETE RESTRICT,
	CONSTRAINT "CK_Engine_horsePower" CHECK("horsePower" > 0 AND "horsePower" < 3000),
	CONSTRAINT "CK_Engine_price" CHECK("price" > 0)
);

DROP TABLE IF EXISTS "Gas";
CREATE TABLE "Gas"(
	"modelNameEngine" VARCHAR(80),
	"numberOfCylinders" INT NOT NULL,
	"engineDisplacement" DECIMAL(3,1) NOT NULL,
	CONSTRAINT "PK_Gas" PRIMARY KEY ("modelNameEngine"),
	CONSTRAINT "FK_Gas_modelNameEngine" FOREIGN KEY ("modelNameEngine") REFERENCES "Engine"("modelName") ON UPDATE CASCADE ON DELETE CASCADE,
	CONSTRAINT "CK_Gas_numberOfCylinders" CHECK("numberOfCylinders" >= 0 AND "numberOfCylinders" <= 18)
);

DROP TABLE IF EXISTS "Electric";
CREATE TABLE "Electric"(
	"modelNameEngine" VARCHAR(80),
	"maxPower" INT NOT NULL,
	"batteryDistanceCapacity" INT NOT NULL,
	CONSTRAINT "PK_Electric" PRIMARY KEY ("modelNameEngine"),
	CONSTRAINT "FK_Electric_modelNameEngine" FOREIGN KEY ("modelNameEngine") REFERENCES "Engine"("modelName") ON UPDATE CASCADE ON DELETE CASCADE,
	CONSTRAINT "CK_Electric_maxPower" CHECK("maxPower" > 0),
	CONSTRAINT "CK_Electric_batteryDistanceCapacity" CHECK("batteryDistanceCapacity" > 0)    
);

DROP TYPE IF EXISTS "TRANSMISSION_TYPE_ENUM" CASCADE;
DROP TYPE IF EXISTS "DRIVETRAIN_ENUM" CASCADE;
CREATE TYPE "TRANSMISSION_TYPE_ENUM" AS ENUM('automatic', 'manual');
CREATE TYPE "DRIVETRAIN_ENUM" AS ENUM('rwd', 'fwd', 'awd', '4wd');

DROP TABLE IF EXISTS "Transmission" CASCADE;
CREATE TABLE "Transmission"(
	"id" SERIAL,
	"type" "TRANSMISSION_TYPE_ENUM" NOT NULL,
	"numberOfGears" INT NOT NULL,
	"drivetrain" "DRIVETRAIN_ENUM" NOT NULL,
	"price" DECIMAL(8,2) NOT NULL,
	CONSTRAINT "PK_Transmission" PRIMARY KEY ("id"),
	CONSTRAINT "CK_Transmission_numberOfGears" CHECK("numberOfGears" > 0 AND "numberOfGears" <= 10),
	CONSTRAINT "CK_Transmission_price" CHECK("price" > 0)
);

DROP TABLE IF EXISTS "Brake" CASCADE;
CREATE TABLE "Brake"(
	"id" SERIAL,
	"model" VARCHAR(80) NOT NULL,
	"abs" BOOLEAN NOT NULL,
	"price" DECIMAL(7,2) NOT NULL,
	CONSTRAINT "PK_Brake" PRIMARY KEY ("id"),
	CONSTRAINT "CK_Brake_price" CHECK("price" > 0)
);

DROP TABLE IF EXISTS "Specification" CASCADE;
CREATE TABLE "Specification"(
	"id" SERIAL,
	"modelNameCar" VARCHAR(80) NOT NULL,
	"idBrake" INT NOT NULL,
	"idTransmission" INT NOT NULL,
	"idPerformance" INT NOT NULL,
	CONSTRAINT "PK_Specification" PRIMARY KEY ("id"),
	CONSTRAINT "FK_Specification_modelNameCar" FOREIGN KEY ("modelNameCar") REFERENCES "Car"("modelName") ON UPDATE CASCADE ON DELETE CASCADE,
	CONSTRAINT "FK_Specification_idBrake" FOREIGN KEY ("idBrake") REFERENCES "Brake"("id") ON UPDATE CASCADE ON DELETE RESTRICT,
	CONSTRAINT "FK_Specification_idTransmission" FOREIGN KEY ("idTransmission") REFERENCES "Transmission"("id") ON UPDATE CASCADE ON DELETE RESTRICT,
	CONSTRAINT "FK_Specification_idPerformance" FOREIGN KEY ("idPerformance") REFERENCES "Performance"("id") ON UPDATE CASCADE ON DELETE RESTRICT
);

DROP TABLE IF EXISTS "Specification_Engine";
CREATE TABLE "Specification_Engine"(
	"idSpecification" SERIAL,
	"modelNameEngine" VARCHAR(80) NOT NULL,
	CONSTRAINT "PK_Specification_Engine" PRIMARY KEY ("idSpecification", "modelNameEngine"),
	CONSTRAINT "FK_Specification_Engine_idSpecification" FOREIGN KEY ("idSpecification") REFERENCES "Specification"("id") ON UPDATE CASCADE ON DELETE CASCADE,
	CONSTRAINT "FK_Specification_Engine_modelNameEngine" FOREIGN KEY ("modelNameEngine") REFERENCES "Engine"("modelName") ON UPDATE CASCADE ON DELETE RESTRICT
);

DROP TABLE IF EXISTS "Review";
CREATE TABLE "Review"(
	"id" SERIAL,
	"title" VARCHAR(30) NOT NULL,
	"content" VARCHAR (1000),
	"grade" INT NOT NULL,
	"date" DATE NOT NULL,
	"idSpecification" INT NOT NULL,
	"emailUser" VARCHAR(320) NOT NULL,
	CONSTRAINT "PK_Review" PRIMARY KEY ("id"),
	CONSTRAINT "FK_Review_idSpecification" FOREIGN KEY ("idSpecification") REFERENCES "Specification"("id") ON UPDATE CASCADE ON DELETE CASCADE,
	CONSTRAINT "FK_Review_emailUser" FOREIGN KEY ("emailUser") REFERENCES "AppUser"("email") ON UPDATE CASCADE ON DELETE CASCADE,
	CONSTRAINT "CK_Review_grade" CHECK("grade" > 0 AND "grade" <= 5),
	CONSTRAINT "CK_Review_date" CHECK("date" <= CURRENT_DATE)
);

DROP TABLE IF EXISTS "Category_Specification";
CREATE TABLE "Category_Specification"(
	"nameCategory" VARCHAR(80),
	"idSpecification" INT,
	CONSTRAINT "PK_Category_Specification" PRIMARY KEY ("idSpecification", "nameCategory"),
	CONSTRAINT "FK_Category_Specification_nameCategory" FOREIGN KEY ("nameCategory") REFERENCES "Category"("name") ON UPDATE CASCADE ON DELETE CASCADE,
	CONSTRAINT "FK_Category_Specification_idSpecification" FOREIGN KEY ("idSpecification") REFERENCES "Specification"("id") ON UPDATE CASCADE ON DELETE CASCADE
);
