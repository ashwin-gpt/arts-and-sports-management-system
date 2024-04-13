from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import mysql.connector

app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = 'your_secret_key_here'

def connect_to_database():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="ashwin",
            password="ashwin9*",
            database="mini_proj"
        )
    except mysql.connector.Error as e:
        print("An error occurred while connecting to the database:", e)

@app.route('/')
def home():
    return render_template('homepage.html')

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db_connection = connect_to_database()
        cursor = db_connection.cursor()

        try:
            query = "SELECT * FROM admin WHERE username = %s AND password = %s"
            cursor.execute(query, (username, password))
            admin = cursor.fetchone()

            cursor.fetchall()

            if admin:
                session['admin_logged_in'] = True
                return redirect(url_for('admin_dashboard'))
            else:
                return render_template('admin_login.html', error='Invalid username or password')

        except mysql.connector.Error as e:
            return render_template('admin_login.html', error='An error occurred while processing your request.')

        finally:
            cursor.close()
            db_connection.close()
    else:
        return render_template('admin_login.html')

@app.route('/admin_dashboard')
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    return render_template('admin_dashboard.html')



#ADMIN-SPORTSDAY
@app.route('/sportsevent_creation', methods=['GET', 'POST'])
def sportsevent_creation():
    if request.method == 'POST':
        # Retrieve values from the form
        event_type = request.form['event_type']
        event_name = request.form['event_name']
        venue = request.form['venue']
        event_date = request.form['event_date']
        event_time = request.form['event_time']
        ampm = request.form['ampm']

        try:
            # Connect to the database
            db_connection = connect_to_database()
            cursor = db_connection.cursor()

            # Insert data into the sportsevent table
            insert_query = "INSERT INTO sportsevent (event_name, venue, event_date, event_time, ampm, event_type) VALUES (%s, %s, %s, %s, %s, %s)"
            data = (event_name, venue, event_date, event_time, ampm, event_type)
            cursor.execute(insert_query, data)
            db_connection.commit()

            # Close database connection
            cursor.close()
            db_connection.close()

            # Redirect to admin dashboard after successful submission
            return redirect(url_for('admin_dashboard'))

        except mysql.connector.Error as e:
            # Handle database errors
            return render_template('sportsevent_creation.html', error="An error occurred while processing your request.")

    else:
        return render_template('sportsevent_creation.html')

@app.route('/artsevent_creation', methods=['GET', 'POST'])
def artsevent_creation():
    if request.method == 'POST':
        # Retrieve values from the form
        event_name = request.form['event_name']
        category = request.form['category']
        venue = request.form['venue']
        event_date = request.form['event_date']
        event_time = request.form['event_time']
        ampm = request.form['ampm']

        try:
            # Connect to the database
            db_connection = connect_to_database()
            cursor = db_connection.cursor()

            # Insert data into the artsevent table
            insert_query = "INSERT INTO artsevent (event_name, category, venue, event_date, event_time, ampm) VALUES (%s, %s, %s, %s, %s, %s)"
            data = (event_name, category, venue, event_date, event_time, ampm)
            cursor.execute(insert_query, data)
            db_connection.commit()

            # Close database connection
            cursor.close()
            db_connection.close()

            # Redirect to admin dashboard after successful submission
            return redirect(url_for('admin_dashboard'))

        except mysql.connector.Error as e:
            # Handle database errors
            return render_template('artsevent_creation.html', error="An error occurred while scheduling the event.")
    
    # This block is missing in your original code, it handles GET requests
    else:
        return render_template('artsevent_creation.html')

