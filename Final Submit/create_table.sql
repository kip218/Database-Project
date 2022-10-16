CREATE TABLE Airline (
	name VARCHAR(50),
	PRIMARY KEY (name)
);

CREATE TABLE Airplane (
	airline_name VARCHAR(50),
	id VARCHAR(50),
	seats INT,
	manufacturer VARCHAR(50),
	age INT,
	PRIMARY KEY (airline_name, ID),
	FOREIGN KEY (airline_name) REFERENCES Airline(name)
);

CREATE TABLE Airport (
	id VARCHAR(50),
	name VARCHAR(50),
	city VARCHAR(50),
	country VARCHAR(50),
	type VARCHAR(50),
	PRIMARY KEY (id)
);

CREATE TABLE Flight (
	airline_name VARCHAR(50),
	flight_number VARCHAR(50),
	departure_date DATE,
	departure_time TIME,
	arrival_date DATE,
	arrival_time TIME,
	base_price NUMERIC(10,2),
	airplane_id VARCHAR(50),
	departure_airport VARCHAR(50),
	arrival_airport VARCHAR(50),
	status VARCHAR(50),
	PRIMARY KEY (airline_name, flight_number, departure_date, departure_time),
	FOREIGN KEY (airline_name, airplane_id) REFERENCES Airplane(airline_name, id),
	FOREIGN KEY (departure_airport) REFERENCES Airport(id),
	FOREIGN KeY (arrival_airport) REFERENCES Airport(id)
);

CREATE TABLE Customer (
	email VARCHAR(50),
	name VARCHAR(50),
	password CHAR(32), #length of md5 hash
	building_number VARCHAR(50),
	street VARCHAR(50),
	city VARCHAR(50),
	state VARCHAR(50),
	phone_number VARCHAR(50),
	passport_number VARCHAR(50),
	passport_expiration DATE,
	passport_country VARCHAR(50),
	date_of_birth DATE,
	PRIMARY KEY (email)
);

CREATE TABLE Ticket (
	id VARCHAR(50),
	travel_class VARCHAR(50),
	sold_price NUMERIC(10,2),
	card_type VARCHAR(50),
	card_number VARCHAR(50),
	name_on_card VARCHAR(50),
	card_exp_date DATE,
	purchase_date DATE,
	purchase_time TIME,
	airline_name VARCHAR(50),
	flight_number VARCHAR(50),
	departure_date DATE,
	departure_time TIME,
	customer_email VARCHAR(50),
	PRIMARY KEY (id),
	FOREIGN KEY (airline_name, flight_number, departure_date, departure_time) REFERENCES Flight(airline_name, flight_number, departure_date, departure_time),
	FOREIGN KEY (customer_email) REFERENCES Customer(email)
);

CREATE TABLE Review (
	customer_email VARCHAR(50),
	airline_name VARCHAR(50),
	flight_number VARCHAR(50),
	departure_date DATE,
	departure_time TIME,
	rating INT,
	comment VARCHAR(5000), #review length of 5000 characters
	PRIMARY KEY (customer_email, airline_name, flight_number, departure_date, departure_time),
	FOREIGN KEY (customer_email) REFERENCES Customer(email),
	FOREIGN KEY (airline_name, flight_number, departure_date, departure_time) REFERENCES Flight(airline_name, flight_number, departure_date, departure_time)
);

CREATE TABLE Staff (
	username VARCHAR(50),
	password CHAR(32), #length of md5 hash
	first_name VARCHAR(50),
	last_name VARCHAR(50),
	date_of_birth DATE,
	airline_name VARCHAR(50),
	PRIMARY KEY (username),
	FOREIGN KEY (airline_name) REFERENCES Airline(name)
);

CREATE TABLE Staff_Phone_Number (
	phone_number VARCHAR(50),
	staff_username VARCHAR(50),
	PRIMARY KEY (phone_number),
	FOREIGN KEY (staff_username) REFERENCES Staff(username)
);
