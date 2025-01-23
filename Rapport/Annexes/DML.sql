	-- Insertion de marques
	INSERT INTO "Brand" ("name", "image") VALUES 
	('Tesla', 'tesla.jpg'),
	('BMW', 'bmw.jpg'),
	('Audi', 'audi.jpg'),
	('Mercedes', 'mercedes.png'),
	('Toyota', 'toyota.png'),
	('Ford', 'ford.png');
	
	-- Insertion de voitures
	INSERT INTO "Car" ("modelName", "numberOfSeats", "releaseDate", "defaultPrice", "nameBrand") VALUES 
	('Model S', 5, '2016-05-10', 79999.99, 'Tesla'),
	('Model 3', 5, '2019-04-15', 49999.99, 'Tesla'),
	('Model X', 7, '2021-07-10', 89999.99, 'Tesla'),
	('X5', 5, '2020-03-10', 69999.99, 'BMW'),
	('X3', 5, '2018-09-15', 45999.99, 'BMW'),
	('A4', 5, '2018-06-12', 40999.99, 'Audi'),
	('A6', 5, '2021-05-12', 55999.99, 'Audi'),
	('C-Class', 5, '2019-09-22', 41999.99, 'Mercedes'),
	('E-Class', 5, '2022-03-14', 64999.99, 'Mercedes'),
	('Camry', 5, '2021-11-10', 25999.99, 'Toyota'),
	('Corolla', 5, '2018-04-20', 19999.99, 'Toyota'),
	('F-150', 5, '2022-01-05', 35999.99, 'Ford'),
	('Explorer', 7, '2020-06-15', 42999.99, 'Ford');
	
	-- Insertion d'options
	INSERT INTO "Option" ("name") VALUES 
	('Sunroof'), 
	('Heated Seats'), 
	('Navigation System'), 
	('Bluetooth'), 
	('Leather Seats');
	
	-- Assignation d'options aux voitures
	INSERT INTO "Car_Option" ("modelNameCar", "nameOption", "optionPrice") VALUES
	('Model S', 'Sunroof', 1500.00),
	('Model S', 'Navigation System', 2000.00),
	('Model 3', 'Bluetooth', 1000.00),
	('X5', 'Leather Seats', 2500.00),
	('C-Class', 'Heated Seats', 1500.00);
	
	-- Insertion d'images
	INSERT INTO "Image" ("modelNameCar", "image") VALUES
	('Model S', 'tesla_models.jpeg'),
	('Model 3', 'tesla_model3.png'),
	('X5', 'bmw_x5.jpg'),
	('X5', 'bmw_x5_2.jpg'),
	('F-150', 'fordf150.jpg'),
	('Explorer', 'ford_explorer.jpg'),
	('A4', 'a4.png'),
	('A4', 'a4_2.jpg'),
	('A6', 'a6.jpg'),
	('C-Class', 'c_class.jpg'),
	('Camry', 'camry.jpeg'),
	('Corolla', 'corolla.png'),
	('Corolla', 'corolla_2.jpeg'),
	('E-Class', 'e_class.jpg'),
	('E-Class', 'e_class_2.jpg'),
	('Model X', 'model_x.jpg'),
	('X3', 'x3.jpeg');

	-- Insertion de comptes utilisateurs
	INSERT INTO "AppUser" ("email", "username", "password", "isSuperUser") VALUES
	('admin@example.com', 'admin', 'pbkdf2_sha256$870000$sjPkPHCfJ4bCTidg5TT4zH$8ka97apXCgrFHx+QdjoRDfKbsFTQS44v8/ctTnewfBg=', TRUE),
	('user1@example.com', 'user1', 'pbkdf2_sha256$870000$sjPkPHCfJ4bCTidg5TT4zH$8ka97apXCgrFHx+QdjoRDfKbsFTQS44v8/ctTnewfBg=', FALSE),
	('user2@example.com', 'user2', 'pbkdf2_sha256$870000$sjPkPHCfJ4bCTidg5TT4zH$8ka97apXCgrFHx+QdjoRDfKbsFTQS44v8/ctTnewfBg=', FALSE),
	('reviewer@example.com', 'reviewer', 'pbkdf2_sha256$870000$sjPkPHCfJ4bCTidg5TT4zH$8ka97apXCgrFHx+QdjoRDfKbsFTQS44v8/ctTnewfBg=', FALSE);
	
	-- Insertion de catégories
	INSERT INTO "Category" ("name") VALUES 
	('Luxury'),
	('Sport'),
	('SUV'),
	('Electric'),
	('Hybrid');
	
	-- Association de catégories avec utilisateurs
	INSERT INTO "User_Category" ("emailUser", "nameCategory") VALUES
	('admin@example.com', 'Luxury'),
	('user1@example.com', 'Electric'),
	('user2@example.com', 'SUV');
	
	-- Insertion de freins
	INSERT INTO "Brake" ("model", "abs", "price") VALUES
	('ABS Standard', TRUE, 1500.00),
	('ABS Advanced', TRUE, 2000.00),
	('Sport Brakes', TRUE, 3000.00);
	
	-- Insertion de transmissions
	INSERT INTO "Transmission" ("type", "numberOfGears", "drivetrain", "price") VALUES
	('automatic', 8, 'awd', 3000.00),
	('manual', 6, 'rwd', 2000.00),
	('automatic', 10, '4wd', 3500.00),
	('manual', 5, 'fwd', 1800.00);
	
	-- Insertion de performances
	INSERT INTO "Performance" ("maxSpeed", "zeroToHundredTime") VALUES
	(250, 3.2),
	(220, 4.5),
	(200, 6.0),
	(180, 7.5),
	(160, 8.2);
	
	-- Insertion de spécifications
	INSERT INTO "Specification" ("modelNameCar", "idBrake", "idTransmission", "idPerformance") VALUES
	('Model S', 1, 1, 1),
	('Model S', 1, 2, 2),
	('Model 3', 1, 1, 3),
	('Model X', 1, 3, 1),
	('X5', 2, 1, 2),
	('X3', 2, 4, 4),
	('A4', 3, 2, 3),
	('Camry', 2, 4, 5),
	('Explorer', 3, 3, 4),
	('A6', 1, 1, 2),
	('C-Class', 2, 2, 3),
	('E-Class', 3, 1, 2),
	('Corolla', 2, 4, 5),
	('F-150', 3, 3, 4);
	
	-- Insertion de moteurs
	INSERT INTO "Engine" ("modelName", "horsePower", "position", "price", "nameBrand") VALUES
	('Electric Motor Model S', 1020, 'rear', 10000.00, 'Tesla'),
	('Electric Motor Model 3', 450, 'rear', 6000.00, 'Tesla'),
	('Gas Motor X5', 300, 'front', 8000.00, 'BMW'),
	('Gas Motor A4', 250, 'front', 7000.00, 'Audi'),
	('Diesel Motor X3', 190, 'front', 5000.00, 'BMW'),
	('Gas Motor F150', 290, 'front', 7000.00, 'Ford'),
	('Electric Motor Camry', 200, 'front', 8000.00, 'Toyota'),
	('Hybrid Motor Camry', 176, 'front', 9500.00, 'Toyota');

	INSERT INTO "Gas" ("modelNameEngine", "numberOfCylinders", "engineDisplacement") VALUES
	('Gas Motor A4', 4, 2.0),
	('Gas Motor X5', 6, 3.0),
	('Gas Motor F150', 6, 3.5),
	('Diesel Motor X3', 4, 2.2),
	('Hybrid Motor Camry', 4, 1.8);

	INSERT INTO "Electric" ("modelNameEngine", "maxPower", "batteryDistanceCapacity") values
	('Electric Motor Model S', 450, 500),
	('Electric Motor Model 3', 350, 500),
	('Electric Motor Camry', 220, 400),
	('Hybrid Motor Camry', 100, 300);
	
	-- Association moteurs à des spécifications
	INSERT INTO "Specification_Engine" ("idSpecification", "modelNameEngine") VALUES
	(1, 'Electric Motor Model S'),
	(2, 'Electric Motor Model S'),
	(3, 'Electric Motor Model 3'),
	(4, 'Electric Motor Model S'),
	(5, 'Gas Motor X5'),
	(6, 'Diesel Motor X3'),
	(7, 'Gas Motor A4'),
	(8, 'Hybrid Motor Camry'),
	(9, 'Gas Motor X5'),
	(10, 'Gas Motor A4'),
	(11, 'Gas Motor X5'),
	(12, 'Gas Motor X5'),
	(13, 'Hybrid Motor Camry'),
	(14, 'Diesel Motor X3');
	
	-- Insertion de modifications
	INSERT INTO "Modification" ("text", "isAccepted", "modelNameCar", "emailUserSuggests") VALUES
	('Add autopilot to Model S', NULL, 'Model S', 'user1@example.com'),
	('Enhance safety features on X5', NULL, 'X5', 'user2@example.com'),
	('Add sport brakes to A4', NULL, 'A4', 'user1@example.com'),
	('Include hybrid option for Camry', NULL, 'Camry', 'user2@example.com');
	
	-- Insertion de reviews
	INSERT INTO "Review" ("title", "content", "grade", "date", "idSpecification", "emailUser") VALUES
	('Amazing Performance', 'The Model S is incredibly fast and comfortable.', 5, '2023-10-01', 1, 'user1@example.com'),
	('Great Family SUV', 'The X5 is perfect for family trips and handles well.', 4, '2024-01-15', 5, 'user2@example.com'),
	('Efficient and Reliable', 'The Camry hybrid is both fuel-efficient and smooth.', 4, '2024-03-22', 8, 'user1@example.com');