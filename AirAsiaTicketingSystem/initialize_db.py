import db_base as db
import csv

class AirAsiaDatabase(db.DBbase):
    passenger_list=[]
    flight_list=[]

    def __init__(self, db_name='AirAsiaTicketingDB.sqlite'):
        super().__init__(db_name)

    def reset_database(self):
        try:
            sql = """
                DROP TABLE IF EXISTS Ticket;  -- Drop Ticket table first
                DROP TABLE IF EXISTS Passenger;  -- Drop Passenger table first
                DROP TABLE IF EXISTS Flight;  -- Drop Flight table first

                
                CREATE TABLE  Flight (
                    flightID INTEGER PRIMARY KEY ,
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
                    ticketNum INTEGER  PRIMARY KEY ,
                    customer_id INTEGER NOT NULL,
                    flightID INTEGER NOT NULL,
                    booking_date TEXT NOT NULL,
                    price REAL NOT NULL,
                    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id),
                    FOREIGN KEY (flightID) REFERENCES Flight(flightID)
                );

                
            """

            super().execute_script(sql)  # Use execute_script from db_base.py
            print("Database and tables created successfully.")

        except Exception as e:
            print(f"An error occurred: {e}")

    def read_passenger_data(self,file_name):
        """Read passenger data from a CSV file and store it in the passenger_list."""
        self.passenger_list = []  # Clear the list before reading new data

        try:
            with open(file_name, 'r') as record:
                csv_contents = csv.reader(record)
                next(csv_contents)  # Skip header row
                for row in csv_contents:
                    passenger = {
                        "title": row[0],
                        "first_name": row[1],
                        "last_name": row[2],
                        "DOB": row[3],
                        "email": row[4],
                        "phone": row[5],
                        "age": int(row[6])  # Assuming age is an integer
                    }
                    self.passenger_list.append(passenger)  # Add passenger dictionary to the list
        except Exception as e:
            print(f"Error reading CSV: {e}")

    def save_passenger_to_database(self):
        """Save passenger data to the database."""
        for item in self.passenger_list:
            try:
                super().get_cursor.execute("""
                        INSERT INTO Passenger (title, firstName, lastName, DOB, email, phone, age)
                        VALUES (?, ?, ?, ?, ?, ?, ?)""",
                                           (item["title"], item["first_name"], item["last_name"],
                                            item["DOB"], item["email"], item["phone"], item["age"]))
                super().get_connection.commit()  # Commit the transaction
                #print(f"Saved passenger: {item['first_name']} {item['last_name']} with email: {item['email']}")
            except Exception as e:
                print(f"Error saving passenger: {e}")

    def list_passengers(self):
        """List all passengers in the database."""
        try:
            self.get_cursor.execute("SELECT * FROM Passenger")
            return self.get_cursor.fetchall()  # Return all passengers
        except Exception as e:
            print("Error listing passengers:", e)





    # Reading flight data from csv file
    def read_flight_data(self, file_name):
        self.flight_list = []  # Clear the list before reading new data
        try:
            with open(file_name, 'r') as record:  # Open the CSV file for reading
                csv_contents = csv.reader(record)  # Create a CSV reader object
                next(csv_contents)  # Skip the header row
                for row in csv_contents:# Iterate over the remaining rows in the CSV
                    flight = {
                        "flightID": row[0],
                        "airportFrom":row[1],
                        "airportTo":row[2],
                        "aircraftID":row[3],
                        "departureDate":row[4],
                        "departureTime":row[5],
                        "departureGate":row[6],
                        "arrivalGate":row[7],
                        "duration":row[8],
                        "arrivalDate":row[9],
                        "arrivalTime":row[10]
                    }
                    self.flight_list.append(flight)  # Add the flight dictionary to the list


        except Exception as e:  # Catch any exceptions that occur
            print(f"Error saving passenger: {e}")  # Print the exception message

        print(self.flight_list)
    def save_flight_to_database(self):
        """Save flight data to the database."""
        for item in self.flight_list:
            try:
                super().get_cursor.execute("""
                           INSERT INTO Flight (flightID,airportFrom,airportTo,aircraftID,departureDate,
                           departureTime,departureGate,arrivalGate,duration,arrivalDate,arrivalTime)
                           VALUES (?, ?, ?, ?, ?, ?, ?,?,?,?,?)""",
                                           (item["flightID"], item["airportFrom"], item["airportTo"],
                                            item["aircraftID"], item["departureDate"], item["departureTime"], item["departureGate"],
                                            item["arrivalGate"],item["duration"],item["arrivalDate"].item["arrivalTime"]))
                super().get_connection.commit()  # Commit the transaction

            except Exception as e:
                print(f"Error saving flights: {e}")

    def list_flights(self):
        """List all Flights in the database."""
        try:
            self.get_cursor.execute("SELECT * FROM Flight")
            return self.get_cursor.fetchall()  # Return all passengers
        except Exception as e:
            print("Error listing Flights:", e)




# Initialize and set up the database tables and load data
if __name__ == "__main__":

    airasia_db = AirAsiaDatabase()
    airasia_db.reset_database() # Create/reset the database

    #loading passenger data from passenger.csv
    airasia_db.read_passenger_data("Passenger.csv")  # Read data from CSV
    airasia_db.save_passenger_to_database()  # Save data to the database

    #loading flight data from flight_list .csv
    airasia_db.read_flight_data("flight_list.csv")  # Read data from CSV
    airasia_db.save_flight_to_database  #Save data to the database





    #printing  passengers list
    passengers = airasia_db.list_passengers()
    print("Passenger Details")
    for passenger in passengers:
        print(f"Passenger ID: {passenger[0]}, Name: {passenger[2]} {passenger[3]}, Email: {passenger[4]}")

    # printing flight list
    try:
        flights = airasia_db.list_flights()
        if not flights:
            print("No flights found.")
        else:
            print("Flight Details")
            for flight in flights:
                print(
                    f"Flight ID: {flight[0]}, Flight Number: {flight[1]}, Departure: {flight[2]}, Arrival: {flight[3]}")
    except Exception as e:
        print(f"An error occurred while retrieving flights: {e}")

    # flights = airasia_db.list_flights()
    # print("Flight Details")
    # for flight in flights:
    #     print(f"Flight ID: {flight[0]}, airportFrom: {flight[2]} ,airportTo {passenger[3]}, aircraftId: {passenger[4]}")
    #
    # airasia_db.close_db()  # Close the database connection

