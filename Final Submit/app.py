from venv import create
from flask import Flask, render_template, request, session, url_for, redirect, flash
import pymysql.cursors # Used to interface the database
from datetime import datetime # May need this for your datetime columns/client
import hashlib # But can use this for md5
import re # If you want to use regex
import json # You'll need this library to parse json objects in python

# Verifies if an email is in a valid format via regex (regular expressions)
def validateEmail(email):
    # Regex is a way to examine a pattern in a string given a format pattern
	regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    # Checks if string input has the regex pattern
	return re.fullmatch(regex, email)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'MQZtHs3r6y>KdO/' # Needed for session and other stuff
app.config['APP_HOST'] = "localhost" # 127.0.0.1 is localhost IP for all computers

# Set this to your custom DB information
app.config['DB_USER'] = "root"
app.config['DB_PASSWORD'] = ""
app.config['APP_DB'] = "airline_ticket_management"
app.config['CHARSET'] = "utf8mb4"

# Connect to the DB
conn =  pymysql.connect(host=app.config['APP_HOST'],
                       user=app.config['DB_USER'],
                       password=app.config['DB_PASSWORD'],
                       db=app.config['APP_DB'],
                       charset=app.config['CHARSET'],
                       cursorclass=pymysql.cursors.DictCursor)

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    staffRegister = False
    error = None
    success = None
    checkUserStatement = "SELECT * FROM Customer WHERE email=%s"
    createUserStatement = "INSERT INTO Customer(email, password, name, building_number, street, city,\
                                                state, phone_number, passport_number, passport_expiration,\
                                                passport_country, date_of_birth)\
                                                VALUES (%s, md5(%s), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    if request.args.get('staff'):
        staffRegister = True
        checkUserStatement = "SELECT * FROM Staff WHERE username=%s"
        createUserStatement = "INSERT INTO Staff(username, password, first_name, last_name, date_of_birth, airline_name)\
                                                VALUES (%s, md5(%s), %s, %s, %s, %s)"

    if request.method == 'POST':
        if staffRegister:
            username = request.form['username']
            password = request.form['password']
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            date_of_birth = request.form['date_of_birth']
            airline_name = request.form['airline_name']
            args = (username, password, first_name, last_name, date_of_birth, airline_name)
        else:
            username = request.form['email']
            password = request.form['password']
            name = request.form['name']
            building_number = request.form['building_number']
            street = request.form['street']
            city = request.form['city']
            state = request.form['state']
            phone_number = request.form['phone_number']
            passport_number = request.form['passport_number']
            passport_expiration = request.form['passport_expiration']
            passport_country = request.form['passport_country']
            date_of_birth = request.form['date_of_birth']
            args = (email, password, name, building_number, street, city, state, phone_number,\
                    passport_number, passport_expiration, passport_country, date_of_birth)

        try:
            cursor = conn.cursor()
            # check if username is already registered
            cursor.execute(checkUserStatement, username)
            result = cursor.fetchall()
            if result:
                error = "Account with this email/username already exists!"
            else:
                # create new user
                cursor.execute(createUserStatement, args)
                conn.commit()
        except Exception as e:
            error = f"An error occurred: {e}"
        cursor.close()

        if not error:
            success = "Account created successfully!"

    if success:
        flash(success)
        return redirect(url_for('index'))
    else:
        return render_template("register.html", error=error, staffRegister=staffRegister)


@app.route('/login', methods=['GET', 'POST'])
def login():
    staffLogin = False
    error = None
    success = None
    getUserStatement = "SELECT email, name FROM Customer WHERE email=%s AND password=md5(%s)"
    if request.args.get('staff'):
        staffLogin = True
        getUserStatement = "SELECT username, first_name, last_name FROM Staff WHERE username=%s AND password=md5(%s)"

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:
            cursor = conn.cursor()
            cursor.execute(getUserStatement, (username, password))
            result = cursor.fetchone()
            if not result:
                error = "Wrong username or wrong password. For customers, please use your email as username."
            else:
                if staffLogin:
                    session['name'] = f"{result['first_name']} {result['last_name']}"
                else:
                    session['name'] = result['name']
                session['username'] = username
                session['isStaff'] = staffLogin
                session['logged_in'] = True

        except Exception as e:
            error = f"An error occurred: {e}"
        cursor.close()

        if not error:
            success = f"Logged in. Welcome {session['name']}"

    if success:
        flash(success)
        if staffLogin:
            return redirect(url_for('staff_dashboard'))
        else:
            return redirect(url_for('customer_dashboard'))
    else:
        return render_template("login.html", error=error)


