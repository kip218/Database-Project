# a. Show all the future flights in the system. 
SELECT * FROM Flight WHERE TIMESTAMP(departure_date, departure_time) > CURRENT_TIMESTAMP();

#QUERY RESULTS
#airline_name	flight_number	departure_date	departure_time	arrival_date	arrival_time	base_price	airplane_id	departure_airport	arrival_airport	status	
#China Eastern	CE4321			2022-04-07		16:00:00		2022-04-07		20:00:00		400.00		135246		PVG					ICN				delayed	
#Korean Air		KA1234			2022-04-20		08:00:00		2022-04-21		06:00:00		700.00		123456		ICN					JFK				on time	



# b. Show all of the delayed flights in the system.
SELECT * FROM FLIGHT WHERE status = 'delayed';

#QUERY RESULTS
#airline_name		flight_number	departure_date	departure_time	arrival_date	arrival_time	base_price	airplane_id	departure_airport	arrival_airport	status	
#American Airlines	AA1423			2022-04-06		15:00:00		2022-04-07		12:00:00		800.00		183828		JFK					ICN				delayed	
#China Eastern		CE4321			2022-04-07		16:00:00		2022-04-07		20:00:00		400.00		135246		PVG					ICN				delayed	



# c. Show the customer names who bought the tickets.
SELECT DISTINCT name FROM Ticket LEFT OUTER JOIN Customer ON Ticket.customer_email=Customer.email;

#QUERY RESULTS
#name	
#John Doe	
#Kevin Li	
#Kang In Park	



# d. Show all the airplanes owned by the airline (such as "China Eastern")
SELECT * FROM Airplane WHERE airline_name='China Eastern';

#QUERY RESULTS
#airline_name	id		seats	manufacturer								age	
#China Eastern	135246	900		Commercial Aircraft Corporation of China	6	
#China Eastern	574737	500		Commercial Aircraft Corporation of China	4	
