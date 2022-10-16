INSERT INTO Airline
	(name)
VALUES
	('China Eastern'),
	('Korean Air'),
	('American Airlines');


INSERT INTO Airport
	(
		id,
		name,
		city,
		country,
		type
	)
VALUES
	(
		'JFK',
		'John F. Kennedy International Airport',
		'New York City',
		'United States',
		'International'
	),
	(
		'PVG',
		'Shanghai Pudong International Airport',
		'Shanghai',
		'China',
		'International'
	),
	(
		'ICN',
		'Incheon International Airport',
		'Incheon',
		'Korea',
		'International'
	);


INSERT INTO Customer
	(
		email,
		name,
		password,
		building_number,
		street,
		city,
		state,
		phone_number,
		passport_number, 
		passport_expiration,
		passport_country,
		date_of_birth
	)
VALUES
	(
		'kip218@nyu.edu',
		'Kang In Park',
		'5f4dcc3b5aa765d61d8327deb882cf99',
		'310',
		'3rd Ave',
		'New York City',
		'New York',
		'3322015579',
		'123456789',
		'2025-07-07',
		'Korea',
		'1999-04-07'
	),
	(
		'john@gmail.com',
		'John Doe',
		'5f4dcc3b5aa765d61d8327deb882cf99',
		'750',
		'Broadway',
		'New York City',
		'New York',
		'1357924680',
		'987654321',
		'2024-06-06',
		'United States',
		'1997-09-15'
	),
	(
		'kevin@gmail.com',
		'Kevin Li',
		'5f4dcc3b5aa765d61d8327deb882cf99',
		'460',
		'23rd Street',
		'New York City',
		'New York',
		'1029384756',
		'192837465',
		'2023-08-08',
		'China',
		'1998-02-24'
	),
	(
		'ms123@gmail.com',
		'Mary Smith',
		'5f4dcc3b5aa765d61d8327deb882cf99',
		'310',
		'3rd Ave',
		'New York City',
		'New York',
		'3322011234',
		'123451234',
		'2025-07-07',
		'Korea',
		'1999-04-07'
	);


INSERT INTO Airplane
	(
		airline_name,
		id,
		seats,
		manufacturer,
		age
	)
VALUES
	(
		'Korean Air',
		'123456',
		800,
		'Korea Aerospace Industries',
		5
	),
	(
		'Korean Air',
		'293949',
		400,
		'Korea Aerospace Industries',
		3
	),
	(
		'China Eastern',
		'135246',
		900,
		'Commercial Aircraft Corporation of China',
		6
	),
	(
		'China Eastern',
		'574737',
		500,
		'Commercial Aircraft Corporation of China',
		4
	),
	(
		'American Airlines',
		'183828',
		600,
		'Boeing',
		8
	);


INSERT INTO Staff
	(
		username,
		password,
		first_name,
		last_name,
		date_of_birth,
		airline_name
	)
VALUES
	(
		'sam123',
		'5f4dcc3b5aa765d61d8327deb882cf99',
		'Sam',
		'Zhou',
		'1996-12-21',
		'China Eastern'
	),
	(
		'david123',
		'5f4dcc3b5aa765d61d8327deb882cf99',
		'David',
		'Kim',
		'1995-11-14',
		'Korean Air'
	),
	(
		'martha123',
		'5f4dcc3b5aa765d61d8327deb882cf99',
		'Martha',
		'Anderson',
		'1994-10-12',
		'American Airlines'
	);


INSERT INTO Flight
	(
		airline_name,
		flight_number,
		departure_date,
		departure_time,
		arrival_date,
		arrival_time,
		base_price,
		airplane_id,
		departure_airport,
		arrival_airport,
		status
	)
VALUES
	(
		'Korean Air',
		'KA1234',
		'2022-04-20',
		'08:00:00',
		'2022-04-21',
		'06:00:00',
		700,
		'123456',
		'ICN',
		'JFK',
		'on time'
	),
	(
		'China Eastern',
		'CE4321',
		'2022-04-07',
		'16:00:00',
		'2022-04-07',
		'20:00:00',
		400,
		'135246',
		'PVG',
		'ICN',
		'delayed'
	),
	(
		'American Airlines',
		'AA1423',
		'2022-04-06',
		'15:00:00',
		'2022-04-07',
		'12:00:00',
		800,
		'183828',
		'JFK',
		'ICN',
		'delayed'
	),
	(
		'Korean Air',
		'KA1234',
		'2023-04-20',
		'08:00:00',
		'2023-04-21',
		'06:00:00',
		400,
		'123456',
		'ICN',
		'JFK',
		'on time'
	);


INSERT INTO Ticket
	(
		id,
		travel_class,
		sold_price,
		card_type,
		card_number,
		name_on_card,
		card_exp_date,
		purchase_date,
		purchase_time,
		airline_name,
		flight_number,
		departure_date,
		departure_time,
		customer_email
	)
VALUES
	(
		'00000001',
		'economy class',
		500,
		'Visa',
		'1928574892837462',
		'Kang In Park',
		'2024-09-04',
		'2022-03-29',
		'21:00:00',
		'China Eastern',
		'CE4321',
		'2022-04-07',
		'16:00:00',
		'kip218@nyu.edu'
	),
	(
		'00000002',
		'business class',
		800,
		'Mastercard',
		'4839029317829382',
		'John Doe',
		'2025-03-12',
		'2022-04-04',
		'22:00:00',
		'Korean Air',
		'KA1234',
		'2022-04-20',
		'08:00:00',
		'john@gmail.com'
	),
	(
		'00000003',
		'first class',
		1200,
		'Visa',
		'5748938420918293',
		'Kevin Li',
		'2024-05-02',
		'2022-04-03',
		'20:00:00',
		'American Airlines',
		'AA1423',
		'2022-04-06',
		'15:00:00',
		'kevin@gmail.com'
	);