@app.route('/delete_event', methods=['POST'])
def delete_event():
    if request.method == 'POST':
        event_type = request.form['event_type']
        event_name = request.form['event_name']

        try:
            db_connection = connect_to_database()
            cursor = db_connection.cursor()

            # Determine which table to delete from based on event type
            if event_type == 'arts':
                delete_query = "DELETE FROM artsevent WHERE event_name = %s"
            elif event_type == 'sports':
                delete_query = "DELETE FROM sportsevent WHERE event_name = %s"

            cursor.execute(delete_query, (event_name,))
            db_connection.commit()

            cursor.close()
            db_connection.close()

            return jsonify({'success': True})

        except mysql.connector.Error as e:
            return jsonify({'success': False, 'error': str(e)})
        
import json
from flask import jsonify, request

@app.route('/get_event_names_deletion', methods=['GET'])
def get_event_names_deletion():
    category = request.args.get('category')
    try:
        db_connection = connect_to_database()
        cursor = db_connection.cursor()

        cursor.execute("SELECT event_name FROM {}event".format(category))
        event_names = [row[0] for row in cursor.fetchall()]
        print(event_names)

        cursor.close()
        db_connection.close()

        return jsonify(event_names)

    except mysql.connector.Error as e:
        print("An error occurred while retrieving data from the database:", e)
        return jsonify(error='An error occurred while retrieving data from the database.')


@app.route('/get_event_names', methods=['GET'])
def get_event_names():
    try:
        db_connection = connect_to_database()
        cursor = db_connection.cursor()

        # Query event names from the database for the selected category
        category = request.args.get('category')  # Get category from request parameters
        cursor.execute("SELECT event_name FROM event_names WHERE event_category = %s", (category,))
        event_names = [row[0] for row in cursor.fetchall()]

        # Close database connection
        cursor.close()
        db_connection.close()

        return jsonify(event_names)

    except mysql.connector.Error as e:
        print("An error occurred while retrieving data from the database:", e)
        return jsonify([])



@app.route('/get_all_arts_venues', methods=['GET'])
def get_all_arts_venues():
    try:
        print("Fetching all venues...")
        db_connection = connect_to_database()
        cursor = db_connection.cursor()

        # Query all venues from the arts_venues table
        cursor.execute("SELECT venue FROM arts_venues")
        venues = [row[0] for row in cursor.fetchall()]

        # Close database connection
        cursor.close()
        db_connection.close()

        return jsonify(venues)

    except mysql.connector.Error as e:
        print("An error occurred while retrieving data from the database:", e)
        return jsonify(error='An error occurred while retrieving data from the database.')


def get_events(event_type):
    try:
        db_connection = connect_to_database()
        cursor = db_connection.cursor()

        # Query event names from the database for the selected category
        cursor.execute("SELECT event_name FROM SportsEvents WHERE event_type = %s", (event_type,))
        event_names = [row[0] for row in cursor.fetchall()]

        # Close database connection
        cursor.close()
        db_connection.close()

        return event_names

    except mysql.connector.Error as e:
        print("An error occurred while retrieving data from the database:", e)
        return []

@app.route('/get_events', methods=['POST'])
def get_events_route():
    event_type = request.form['event_type']
    event_names = get_events(event_type)
    return jsonify(event_names)


#for sports venues dropdown
@app.route('/get_all_sports_venues', methods=['GET'])
def get_all_sports_venues():
    try:
        print("Fetching all venues...")
        db_connection = connect_to_database()
        cursor = db_connection.cursor()

        # Query all venues from the arts_venues table
        cursor.execute("SELECT venue FROM sports_venues")
        venues = [row[0] for row in cursor.fetchall()]

        # Close database connection
        cursor.close()
        db_connection.close()

        return jsonify(venues)

    except mysql.connector.Error as e:
        print("An error occurred while retrieving data from the database:", e)
        return jsonify(error='An error occurred while retrieving data from the database.')

@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('home'))

@app.route('/house_captain')
def house_captain():
    return render_template('house_captain.html')