@app.route('/view_public_info', methods=['GET', 'POST'])
def view_public_info():
    error = None
    success = None
    getFlightsStatement = "SELECT * FROM Flight WHERE departure_airport LIKE CONCAT('%%',%s) AND arrival_airport LIKE CONCAT('%%',%s)\
                                                    AND departure_date LIKE CONCAT('%%',%s) AND arrival_date LIKE CONCAT('%%',%s)"
    getFlightStatus = "SELECT * FROM Flight WHERE airline_name LIKE CONCAT('%%',%s) AND flight_number LIKE CONCAT('%%',%s)\
                                                    AND departure_date LIKE CONCAT('%%',%s) AND arrival_date LIKE CONCAT('%%',%s)"

    if request.method == 'POST':
        form_type = request.form['form']
        if form_type == 'search_flights':
            departure_airport = request.form['departure_airport']
            arrival_airport = request.form['arrival_airport']
            departure_date = request.form['departure_date']
            arrival_date = request.form['arrival_date']
            if request.form.get('only_show_future_flights'):
                getFlightsStatement = getFlightsStatement + " AND departure_date > NOW()"

            try:
                cursor = conn.cursor()
                cursor.execute(getFlightsStatement, (departure_airport, arrival_airport, departure_date, arrival_date))
                result = cursor.fetchall()
                if not result:
                    error = "No flights found satisfying search criteria!"
            except Exception as e:
                error = f"An error occurred: {e}"
            cursor.close()

            if not error:
                success = "Showing flights satisfying search criteria..."
        elif form_type == 'check_flight_status':
            airline_name = request.form['airline_name']
            flight_number = request.form['flight_number']
            departure_date = request.form['departure_date']
            arrival_date = request.form['arrival_date']
            if request.form.get('only_show_future_flights'):
                getFlightStatus = getFlightStatus + " AND departure_date > NOW()"

            try:
                cursor = conn.cursor()
                cursor.execute(getFlightStatus, (airline_name, flight_number, departure_date, arrival_date))
                result = cursor.fetchall()
                if not result:
                    error = "No flights found satisfying search criteria!"
            except Exception as e:
                error = f"An error occurred: {e}"
            cursor.close()

            if not error:
                success = "Showing flight status for flights satisfying search criteria..."

    if success:
        flash(success)
        return render_template("public_search_results.html", form_type=form_type, result=result)
    else:
        return render_template("view_public_info.html", error=error)


@app.route('/customer_dashboard', methods=['GET', 'POST'])
def customer_dashboard():
    error = None
    success = None
    if not session.get('logged_in'):
        error = "You must be logged in to view the dashboard!"
        flash(error)
        return redirect(url_for('index'))

    name = session['name']
    return render_template("customer_dashboard.html", success=success, name=name)


@app.route('/customer_view_flights', methods=['GET', 'POST'])
def customer_view_flights():
    error = None
    success = None
    getTicketsStatement = "SELECT * FROM Ticket LEFT OUTER JOIN Flight ON\
                            Ticket.airline_name=Flight.airline_name AND Ticket.flight_number=Flight.flight_number AND\
                            Ticket.departure_date=Flight.departure_date AND Ticket.departure_time=Flight.departure_time\
                            WHERE customer_email=%s"

    if not session.get('logged_in'):
        error = "You must be logged in to view the dashboard!"
        flash(error)
        return redirect(url_for('index'))

    if request.args.get('only_show_future_flights'):
        getTicketsStatement = getTicketsStatement + " AND Ticket.departure_date > NOW()"

    if request.method == 'GET':
        try:
            email = session['username']
            cursor = conn.cursor()
            cursor.execute(getTicketsStatement, email)
            result = cursor.fetchall()
        except Exception as e:
            error = f"An error occurred: {e}"
        cursor.close()

    if not error:
        success = "Showing your flights..."

    if success:
        flash(success)
        return render_template("customer_view_flights.html", success=success, result=result)
    else:
        flash(error)
        return redirect(url_for('customer_dashboard'))


