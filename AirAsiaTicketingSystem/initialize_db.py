import db_base as db
import csv
from datetime import datetime

class AirAsiaDatabase(db.DBbase):
    passenger_list = []
    flight_list = []
    ticket_list = []
    valid_titles = {"Mr.", "Ms.", "Mrs.", "Miss", "Dr."}  # Set of valid titles for passengers
    seen_emails = set()  # Track emails to avoid duplicates
    seen_flight_ids = set()  # Track flight IDs to avoid duplicates

    def __init__(self, db_name='AirAsiaTicketingDB.sqlite'):
        super().__init__(db_name)

    def reset_database(self):
        """Reset the database and create required tables."""
        try:
            sql = """
                DROP TABLE IF EXISTS Ticket;
                DROP TABLE IF EXISTS Passenger;
                DROP TABLE IF EXISTS Flight;

                CREATE TABLE Flight (
                    flightID INTEGER PRIMARY KEY,
                    airportFrom VARCHAR(5),
                    airportTo VARCHAR(5),
                    aircraftID INTEGER,
                    departureDate TEXT NOT NULL,
                    departureTime TEXT NOT NULL,
                    departureGate TEXT,
                    arrivalGate TEXT, 
                    duration REAL NOT NULL,
                    arrivalDate TEXT NOT NULL,
                    arrivalTime TEXT NOT NULL
                );

                CREATE TABLE Passenger (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    firstName TEXT NOT NULL,
                    lastName TEXT NOT NULL,
                    DOB TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    phone TEXT UNIQUE,
                    age INTEGER NOT NULL
                );

                CREATE TABLE Ticket (
                    ticketNum INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    flightID INTEGER NOT NULL,
                    booking_date TEXT NOT NULL,
                    price REAL NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES Passenger(user_id),
                    FOREIGN KEY (flightID) REFERENCES Flight(flightID)
                );
            """
            super().execute_script(sql)
            print("Database and tables created successfully.")

        except Exception as e:
            print(f"An error occurred during database reset: {e}")

    def validate_date(self, date_str):
        """Check if date is in YYYY-MM-DD format."""
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    def validate_time(self, time_str):
        """Check if time is in HH:MM format."""
        try:
            datetime.strptime(time_str, '%H:%M')
            return True
        except ValueError:
            return False

    def validate_age(self, age):
        """Ensure age is a positive integer."""
        return age.isdigit() and int(age) > 0

    def validate_phone(self, phone):
        """Check if the phone number matches xxx-xxx-xxxx format."""
        return phone.count("-") == 2 and all(part.isdigit() and len(part) == 3 for part in phone.split("-"))

    def read_passenger_data(self, file_name):
        """Read passenger data from a CSV file and validate before saving."""
        self.passenger_list = []
        try:
            with open(file_name, 'r') as file:
                csv_contents = csv.reader(file)
                next(csv_contents)
                row_num = 1  # Track row number for error reporting
                for row in csv_contents:
                    row_num += 1
                    # Validate fields
                    if row[0] not in self.valid_titles:
                        print(f"Skipping invalid title in row {row_num}: {row}")
                        continue
                    if not self.validate_date(row[3]):
                        print(f"Skipping invalid DOB in row {row_num}: {row}")
                        continue
                    if row[4] in self.seen_emails:
                        print(f"Skipping duplicate email in row {row_num}: {row[4]}")
                        continue
                    if not self.validate_phone(row[5]):
                        print(f"Skipping invalid phone number in row {row_num}: {row[5]}")
                        continue
                    if not self.validate_age(row[6]):
                        print(f"Skipping invalid age in row {row_num}: {row[6]}")
                        continue

                    # Add valid row to passenger list and track email
                    self.seen_emails.add(row[4])
                    passenger = {
                        "title": row[0],
                        "first_name": row[1],
                        "last_name": row[2],
                        "DOB": row[3],
                        "email": row[4],
                        "phone": row[5],
                        "age": int(row[6])
                    }
                    self.passenger_list.append(passenger)
        except Exception as e:
            print(f"Error reading passenger CSV: {e}")

    def save_passenger_to_database(self):
        """Save validated passenger data to the database."""
        for item in self.passenger_list:
            try:
                super().get_cursor.execute("""
                    INSERT INTO Passenger (title, firstName, lastName, DOB, email, phone, age)
                    VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    (item["title"], item["first_name"], item["last_name"],
                     item["DOB"], item["email"], item["phone"], item["age"]))
                super().get_connection.commit()
            except Exception as e:
                print(f"Error saving passenger: {e}")

    def read_flight_data(self, file_name):
        """Read flight data from a CSV file and validate before saving."""
        self.flight_list = []
        try:
            with open(file_name, 'r') as file:
                csv_contents = csv.reader(file)
                next(csv_contents)
                row_num = 1
                for row in csv_contents:
                    row_num += 1
                    if row[0] in self.seen_flight_ids:
                        print(f"Skipping duplicate flight ID in row {row_num}: {row[0]}")
                        continue
                    if not self.validate_date(row[4]) or not self.validate_date(row[9]):
                        print(f"Skipping invalid date in row {row_num}: {row[4]}, {row[9]}")
                        continue
                    if not self.validate_time(row[5]) or not self.validate_time(row[10]):
                        print(f"Skipping invalid time in row {row_num}: {row[5]}, {row[10]}")
                        continue
                    try:
                        duration = float(row[8])
                        if duration <= 0:
                            print(f"Skipping invalid duration in row {row_num}: {duration}")
                            continue
                    except ValueError:
                        print(f"Skipping invalid duration in row {row_num}: {row[8]}")
                        continue

                    # Add flight details to list and track flight ID
                    self.seen_flight_ids.add(row[0])
                    flight_details = {
                        "flightID": row[0],
                        "airportFrom": row[1],
                        "airportTo": row[2],
                        "aircraftID": row[3],
                        "departureDate": row[4],
                        "departureTime": row[5],
                        "departureGate": row[6],
                        "arrivalGate": row[7],
                        "duration": duration,
                        "arrivalDate": row[9],
                        "arrivalTime": row[10]
                    }
                    self.flight_list.append(flight_details)
        except Exception as e:
            print(f"Error reading flight CSV: {e}")

    def save_flight_to_database(self):
        """Save validated flight data to the database."""
        for item in self.flight_list:
            try:
                super().get_cursor.execute("""
                    INSERT INTO Flight (flightID, airportFrom, airportTo, aircraftID, departureDate,
                    departureTime, departureGate, arrivalGate, duration, arrivalDate, arrivalTime)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (item["flightID"], item["airportFrom"], item["airportTo"],
                     item["aircraftID"], item["departureDate"], item["departureTime"],
                     item["departureGate"], item["arrivalGate"], item["duration"],
                     item["arrivalDate"], item["arrivalTime"]))
                super().get_connection.commit()
            except Exception as e:
                print(f"Error saving flight {item['flightID']}: {e}")

    def read_ticket_data(self, file_name):
        """Read ticket data from a CSV file and validate before saving."""
        self.ticket_list = []
        try:
            with open(file_name, 'r') as file:
                csv_contents = csv.reader(file)
                next(csv_contents)
                row_num = 1
                for row in csv_contents:
                    row_num += 1
                    if not self.validate_date(row[2]):
                        print(f"Skipping invalid booking date in row {row_num}: {row[2]}")
                        continue
                    try:
                        price = float(row[3])
                        if price < 0:
                            print(f"Skipping invalid price in row {row_num}: {price}")
                            continue
                    except ValueError:
                        print(f"Skipping invalid price in row {row_num}: {row[3]}")
                        continue

                    # Add validated ticket to list
                    ticket_details = {
                        "user_id": row[0],
                        "flightID": row[1],
                        "booking_date": row[2],
                        "price": price
                    }
                    self.ticket_list.append(ticket_details)
        except Exception as e:
            print(f"Error reading ticket CSV: {e}")

    def save_ticket_to_database(self):
        """Save validated ticket data to the database."""
        for item in self.ticket_list:
            try:
                super().get_cursor.execute("""
                    INSERT INTO Ticket (user_id, flightID, booking_date, price)
                    VALUES (?, ?, ?, ?)""",
                    (item["user_id"], item["flightID"], item["booking_date"], item["price"]))
                super().get_connection.commit()
            except Exception as e:
                print(f"Error saving ticket: {e}")
