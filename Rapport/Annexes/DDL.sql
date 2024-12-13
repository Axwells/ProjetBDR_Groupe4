drop table if exists Brand cascade;
create table Brand(
	name VARCHAR(50),
	image VARCHAR(1030),
	constraint PK_Brand primary key(name)
);

drop table if exists Car cascade;
create table Car(
	modelName VARCHAR(80),
	numberOfSeats INT not NULL,
	releaseDate DATE not NULL,
	defaultPrice DECIMAL(12,2) not NULL,
	nameBrand VARCHAR(50) not null,
	constraint PK_Car primary key(modelName),
	constraint FK_Car_nameBrand foreign key (nameBrand) references Brand(name) on update cascade on delete restrict,
	constraint CK_Car_numberOfSeats check (numberOfSeats >= 1),
	constraint CK_Car_releaseDate check (releaseDate <= CURRENT_DATE),
	constraint CK_Car_defaultPrice check (defaultPrice > 0)
);

drop table if exists option cascade;
create table Option(
	name VARCHAR(100),
	constraint PK_Option primary key(name)
);

drop table if exists Car_Option;
create table Car_Option(
	modelNameCar VARCHAR(80),
	nameOption VARCHAR(100),
	optionPrice DECIMAL(7,2) not NULL,
	constraint PK_Car_Option primary key(modelNameCar, nameOption),
	constraint FK_Car_Option_nameOption foreign key (nameOption) references Option(name) on update cascade on delete cascade,
	constraint FK_Car_modelNameCar foreign key (modelNameCar) references Car(modelName) on update cascade on delete cascade,
	constraint CK_Car_Option_optionPrice check (optionPrice >= 0)
);

drop table if exists Image;
create table Image(
	modelNameCar VARCHAR(80),
	image VARCHAR(1030),
	constraint PK_Image primary key(modelNameCar, image),
	constraint FK_Image_modelNameCar foreign key (modelNameCar) references Car(modelName) on update cascade on delete cascade
);

drop table if exists AppUser cascade;
create table AppUser(
	email VARCHAR(320),
	username VARCHAR(80) not null,
	password VARCHAR(128) not null,
	isSuperUser BOOL not null default false,
	constraint PK_User primary key(email)
);

drop table if exists Modification;
create table Modification(
	id SERIAL,
	text VARCHAR(500) not null,
	isAccepted BOOL,
	modelNameCar VARCHAR(80) not NULL,
	emailUserSuggests VARCHAR(320) not NULL,
	emailUserManages VARCHAR(320),
	constraint PK_Modification primary key (id),
	constraint FK_Modification_modelNameCar foreign key (modelNameCar) references Car(modelName) on update cascade on delete cascade,
	constraint FK_Modification_emailUserSuggests foreign key (emailUserSuggests) references AppUser(email) on update cascade on delete restrict,
	constraint FK_Modification_emailUserManages foreign key (emailUserManages) references AppUser(email) on update cascade on delete restrict
);

drop table if exists Category cascade;
create table Category(
	name VARCHAR(80),
	constraint PK_Category primary key (name)
);

drop table if exists User_Category;
create table User_Category(
	emailUser VARCHAR(320),
	nameCategory VARCHAR(80),
	constraint PK_User_Category primary key (emailUser, nameCategory),
	constraint FK_User_Category_emailUser foreign key (emailUser) references AppUser(email) on update cascade on delete cascade,
	constraint FK_User_Category_nameCategory foreign key (nameCategory) references Category(name) on update cascade on delete cascade
);

DROP TABLE IF EXISTS Performance cascade;
CREATE TABLE Performance(
    id SERIAL,
    maxSpeed INT not null,
    zeroToHundredTime DECIMAL(4,2) not null,
    CONSTRAINT PK_Performance PRIMARY KEY (id),
    constraint CK_Performance_maxSpeed check (maxSpeed > 0 and maxSpeed <= 600),
    constraint CK_Performance_zeroToHundredTime check (zeroToHundredTime > 0)
);

drop type if exists POSITION_ENUM CASCADE;
create type POSITION_ENUM as enum('front', 'middle', 'rear', 'underfloor');

DROP TABLE IF EXISTS Engine cascade;
CREATE TABLE Engine(
    modelName VARCHAR(80),
    horsePower INT not null,
    position POSITION_ENUM not null,
    price DECIMAL(9,2) not null,
    nameBrand VARCHAR(50) NOT NULL,
    CONSTRAINT PK_Engine PRIMARY KEY (modelName),
    CONSTRAINT FK_Engine_nameBrand FOREIGN KEY (nameBrand) REFERENCES Brand(name) on update cascade on delete restrict,
    constraint CK_Engine_horsePower check(horsePower > 0 and horsepower < 3000),
    constraint CK_Engine_price check(price > 0)
);
 
DROP TABLE IF EXISTS Gas;
CREATE TABLE Gas(
    modelNameEngine VARCHAR(80),
    numberOfCylinders INT not null,
    engineDisplacement DECIMAL(3,1) not null,
    CONSTRAINT PK_Gas PRIMARY KEY (modelNameEngine),
    CONSTRAINT FK_Gas_modelNameEngine FOREIGN KEY (modelNameEngine) REFERENCES Engine(modelName) on update cascade on delete cascade,
	constraint CK_Gas_numberOfCylinders check(numberOfCylinders >= 0 and numberOfCylinders <= 18)
);
 