@app.route('/customer_search_flights', methods=['GET', 'POST'])
def customer_search_flights():
    error = None
    success = None
    getFlightsStatement = "SELECT * FROM Flight WHERE departure_airport LIKE CONCAT('%%',%s) AND arrival_airport LIKE CONCAT('%%',%s)\
                                                    AND departure_date LIKE CONCAT('%%',%s) AND arrival_date LIKE CONCAT('%%',%s)\
                                                    AND departure_date > NOW()"

    if not session.get('logged_in'):
        error = "You must be logged in to view the dashboard!"
        flash(error)
        return redirect(url_for('index'))

    if request.method == 'POST':
        form_type = request.form['form']
        if form_type == 'search_flights':
            departure_airport = request.form['departure_airport']
            arrival_airport = request.form['arrival_airport']
            departure_date = request.form['departure_date']
            arrival_date = request.form['arrival_date']

            try:
                cursor = conn.cursor()
                cursor.execute(getFlightsStatement, (departure_airport, arrival_airport, departure_date, arrival_date))
                result = cursor.fetchall()
                if not result:
                    error = "No flights found satisfying search criteria!"
            except Exception as e:
                error = f"An error occurred: {e}"
            cursor.close()

            if not error:
                success = "Showing flights satisfying search criteria..."

    if success:
        flash(success)
        return render_template("customer_search_results.html", result=result)
    else:
        return render_template("customer_search_flights.html", error=error)


@app.route('/customer_purchase', methods=['GET', 'POST'])
def customer_purchase():
    error = None
    success = None
    getID = 'SELECT MAX(id) as maxID FROM Ticket'
    purchaseTicket = 'INSERT INTO Ticket(id, travel_class, sold_price, purchase_date, purchase_time,\
                                airline_name, flight_number, departure_date, departure_time, customer_email)\
                                VALUES(%s, %s, %s, DATE(NOW()), TIME(NOW()), %s, %s, %s, %s, %s)'
    getFlightInfo = 'SELECT * FROM Flight WHERE airline_name=%s AND flight_number=%s AND departure_date=%s AND departure_time=%s'

    airline_name = request.args.get('airline_name')
    flight_number = request.args.get('flight_number')
    departure_date = request.args.get('departure_date')
    departure_time = request.args.get('departure_time')

    try:
        email = session['username']
        cursor = conn.cursor()
        cursor.execute(getID)
        maxID = cursor.fetchone()['maxID']
        newID = str(int(maxID)+1).zfill(8)
        cursor.execute(getFlightInfo, (airline_name, flight_number, departure_date, departure_time))
        price = cursor.fetchone()['base_price']
        cursor.execute(purchaseTicket, (newID, 'economy class', price, airline_name, flight_number, departure_date, departure_time, email))
        conn.commit()
    except Exception as e:
        error = f"An error occurred: {e}"
    cursor.close()

    if not error:
        success = f"Succesfully purchased flight {flight_number}"

    if success:
        flash(success)
        return redirect(url_for('customer_dashboard'))
    else:
        flash(error)
        return redirect(url_for('customer_dashboard'))


@app.route('/customer_cancel', methods=['GET', 'POST'])
def customer_cancel():
    error = None
    success = None
    getID = 'SELECT id FROM Ticket WHERE airline_name=%s AND flight_number=%s AND departure_date=%s AND departure_time=%s AND customer_email=%s'
    deleteTicket = 'DELETE FROM Ticket WHERE id=%s'

    airline_name = request.args.get('airline_name')
    flight_number = request.args.get('flight_number')
    departure_date = request.args.get('departure_date')
    departure_time = request.args.get('departure_time')

    try:
        email = session['username']
        cursor = conn.cursor()
        cursor.execute(getID, (airline_name, flight_number, departure_date, departure_time, email))
        ticketID = cursor.fetchone()['id']
        cursor.execute(deleteTicket, ticketID)
        conn.commit()
    except Exception as e:
        error = f"An error occurred: {e}"
    cursor.close()

    if not error:
        success = f"Succesfully canceled flight {flight_number}"

    if success:
        flash(success)
        return redirect(url_for('customer_dashboard'))
    else:
        flash(error)
        return redirect(url_for('customer_dashboard'))