@app.route('/student_login', methods=['GET', 'POST'])
def student_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:
            db_connection = connect_to_database()
            cursor = db_connection.cursor()

            query = "SELECT * FROM student WHERE username = %s AND password = %s"
            data = (username, password)
            cursor.execute(query, data)
            result = cursor.fetchone()

            if result:
                session['username'] = username
                return redirect(url_for('profile', username=username))
            else:
                return render_template('student_login.html', error="Invalid username or password")

        except mysql.connector.Error as e:
            return render_template('student_login.html', error="An error occurred while processing your request.")

        finally:
            cursor.close()
            db_connection.close()

    else:
        return render_template('student_login.html')

@app.route('/profile/<username>', methods=['GET', 'POST'])
def profile(username):
    if request.method == 'POST':
        event_name = request.form['event_name']
        return register_event(username, event_name)
    else:
        try:
            db_connection = connect_to_database()
            cursor = db_connection.cursor()

            query = "SELECT Name, Register_number, House_name FROM student WHERE Username = %s"
            cursor.execute(query, (username,))
            user_details = cursor.fetchone()

            if user_details:
                name, register_number, house_name = user_details

                # Fetch available events from artsevent table
                cursor.execute("SELECT event_name, category, venue, event_date, event_time, ampm FROM artsevent")
                arts_events = cursor.fetchall()

                # Fetch available events from sportsevent table
                cursor.execute("SELECT event_name, event_type , venue, event_date, event_time, ampm FROM sportsevent")
                sports_events = cursor.fetchall()

                events = arts_events  + sports_events

                return render_template('profile.html', name=name, register_number=register_number, house_name=house_name, events=events)
            else:
                return "User not found"

        except mysql.connector.Error as e:
            return "An error occurred while fetching user details"

        finally:
            cursor.close()
            db_connection.close()


            


def register_event(username, event_name):
    try:
        db_connection = connect_to_database()
        cursor = db_connection.cursor()

        # Check if the user is already registered for the event
        cursor.execute("SELECT * FROM registered_art_events WHERE username = %s AND event_name = %s", (username, event_name))
        if cursor.fetchone():
            return render_template('profile.html', error="You are already registered for this event.")

        # If not registered, insert the registration into the database
        insert_query = "INSERT INTO registered_art_events (username, event_name) VALUES (%s, %s)"
        data = (username, event_name)
        cursor.execute(insert_query, data)
        db_connection.commit()

        # Close database connection
        cursor.close()
        db_connection.close()

        return redirect(url_for('profile', username=username, success="Event registration successful."))

    except mysql.connector.Error as e:
        # Handle database errors
        return render_template('profile.html', error="An error occurred while registering for the event.")
    

from flask import request

@app.route('/register_event', methods=['POST'])
def process_event_registration():
    if request.method == 'POST':
        event_name = request.form['event_name']
        user_name = request.form['user_name']  # Assuming you have a way to get the user's name
        register_number = request.form['register_number']  # Assuming you have a way to get the user's register number
        house_name = request.form['house_name']  # Assuming you have a way to get the user's house name

        # Fetch event details
        db_connection = connect_to_database()
        cursor = db_connection.cursor()

        cursor.execute("SELECT category, venue, event_date, event_time FROM artsevent WHERE event_name = %s", (event_name,))
        event_details = cursor.fetchone()

        if event_details:
            category, venue, event_date, event_time = event_details

            if category in ['Music', 'Dance', 'Literary', 'Theater', 'Fine Arts']:
                insert_query = "INSERT INTO registered_art_events (user_name, register_number, house_name, event_name, category, venue, event_date, event_time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            else:
                return "Event category not supported for arts events!"

            # Check if the user has already registered for the event
            cursor.execute("SELECT * FROM registered_art_events WHERE user_name = %s AND event_name = %s", (user_name, event_name))
            existing_registration = cursor.fetchone()
            if existing_registration:
                return "You have already registered for this event!"

            cursor.execute(insert_query, (user_name, register_number, house_name, event_name, category, venue, event_date, event_time))
            db_connection.commit()

            cursor.close()
            db_connection.close()

            return "Event registered successfully!"
        else:
            return "Event not found!"

    else:
        return "Method not allowed"