DROP TABLE IF EXISTS Electric;
CREATE TABLE Electric(
    modelNameEngine VARCHAR(80),
    maxPower INT not null,
    batteryDistanceCapacity INT not null,
    CONSTRAINT PK_Electric PRIMARY KEY (modelNameEngine),
    CONSTRAINT FK_Electric_modelNameEngine FOREIGN KEY (modelNameEngine) REFERENCES Engine(modelName) on update cascade on delete cascade,
    constraint CK_Electric_maxPower check(maxPower > 0),
    constraint CK_Electric_batteryDistanceCapacity check(batteryDistanceCapacity > 0)    
);

drop type if exists TRANSMISSION_TYPE_ENUM CASCADE;
drop type if exists DRIVETRAIN_ENUM CASCADE;
CREATE TYPE TRANSMISSION_TYPE_ENUM AS ENUM('automatic', 'manual');
CREATE TYPE DRIVETRAIN_ENUM AS ENUM('rwd', 'fwd', 'awd', '4wd');

DROP TABLE IF EXISTS Transmission cascade;
CREATE TABLE Transmission(
    id SERIAL,
    type TRANSMISSION_TYPE_ENUM not null,
    numberOfGears INT not null,
    drivetrain DRIVETRAIN_ENUM not null,
    price DECIMAL(8,2) not null,
    CONSTRAINT PK_Transmission PRIMARY KEY (id),
    constraint CK_Transmission_numberOfGears check(numberOfGears > 0 and numberOfGears <= 10),
    constraint CK_Transmission_price check(price > 0)
);
 
DROP TABLE IF EXISTS Brake cascade;
CREATE TABLE Brake(
    id SERIAL,
    model VARCHAR(80) not null,
    abs BOOL not null,
    price DECIMAL(7,2) not null,
    CONSTRAINT PK_Brake PRIMARY KEY (id),
    constraint CK_Brake_price check(price > 0)
);
 
DROP TABLE IF EXISTS Specification cascade;
CREATE TABLE Specification(
    id SERIAL,
    modelNameCar VARCHAR(80) NOT NULL,
    idBrake INT NOT NULL,
    idTransmission INT NOT NULL,
    idPerformance INT NOT NULL,
    CONSTRAINT PK_Specification PRIMARY KEY (id),
    CONSTRAINT FK_Specification_modelNameCar FOREIGN KEY (modelNameCar) REFERENCES Car(modelName) on update cascade on delete cascade,
    CONSTRAINT FK_Specification_idBrake FOREIGN KEY (idBrake) REFERENCES Brake(id) on update cascade on delete restrict,
    CONSTRAINT FK_Specification_idTransmission FOREIGN KEY (idTransmission) REFERENCES Transmission(id) on update cascade on delete restrict,
    CONSTRAINT FK_Specification_idPerformance FOREIGN KEY (idPerformance) REFERENCES Performance(id) on update cascade on delete restrict
);
 
DROP TABLE IF EXISTS Specification_Engine;
CREATE TABLE Specification_Engine(
    idSpecification INT,
    modelNameEngine VARCHAR(80),
    CONSTRAINT PK_Specification_Engine PRIMARY KEY (idSpecification, modelNameEngine),
    CONSTRAINT FK_Specification_Engine_idSpecification FOREIGN KEY (idSpecification) REFERENCES Specification(id) on update cascade on delete cascade,
    CONSTRAINT FK_Specification_Engine_modelNameEngine FOREIGN KEY (modelNameEngine) REFERENCES Engine(modelName) on update cascade on delete restrict
);
 
DROP TABLE IF EXISTS Review;
CREATE TABLE Review(
    id SERIAL,
    title VARCHAR(30) not null,
    content VARCHAR (1000),
    grade INT not null,
    date DATE not null,
    idSpecification INT NOT NULL,
    emailUser VARCHAR(320) NOT NULL,
    CONSTRAINT PK_Review PRIMARY KEY (id),
    CONSTRAINT FK_Review_idSpecification FOREIGN KEY (idSpecification) REFERENCES Specification(id) on update cascade on delete cascade,
    CONSTRAINT FK_Review_emailUser FOREIGN KEY (emailUser) REFERENCES AppUser(email) on update cascade on delete restrict,
    constraint CK_Review_grade check(grade > 0 and grade <= 5),
    constraint CK_Review_date check(date <= CURRENT_DATE)
);
 
DROP TABLE IF EXISTS Category_Specification;
CREATE TABLE Category_Specification(
    nameCategory VARCHAR(80),
    idSpecification INT,
    CONSTRAINT PK_Category_Specification PRIMARY KEY (idSpecification, nameCategory),
    CONSTRAINT FK_Category_Specification_nameCategory FOREIGN KEY (nameCategory) REFERENCES Category(name) on update cascade on delete restrict,
    CONSTRAINT FK_Category_Specification_idSpecification FOREIGN KEY (idSpecification) REFERENCES Specification(id) on update cascade on delete cascade
);