@app.route('/customer_review', methods=['GET', 'POST'])
def customer_review():
    error = None
    success = None
    createReview = 'INSERT INTO Review(customer_email, airline_name, flight_number, departure_date, departure_time, rating, comment)\
                                VALUES(%s, %s, %s, %s, %s, %s, %s)'

    airline_name = request.args.get('airline_name')
    flight_number = request.args.get('flight_number')
    departure_date = request.args.get('departure_date')
    departure_time = request.args.get('departure_time')
    rating = request.form['rating']
    comment = request.form['comment']

    try:
        email = session['username']
        cursor = conn.cursor()
        cursor.execute(createReview, (email, airline_name, flight_number, departure_date, departure_time, rating, comment))
        conn.commit()
    except Exception as e:
        error = f"An error occurred: {e}"
    cursor.close()

    if not error:
        success = f"Succesfully left review for {flight_number}"

    if success:
        flash(success)
        return redirect(url_for('customer_dashboard'))
    else:
        flash(error)
        return redirect(url_for('customer_dashboard'))


@app.route('/customer_past_flights', methods=['GET', 'POST'])
def customer_past_flights():
    error = None
    success = None
    getFlightsStatement = "SELECT * FROM Ticket LEFT OUTER JOIN Flight ON\
                            Ticket.airline_name=Flight.airline_name AND Ticket.flight_number=Flight.flight_number AND\
                            Ticket.departure_date=Flight.departure_date AND Ticket.departure_time=Flight.departure_time\
                            WHERE customer_email=%s AND Ticket.departure_date < NOW()"

    if not session.get('logged_in'):
        error = "You must be logged in to view the dashboard!"
        flash(error)
        return redirect(url_for('index'))

    if request.method == 'GET':
        try:
            email = session['username']
            cursor = conn.cursor()
            cursor.execute(getFlightsStatement, email)
            result = cursor.fetchall()
        except Exception as e:
            error = f"An error occurred: {e}"
        cursor.close()

    if not error:
        success = "Showing your past flights..."

    if success:
        flash(success)
        return render_template("customer_search_results.html", success=success, result=result)
    else:
        flash(error)
        return redirect(url_for('customer_dashboard'))


@app.route('/track_spending', methods=['GET', 'POST'])
def track_spending():
    error = None
    success = None
    yearlySpendingStatement = "SELECT SUM(sold_price) as past_year_total FROM Ticket WHERE customer_email=%s\
                                AND DATEDIFF(NOW(), purchase_date) < 366"
    monthlySpendingStatement = "SELECT customer_email, purchase_date,\
                                YEAR(purchase_date) as year, MONTH(purchase_date) as month, SUM(sold_price) as monthly_spending\
                                FROM Ticket GROUP BY MONTH(purchase_date), YEAR(purchase_date), customer_email\
                                HAVING customer_email=%s AND TIMESTAMPDIFF(MONTH, purchase_date, NOW()) < 5\
                                ORDER BY purchase_date"

    if not session.get('logged_in'):
        error = "You must be logged in to view the dashboard!"
        flash(error)
        return redirect(url_for('index'))

    if request.method == 'GET':
        try:
            email = session['username']
            cursor = conn.cursor()
            cursor.execute(yearlySpendingStatement, email)
            past_year_total = cursor.fetchone()['past_year_total']
            cursor.execute(monthlySpendingStatement, email)
            monthly_spendings = cursor.fetchall()
            print(monthly_spendings)
        except Exception as e:
            error = f"An error occurred: {e}"
        cursor.close()

    if not error:
        success = "Showing your spending history..."

    if success:
        flash(success)
        return render_template("customer_track_spending.html", success=success, monthly_spendings=monthly_spendings, past_year_total=past_year_total)
    else:
        flash(error)
        return redirect(url_for('customer_dashboard'))


@app.route('/log_out', methods=['GET'])
def log_out():
    session.clear()
    flash("Logged Out!")
    return redirect(url_for('index'))


