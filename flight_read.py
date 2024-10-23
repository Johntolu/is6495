import DBbase as db  # Import the custom DBbase module for database operations
import csv  # Import the csv module for reading CSV files

class Flight:
    def __init__(self, row):
        # Initialize Flight object attributes based on the CSV row
        self.flight_id = row[0]  # Read flight_id from the row
        self.airport_to = row[1]  # Read destination airport from the row
        self.departure_date = row[2]  # Read departure date from the row
        self.departure_gate = row[3]  # Read departure gate from the row
        self.arrival_gate = row[4]  # Read arrival gate from the row
        self.price = row[5]  # Read price as a single value from the row

class Flight_mod(db.DBbase):
    # Define a class that inherits from DBbase for handling CSV operations related to flight data

    def reset_or_create_db(self):
        # Method to drop and recreate the Flight table in the database
        try:
            sql = """
                DROP TABLE IF EXISTS Flight;  

                CREATE TABLE Flight (
                    flight_id INTEGER NOT NULL PRIMARY KEY,  
                    airport_to TEXT NOT NULL,                
                    departure_date TEXT NOT NULL,            
                    departure_gate TEXT NOT NULL,            
                    arrival_gate TEXT NOT NULL,              
                    price INTEGER                            
                );
            """
            super().execute_script(sql)  # Execute the SQL script to drop and create the table

        except Exception as e:  # Catch any exceptions that occur
            print(e)  # Print the exception message

    def read_flight_data(self, file_name):
        # Method to read flight data from a CSV file
        self.flight_list = []  # Initialize an empty list to hold Flight objects

        try:
            with open(file_name, 'r') as record:  # Open the CSV file for reading
                csv_contents = csv.reader(record)  # Create a CSV reader object
                next(record)  # Skip the header row
                for row in csv_contents:  # Iterate over the remaining rows in the CSV
                    flight = Flight(row)  # Create a Flight object for each row
                    self.flight_list.append(flight)  # Add the Flight object to the list

        except Exception as e:  # Catch any exceptions that occur
            print(e)  # Print the exception message

    def save_to_database(self):
        # Method to save flight data to the database
        print("Number of records to save: ", len(self.flight_list))  # Print the number of records
        save = input("Continue? (y/n)").lower()  # Prompt the user to confirm saving

        if save == "y":  # If the user confirms
            for item in self.flight_list:  # Iterate over each Flight object in the list
                try:
                    super().get_cursor.execute("""INSERT INTO Flight
                    (flight_id, airport_to, departure_date, departure_gate, arrival_gate, price)
                    VALUES (?, ?, ?, ?, ?, ?)""",
                    (item.flight_id, item.airport_to, item.departure_date,
                     item.departure_gate, item.arrival_gate, item.price))  # Insert flight data into the database
                    super().get_connection.commit()  # Commit the transaction to the database

                    print("Saved item: ", item.flight_id, item.airport_to, item.departure_date,
                           item.departure_gate, item.arrival_gate, item.price)  # Confirm save

                except Exception as e:  # Catch any exceptions that occur during the insert
                    print(e)  # Print the exception message
            else:
                print("Save to DB aborted")  # If the user doesn't confirm, print a message

# Create an instance of Flight_mod with the database filename
flight = Flight_mod("FlightDB.sqlite")
flight.reset_or_create_db()  # Uncomment to reset or create the database
flight.read_flight_data("flight_list.csv")  # Read flight data from the CSV file
flight.save_to_database()  # Save the flight data to the database
