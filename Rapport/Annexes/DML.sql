-- Brand
INSERT INTO Brand (name, image) VALUES
('Tesla', 'https://example.com/images/tesla.png'),
('Ford', 'https://example.com/images/ford.png'),
('BMW', 'https://example.com/images/bmw.png');

-- Car
INSERT INTO Car (modelName, numberOfSeats, releaseDate, defaultPrice, nameBrand) VALUES
('Model S', 5, '2016-06-22', 79999.99, 'Tesla'),
('F-150', 5, '2018-09-10', 28999.99, 'Ford'),
('X5', 7, '2020-03-15', 59999.99, 'BMW'),
('Model 3', 5, '2021-07-15', 39999.99, 'Tesla'),
('Explorer', 7, '2019-04-20', 35999.99, 'Ford'),
('3 Series', 5, '2022-05-12', 42999.99, 'BMW');

-- Option
INSERT INTO Option (name) VALUES
('Sunroof'),
('Leather Seats'),
('Heated Steering Wheel'),
('Sports Package'),
('Advanced Safety'),
('Premium Audio');

-- Car_Option
INSERT INTO Car_Option (modelNameCar, nameOption, optionPrice) VALUES
('Model S', 'Sunroof', 1000.00),
('F-150', 'Leather Seats', 1500.00),
('X5', 'Heated Steering Wheel', 750.00),
('Model 3', 'Sports Package', 1500.00),
('Explorer', 'Advanced Safety', 2000.00),
('3 Series', 'Premium Audio', 1200.00);

-- Image
INSERT INTO Image (modelNameCar, image) VALUES
('Model S', 'https://example.com/images/model_s.png'),
('F-150', 'https://example.com/images/f150.png'),
('X5', 'https://example.com/images/x5.png'),
('Model 3', 'https://example.com/images/model_3.png'),
('Explorer', 'https://example.com/images/explorer.png'),
('3 Series', 'https://example.com/images/3series.png');

-- AppUser
INSERT INTO AppUser (email, username, password, isSuperUser) VALUES
('user1@example.com', 'user1', 'password123', false),
('admin@example.com', 'admin', 'adminpass', true),
('user2@example.com', 'user2', 'securepass', false);

-- Modification
INSERT INTO Modification (text, isAccepted, modelNameCar, emailUserSuggests, emailUserManages) VALUES
('Add autopilot feature to Model S', true, 'Model S', 'user1@example.com', 'admin@example.com'),
('Improve towing capacity of F-150', false, 'F-150', 'user2@example.com', 'admin@example.com');

-- Category
INSERT INTO Category (name) VALUES
('Luxury'),
('SUV'),
('Electric'),
('Family'),
('Performance');

-- User_Category
INSERT INTO User_Category (emailUser, nameCategory) VALUES
('user1@example.com', 'Electric'),
('user2@example.com', 'SUV');

-- Performance
INSERT INTO Performance (maxSpeed, zeroToHundredTime) VALUES
(250, 2.80),
(180, 6.50),
(220, 4.50),
(240, 3.10),
(210, 7.00),
(230, 5.50);

-- Transmission
INSERT INTO Transmission (type, numberOfGears, drivetrain, price) VALUES
('automatic', 6, 'rwd', 2500.00),
('manual', 5, 'awd', 2000.00),
('automatic', 8, 'fwd', 2800.00),
('automatic', 8, 'awd', 3000.00);

-- Brake
INSERT INTO Brake (model, abs, price) VALUES
('Brembo', true, 1500.00),
('Standard', false, 500.00),
('Performance', true, 2000.00),
('Advanced Brembo', true, 1800.00);

-- Specification
INSERT INTO Specification (modelNameCar, idBrake, idTransmission, idPerformance) VALUES
('Model S', 1, 1, 1),
('F-150', 2, 2, 2),
('X5', 3, 3, 3),
('Model 3', 1, 1, 4),
('Explorer', 2, 3, 5),
('3 Series', 3, 3, 6);

-- Engine
INSERT INTO Engine (modelName, horsePower, position, price, nameBrand) VALUES
('V8', 450, 'front', 15000.00, 'Ford'),
('Electric Powertrain', 1020, 'rear', 30000.00, 'Tesla'),
('Inline-6', 335, 'front', 12000.00, 'BMW'),
('Dual Motor', 450, 'rear', 25000.00, 'Tesla'),
('EcoBoost V6', 375, 'front', 22000.00, 'Ford'),
('Turbo Inline-4', 300, 'front', 18000.00, 'BMW');

-- Gas
INSERT INTO Gas (modelNameEngine, numberOfCylinders, engineDisplacement) VALUES
('V8', 8, 5.0),
('Inline-6', 6, 3.0);

-- Electric
INSERT INTO Electric (modelNameEngine, maxPower, batteryDistanceCapacity) VALUES
('Electric Powertrain', 1020, 400),
('Dual Motor', 1020, 500);

-- Specification_Engine
INSERT INTO Specification_Engine (idSpecification, modelNameEngine) VALUES
(1, 'Electric Powertrain'),
(4, 'Dual Motor'),
(2, 'EcoBoost V6'),
(5, 'EcoBoost V6'),
(3, 'Turbo Inline-4'),
(6, 'Turbo Inline-4');

-- Review
INSERT INTO Review (title, content, grade, date, idSpecification, emailUser) VALUES
('Amazing car', 'The Model S is fast and luxurious.', 5, '2023-01-10', 1, 'user1@example.com'),
('Great for work', 'The F-150 is perfect for my needs.', 4, '2023-06-15', 2, 'user2@example.com'),
('Comfort and power', 'The X5 combines luxury with performance.', 5, '2023-08-20', 3, 'user1@example.com'),
('Outstanding Performance', 'Model 3 exceeded my expectations.', 5, '2023-02-14', 4, 'user1@example.com'),
('Spacious and Reliable', 'Explorer is perfect for family trips.', 4, '2023-09-01', 5, 'user2@example.com'),
('Luxurious and Smooth', 'The 3 Series feels like a dream.', 5, '2023-11-22', 6, 'user1@example.com');

-- Category_Specification
INSERT INTO Category_Specification (nameCategory, idSpecification) VALUES
('Electric', 1),
('Performance', 4),
('SUV', 5),
('Luxury', 6),
('Family', 5);