@app.route('/staff_dashboard', methods=['GET', 'POST'])
def staff_dashboard():
    error = None
    success = None
    if not session.get('logged_in'):
        error = "You must be logged in to view the dashboard!"
        flash(error)
        return redirect(url_for('index'))

    if not session.get('isStaff'):
        error = "You must be a staff to view the staff dashboard!"
        flash(error)
        return redirect(url_for('customer_dashboard'))

    name = session['name']
    return render_template("staff_dashboard.html", success=success, name=name)


@app.route('/staff_view_flights', methods=['GET', 'POST'])
def staff_view_flights():
    error = None
    success = None
    getFlightsStatement = "SELECT * FROM Flight LEFT OUTER JOIN Staff ON\
                            Flight.airline_name=Staff.airline_name\
                            WHERE username=%s AND DATEDIFF(departure_date, NOW()) < 31 AND DATEDIFF(departure_date, NOW()) > -1"

    if not session.get('logged_in'):
        error = "You must be logged in to view the dashboard!"
        flash(error)
        return redirect(url_for('index'))

    if not session.get('isStaff'):
        error = "You must be a staff to view the staff dashboard!"
        flash(error)
        return redirect(url_for('customer_dashboard'))

    if request.method == 'GET':
        try:
            username = session['username']
            cursor = conn.cursor()
            cursor.execute(getFlightsStatement, username)
            result = cursor.fetchall()
        except Exception as e:
            error = f"An error occurred: {e}"
        cursor.close()

    if not error:
        success = "Showing your airline flights..."

    if success:
        flash(success)
        return render_template("staff_view_flights.html", success=success, result=result)
    else:
        flash(error)
        return redirect(url_for('staff_dashboard'))


@app.route('/staff_create_flights', methods=['GET', 'POST'])
def staff_create_flights():
    error = None
    success = None
    getFlightsStatement = "SELECT * FROM Flight LEFT OUTER JOIN Staff ON\
                            Flight.airline_name=Staff.airline_name\
                            WHERE username=%s AND DATEDIFF(departure_date, NOW()) < 31 AND DATEDIFF(departure_date, NOW()) > -1"
    createFlightStatement = "INSERT INTO Flight(airline_name, flight_number, departure_date, departure_time,\
                                                arrival_date, arrival_time, base_price,\
                                                airplane_id, departure_airport, arrival_airport, status)\
                                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    getStaffInfo = "SELECT DISTINCT airline_name FROM Staff WHERE username=%s"

    if not session.get('logged_in'):
        error = "You must be logged in to view the dashboard!"
        flash(error)
        return redirect(url_for('index'))

    if not session.get('isStaff'):
        error = "You must be a staff to view the staff dashboard!"
        flash(error)
        return redirect(url_for('customer_dashboard'))

    if request.method == 'POST':
        try:
            username = session['username']
            cursor = conn.cursor()

            cursor.execute(getStaffInfo, username)
            airline_name = cursor.fetchone()['airline_name']
            flight_number = request.form['flight_number']
            departure_date = request.form['departure_date']
            departure_time = request.form['departure_time']
            arrival_date = request.form['arrival_date']
            arrival_time = request.form['arrival_time']
            base_price = request.form['base_price']
            airplane_id = request.form['airplane_id']
            departure_airport = request.form['departure_airport']
            arrival_airport = request.form['arrival_airport']
            status = 'on time'
            cursor.execute(createFlightStatement, (airline_name, flight_number, departure_date, departure_time,\
                                                    arrival_date, arrival_time, base_price, airplane_id,\
                                                    departure_airport, arrival_airport, status))
            conn.commit()
            cursor.execute(getFlightsStatement, username)
            result = cursor.fetchall()
        except Exception as e:
            error = f"An error occurred: {e}"
        cursor.close()
        if not error:
            success = f"New Flight {flight_number} Created!"
    elif request.method == 'GET':
        try:
            username = session['username']
            cursor = conn.cursor()
            cursor.execute(getFlightsStatement, username)
            result = cursor.fetchall()
        except Exception as e:
            error = f"An error occurred: {e}"
        cursor.close()
        if not error:
            success = "Showing your airline flights..."

    if success:
        flash(success)
        return render_template("staff_create_flights.html", result=result)
    else:
        flash(error)
        return redirect(url_for('staff_dashboard'))


