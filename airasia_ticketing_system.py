import db_base as db

class AirAsiaDatabase(db.DBbase):
    def __init__(self, db_name='AirAsiaTicketingDB.sqlite'):
        super().__init__(db_name)

    def reset_database(self):
        try:
            sql = """
                CREATE TABLE IF NOT EXISTS Airport (
                    airportCode VARCHAR(5) PRIMARY KEY,
                    name TEXT NOT NULL,
                    city TEXT NOT NULL,
                    country TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS Aircraft (
                    aircraftID INTEGER PRIMARY KEY ,
                    model TEXT NOT NULL,
                    capacity INTEGER NOT NULL,
                    registration_number TEXT UNIQUE NOT NULL
                );

                CREATE TABLE IF NOT EXISTS Employee (
                    employee_id INTEGER PRIMARY KEY ,
                    firstName TEXT NOT NULL,
                    lastName TEXT NOT NULL,
                    role TEXT NOT NULL,
                    email TEXT UNIQUE,
                    phone TEXT UNIQUE,
                    
                );

                CREATE TABLE IF NOT EXISTS Flight (
                    flightID INTEGER PRIMARY KEY ,
                    airportFrom VARCHAR(5),
                    airportTo VARCHAR(5),
                    aircraftID INTEGER,
                    departureDate TEXT NOT NULL,
                    departureTime TEXT NOT NULL,
                    departureGate TEXT,
                    arrivalGate TEXT,
                    duration REAL NOT NULL,
                    FOREIGN KEY (airportFrom) REFERENCES Airport(airportCode),
                    FOREIGN KEY (airportTo) REFERENCES Airport(airportCode),
                    FOREIGN KEY (aircraftID) REFERENCES Aircraft(aircraftID)
                );

                CREATE TABLE IF NOT EXISTS Customer (
                    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL
                    firstName TEXT NOT NULL,
                    lastName TEXT NOT NULL,
                    DOB TEXT NOT NULL,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    phone TEXT UNIQUE
                );

                CREATE TABLE IF NOT EXISTS Ticket (
                    ticketNum INTEGER  PRIMARY KEY ,
                    customer_id INTEGER NOT NULL,
                    flightID INTEGER NOT NULL,
                    booking_date TEXT NOT NULL,
                    price REAL NOT NULL,
                    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id),
                    FOREIGN KEY (flightID) REFERENCES Flight(flightID)
                );

                CREATE TABLE IF NOT EXISTS FlightCrew (
                    flightID INTEGER ,
                    employee_id INTEGER,
                    PRIMARY KEY (flightID, employee_id),
                    FOREIGN KEY (flightID) REFERENCES Flight(flightID),
                    FOREIGN KEY (employee_id) REFERENCES Employee(employee_id)
                );
            """

            super().execute_script(sql)  # Use execute_script from db_base.py
            print("Database and tables created successfully.")

        except Exception as e:
            print(f"An error occurred: {e}")

# Initialize and set up the database tables
if __name__ == "__main__":
    airasia_db = AirAsiaDatabase()
    airasia_db.reset_database()