@app.route('/register_sports_event', methods=['POST'])
def process_event_sportsregistration():
    if request.method == 'POST':
        event_name = request.form['event_name']
        user_name = request.form['user_name']  # Assuming you have a way to get the user's name
        register_number = request.form['register_number']  # Assuming you have a way to get the user's register number
        house_name = request.form['house_name']  # Assuming you have a way to get the user's house 
        event_type = request.form['event_type']

        # Fetch event details from sports events table
        db_connection = connect_to_database()
        cursor = db_connection.cursor()

        cursor.execute("SELECT event_type, venue, event_date, event_time FROM sportsevent WHERE event_name = %s", (event_name,))
        event_details = cursor.fetchone()

        if event_details:
            event_type, venue, event_date, event_time = event_details

            print("Event Date:", event_date)  # Print the value of event_date
            print("Event Time:", event_type)  # Print the value of event_time

            insert_query = "INSERT INTO registered_sports_events (user_name, register_number, house_name, event_name, event_type, venue, event_date, event_time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

            # Check if the user has already registered for the event
            cursor.execute("SELECT * FROM registered_sports_events WHERE user_name = %s AND event_name = %s", (user_name, event_name))
            existing_registration = cursor.fetchone()
            if existing_registration:
                return "You have already registered for this event!"

            cursor.execute(insert_query, (user_name, register_number, house_name, event_name, event_type, venue, event_date, event_time))

            db_connection.commit()

            cursor.close()
            db_connection.close()

            return "Event registered successfully!"
        else:
            return "Event not found!"

    else:
        return "Method not allowed"


from datetime import datetime, time  # Import datetime module
import json  # Import json module

# Route to handle displaying registered events
@app.route('/display_registered_events/<event_type>')
def display_registered_events(event_type):
    if event_type == "arts":
        table_name = "registered_art_events"
    elif event_type == "sports":
        table_name = "registered_sports_events"
    else:
        return jsonify([])  # Return empty list for unknown event type

    try:
        db_connection = connect_to_database()
        cursor = db_connection.cursor()
        cursor.execute(f"SELECT event_name, venue, event_date, event_time FROM {table_name}")
        events = cursor.fetchall()

        # Convert timedelta objects to string representations
        formatted_events = []
        for event in events:
            # Convert date and time to datetime objects
            event_datetime = datetime.combine(event[2], time.fromisoformat(str(event[3])))
            
            # Format datetime objects as strings
            formatted_event = {
                'event_name': event[0],
                'venue': event[1],
                'event_date': event_datetime.strftime('%Y-%m-%d'),  # Format date as string
                'event_time': event_datetime.strftime('%H:%M:%S')  # Format time as string
            }
            formatted_events.append(formatted_event)

        return json.dumps(formatted_events)  # Convert list to JSON string

    except Exception as e:
        print("Error:", e)
        return json.dumps([])  # Return empty list as JSON string





@app.route('/student_signup', methods=['GET', 'POST'])
def student_signup():
    if request.method == 'POST':
        name = request.form['name']
        register_number = request.form['register_number']
        semester = request.form['semester']
        department = request.form['department']
        house_name = request.form['house_name']
        username = request.form['username']
        password = request.form['password']

        try:
            db_connection = connect_to_database()
            cursor = db_connection.cursor()

            insert_query = "INSERT INTO student (Name, Register_number, Semester, Department, House_name, Username, Password) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            data = (name, register_number, semester, department, house_name, username, password)
            cursor.execute(insert_query, data)
            db_connection.commit()

            return redirect(url_for('student_login'))

        except mysql.connector.Error as e:
            return render_template('student_signup.html', error="An error occurred while processing your request.")

        finally:
            cursor.close()
            db_connection.close()

    else:
        return render_template('student_signup.html')

if __name__ == '__main__':
    app.run(debug=True)