@app.route('/staff_see_reviews', methods=['GET', 'POST'])
def staff_see_reviews():
    error = None
    success = None
    getReviews = "SELECT * FROM Review WHERE airline_name=%s"
    getStaffInfo = "SELECT DISTINCT airline_name FROM Staff WHERE username=%s"

    if not session.get('logged_in'):
        error = "You must be logged in to view the dashboard!"
        flash(error)
        return redirect(url_for('index'))

    if not session.get('isStaff'):
        error = "You must be a staff to view the staff dashboard!"
        flash(error)
        return redirect(url_for('customer_dashboard'))

    if request.method == 'GET':
        try:
            username = session['username']
            cursor = conn.cursor()
            cursor.execute(getStaffInfo, username)
            airline_name = cursor.fetchone()['airline_name']
            cursor.execute(getReviews, airline_name)
            result = cursor.fetchall()
        except Exception as e:
            error = f"An error occurred: {e}"
        cursor.close()

    if not error:
        success = "Showing your airline reviews..."

    if success:
        flash(success)
        return render_template("staff_see_reviews.html", success=success, result=result)
    else:
        flash(error)
        return redirect(url_for('staff_dashboard'))


@app.route('/staff_see_frequent_customers', methods=['GET', 'POST'])
def staff_see_frequent_customers():
    error = None
    success = None
    getFrequent = "SELECT *, COUNT(*) as count FROM Ticket LEFT OUTER JOIN Flight ON\
                        Ticket.airline_name=Flight.airline_name AND Ticket.flight_number=Flight.flight_number AND\
                        Ticket.departure_date=Flight.departure_date AND Ticket.departure_time=Flight.departure_time\
                        WHERE Ticket.airline_name=%s AND TIMESTAMPDIFF(MONTH, NOW(), Ticket.departure_date) < 11\
                        GROUP BY Ticket.customer_email \
                        ORDER BY count DESC"
    getStaffInfo = "SELECT DISTINCT airline_name FROM Staff WHERE username=%s"

    if not session.get('logged_in'):
        error = "You must be logged in to view the dashboard!"
        flash(error)
        return redirect(url_for('index'))

    if not session.get('isStaff'):
        error = "You must be a staff to view the staff dashboard!"
        flash(error)
        return redirect(url_for('customer_dashboard'))

    if request.method == 'GET':
        try:
            username = session['username']
            cursor = conn.cursor()
            cursor.execute(getStaffInfo, username)
            airline_name = cursor.fetchone()['airline_name']
            cursor.execute(getFrequent, airline_name)
            result = cursor.fetchall()
            print(result)
        except Exception as e:
            error = f"An error occurred: {e}"
        cursor.close()

    if not error:
        success = "Showing your airline reviews..."

    if success:
        flash(success)
        return render_template("staff_see_frequent_customers.html", success=success, result=result)
    else:
        flash(error)
        return redirect(url_for('staff_dashboard'))

@app.route('/staff_change_status', methods=['GET', 'POST'])
def staff_change_status():
    error = None
    success = None
    getStaffInfo = "SELECT DISTINCT airline_name FROM Staff WHERE username=%s"
    changeStatus = "UPDATE Flight SET status=%s WHERE airline_name=%s AND flight_number=%s AND departure_date=%s AND departure_time=%s"
    checkFlight = "SELECT * FROM Flight WHERE airline_name=%s AND flight_number=%s AND departure_date=%s AND departure_time=%s"

    if not session.get('logged_in'):
        error = "You must be logged in to view the dashboard!"
        flash(error)
        return redirect(url_for('index'))

    if not session.get('isStaff'):
        error = "You must be a staff to view the staff dashboard!"
        flash(error)
        return redirect(url_for('customer_dashboard'))

    if request.method == 'POST':
        try:
            username = session['username']
            cursor = conn.cursor()
            cursor.execute(getStaffInfo, username)
            airline_name = cursor.fetchone()['airline_name']
            flight_number = request.form['flight_number']
            departure_date = request.form['departure_date']
            departure_time = request.form['departure_time']
            status = request.form['status']
            cursor.execute(checkFlight, (airline_name, flight_number, departure_date, departure_time))
            result = cursor.fetchone()
            if result:
                cursor.execute(changeStatus, (status, airline_name, flight_number, departure_date, departure_time))
                conn.commit()
            else:
                error = "Specified flight doesn't exist!"
        except Exception as e:
            error = f"An error occurred: {e}"
        cursor.close()

        if not error:
            success = f"Changed flight status of {flight_number} to {status}"
    elif request.method == 'GET':
        return render_template("staff_change_status.html")

    if success:
        flash(success)
        return render_template("staff_change_status.html")
    else:
        flash(error)
        return redirect(url_for('staff_change_status'))


@app.route('/staff_create_airplane', methods=['GET', 'POST'])
def staff_create_airplane():
    error = None
    success = None
    getStaffInfo = "SELECT DISTINCT airline_name FROM Staff WHERE username=%s"
    createAirplane = "INSERT INTO Airplane(airline_name, id, seats, manufacturer, age)\
                                        VALUES (%s, %s, %s, %s, %s)"
    getAirplanes = "SELECT * FROM Airplane WHERE airline_name=%s"

    if not session.get('logged_in'):
        error = "You must be logged in to view the dashboard!"
        flash(error)
        return redirect(url_for('index'))

    if not session.get('isStaff'):
        error = "You must be a staff to view the staff dashboard!"
        flash(error)
        return redirect(url_for('customer_dashboard'))

    if request.method == 'POST':
        try:
            username = session['username']
            cursor = conn.cursor()
            cursor.execute(getStaffInfo, username)
            airline_name = cursor.fetchone()['airline_name']
            airplane_id = request.form['airplane_id']
            seats = request.form['seats']
            manufacturer = request.form['manufacturer']
            age = request.form['age']
            cursor.execute(createAirplane, (airline_name, airplane_id, seats, manufacturer, age))
            conn.commit()
            cursor.execute(getAirplanes, airline_name)
            result = cursor.fetchall()
        except Exception as e:
            error = f"An error occurred: {e}"
        cursor.close()

        if not error:
            success = f"Added new airplane id:{airplane_id} to {airline_name}"
    elif request.method == 'GET':
        try:
            username = session['username']
            cursor = conn.cursor()
            cursor.execute(getStaffInfo, username)
            airline_name = cursor.fetchone()['airline_name']
            cursor.execute(getAirplanes, airline_name)
            result = cursor.fetchall()
        except Exception as e:
            error = f"An error occurred: {e}"
        cursor.close()
        return render_template("staff_create_airplane.html", result=result, airline_name=airline_name)

    if success:
        flash(success)
        return render_template("staff_create_airplane.html", result=result, airline_name=airline_name)
    else:
        flash(error)
        return redirect(url_for('staff_create_airplane'))


@app.route('/staff_create_airport', methods=['GET', 'POST'])
def staff_create_airport():
    error = None
    success = None
    createAirport = "INSERT INTO Airport(id, name, city, country, type)\
                                        VALUES (%s, %s, %s, %s, %s)"
    getAirports = "SELECT * FROM Airport"

    if not session.get('logged_in'):
        error = "You must be logged in to view the dashboard!"
        flash(error)
        return redirect(url_for('index'))

    if not session.get('isStaff'):
        error = "You must be a staff to view the staff dashboard!"
        flash(error)
        return redirect(url_for('customer_dashboard'))

    if request.method == 'POST':
        try:
            cursor = conn.cursor()
            airport_id = request.form['airport_id']
            name = request.form['name']
            city = request.form['city']
            country = request.form['country']
            airport_type = request.form['type']
            cursor.execute(createAirport, (airport_id, name, city, country, airport_type))
            conn.commit()
            cursor.execute(getAirports)
            result = cursor.fetchall()
        except Exception as e:
            error = f"An error occurred: {e}"
        cursor.close()

        if not error:
            success = f"Added new airport id:{airport_id}"
    elif request.method == 'GET':
        try:
            cursor = conn.cursor()
            cursor.execute(getAirports)
            result = cursor.fetchall()
        except Exception as e:
            error = f"An error occurred: {e}"
        cursor.close()
        return render_template("staff_create_airport.html", result=result)

    if success:
        flash(success)
        return render_template("staff_create_airport.html", result=result)
    else:
        flash(error)
        return redirect(url_for('staff_create_airport'))


@app.route('/staff_see_revenue', methods=['GET'])
def staff_see_revenue():
    error = None
    success = None
    getPastMonthRevenue = "SELECT SUM(sold_price) as past_month_total FROM Ticket WHERE DATEDIFF(NOW(), purchase_date) < 31"
    getPastYearRevenue = "SELECT SUM(sold_price) as past_year_total FROM Ticket WHERE DATEDIFF(NOW(), purchase_date) < 366"
    getTotalByClass = "SELECT SUM(sold_price) as total FROM Ticket WHERE travel_class=%s"

    if not session.get('logged_in'):
        error = "You must be logged in to view the dashboard!"
        flash(error)
        return redirect(url_for('index'))

    if not session.get('isStaff'):
        error = "You must be a staff to view the staff dashboard!"
        flash(error)
        return redirect(url_for('customer_dashboard'))

    if request.method == 'GET':
        try:
            cursor = conn.cursor()
            cursor.execute(getPastMonthRevenue)
            past_month_revenue = cursor.fetchone()['past_month_total']
            cursor.execute(getPastYearRevenue)
            past_year_revenue = cursor.fetchone()['past_year_total']
            cursor.execute(getTotalByClass, "economy class")
            total_econ = cursor.fetchone()['total']
            cursor.execute(getTotalByClass, "business class")
            total_busi = cursor.fetchone()['total']
            cursor.execute(getTotalByClass, "first class")
            total_first = cursor.fetchone()['total']
        except Exception as e:
            error = f"An error occurred: {e}"
        cursor.close()
        if not error:
            success = "Showing Revenue..."

    if success:
        flash(success)
        return render_template("staff_see_revenue.html", past_month_revenue=past_month_revenue, past_year_revenue=past_year_revenue,\
                                total_econ=total_econ, total_busi=total_busi, total_first=total_first)
    else:
        flash(error)
        return redirect(url_for('staff_dashboard'))


@app.route('/staff_see_top_dest', methods=['GET'])
def staff_see_top_dest():
    error = None
    success = None
    getDestMonths = "SELECT *, COUNT(*) as count FROM Ticket LEFT OUTER JOIN Flight ON\
                        Ticket.airline_name=Flight.airline_name AND Ticket.flight_number=Flight.flight_number AND\
                        Ticket.departure_date=Flight.departure_date AND Ticket.departure_time=Flight.departure_time\
                        LEFT OUTER JOIN Airport ON Flight.arrival_airport=Airport.id\
                        WHERE TIMESTAMPDIFF(MONTH, NOW(), Ticket.departure_date) < 2\
                        GROUP BY Flight.arrival_airport \
                        ORDER BY count DESC"
    getDestYear = "SELECT *, COUNT(*) as count FROM Ticket LEFT OUTER JOIN Flight ON\
                        Ticket.airline_name=Flight.airline_name AND Ticket.flight_number=Flight.flight_number AND\
                        Ticket.departure_date=Flight.departure_date AND Ticket.departure_time=Flight.departure_time\
                        LEFT OUTER JOIN Airport ON Flight.arrival_airport=Airport.id\
                        WHERE TIMESTAMPDIFF(MONTH, NOW(), Ticket.departure_date) < 11\
                        GROUP BY Flight.arrival_airport \
                        ORDER BY count DESC"

    if not session.get('logged_in'):
        error = "You must be logged in to view the dashboard!"
        flash(error)
        return redirect(url_for('index'))

    if not session.get('isStaff'):
        error = "You must be a staff to view the staff dashboard!"
        flash(error)
        return redirect(url_for('customer_dashboard'))

    if request.method == 'GET':
        try:
            cursor = conn.cursor()
            cursor.execute(getDestMonths)
            top_dest_months = cursor.fetchall()
            if len(top_dest_months) > 3:
                top_dest_months = top_dest_months[:3]
            cursor.execute(getDestYear)
            top_dest_year = cursor.fetchall()
            if len(top_dest_year) > 3:
                top_dest_year = top_dest_year[:3]
        except Exception as e:
            error = f"An error occurred: {e}"
        cursor.close()
        if not error:
            success = "Showing Top Destinations..."

    if success:
        flash(success)
        return render_template("staff_see_top_dest.html", top_dest_months=top_dest_months, top_dest_year=top_dest_year)
    else:
        flash(error)
        return redirect(url_for('staff_dashboard'))

if __name__ == "__main__":
    app.run("127.0.0.1", 3000, debug = True)
