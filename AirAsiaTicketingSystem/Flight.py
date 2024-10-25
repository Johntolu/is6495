# Flight.py
import db_base as db

class Flight(db.DBbase):
    def __init__(self, db_name='AirAsiaTicketingDB.sqlite'):
        super().__init__(db_name)

    def add_flight(self):
        airport_from = input("Enter departure airport: ")
        airport_to = input("Enter arrival airport: ")
        aircraft_id = input("Enter aircraft ID: ")
        departure_date = input("Enter departure date (YYYY-MM-DD): ")
        departure_time = input("Enter departure time (HH:MM): ")
        departure_gate = input("Enter departure gate: ")
        arrival_gate = input("Enter arrival gate: ")
        duration = float(input("Enter duration (in hours): "))
        arrival_date = input("Enter arrival date (YYYY-MM-DD): ")
        arrival_time = input("Enter arrival time (HH:MM): ")

        try:
            self.get_cursor.execute("""
                INSERT INTO Flight (airportFrom, airportTo, aircraftID, departureDate,
                departureTime, departureGate, arrivalGate, duration, arrivalDate, arrivalTime)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                 (airport_from, airport_to, aircraft_id, departure_date,
                  departure_time, departure_gate, arrival_gate, duration,
                  arrival_date, arrival_time)
            )
            self.get_connection.commit()  # Commit the transaction
            print("Flight added successfully.")
        except Exception as e:
            print(f"An error adding flight occurred: {e}")

    def view_flights(self):
        """Display details of a specific flight based on flight ID or show all flights if no ID is provided."""
        flight_id = input("Enter the Flight ID to view a specific flight (leave blank to view all flights): ")

        try:
            if flight_id:
                # Query for a specific flight by flight_id
                self.get_cursor.execute("""
                    SELECT flightID, airportFrom, airportTo, departureDate, departureTime, arrivalDate, arrivalTime, duration
                    FROM Flight WHERE flightID = ?""", (flight_id,))
                flight = self.get_cursor.fetchone()

                if flight:
                    print("\n=== Flight Details ===")
                    print(f"Flight ID: {flight[0]}")
                    print(f"  From: {flight[1]}  To: {flight[2]}")
                    print(f"  Departure: {flight[3]} {flight[4]}")
                    print(f"  Arrival: {flight[5]} {flight[6]}")
                    print(f"  Duration: {flight[7]} hours")
                    print("-" * 30)
                else:
                    print(f"No flight found with Flight ID: {flight_id}")

            else:
                # Query for all flights if no flight_id is provided
                self.get_cursor.execute("""
                    SELECT flightID, airportFrom, airportTo, departureDate, departureTime, arrivalDate, arrivalTime, duration
                    FROM Flight""")
                flights = self.get_cursor.fetchall()

                if flights:
                    print("\n=== All Flights ===")
                    for flight in flights:
                        print(f"Flight ID: {flight[0]}")
                        print(f"  From: {flight[1]}  To: {flight[2]}")
                        print(f"  Departure: {flight[3]} {flight[4]}")
                        print(f"  Arrival: {flight[5]} {flight[6]}")
                        print(f"  Duration: {flight[7]} hours")
                        print("-" * 30)
                else:
                    print("No flights available.")

        except Exception as e:
            print(f"Error retrieving flights: {e}")

    def update_flight(self):

        flight_id=input("Enter the flight_ID of the flight whose details you want to update")
        #Update flight information for a specific flight ID.
        print(f"Updating flight details for flight ID: {flight_id}")

        # Choose the field to update
        field = input(
            "Enter the field to update (airportFrom, airportTo, aircraftID, departureDate, departureTime, departureGate, arrivalGate, duration, arrivalDate, arrivalTime): ")
        new_value = input(f"Enter the new value for {field}: ")

        try:
            sql = f"UPDATE Flight SET {field} = ? WHERE flightID = ?"
            super().get_cursor.execute(sql, (new_value, flight_id))
            super().get_connection.commit()  # Commit the changes
            print(f"Flight ID {flight_id} updated successfully.")
        except Exception as e:
            print(f"Error updating flight ID {flight_id}: {e}")

    def delete_flight(self):

        flight_id=input("Enter the flight_id of the flight you want to delete : ")
        # Delete a flight based on flight ID."""
        confirmation = input(f"Are you sure you want to delete flight ID {flight_id}? (yes/no): ")
        if confirmation.lower() != 'yes':
            print("Flight deletion cancelled.")
            return
        else:
            try:
                super().get_cursor.execute("DELETE FROM Flight WHERE flightID = ?", (flight_id,))
                super().get_connection.commit()  # Commit the transaction
                print(f"Flight ID {flight_id} deleted successfully.")
            except Exception as e:
                print(f"Error deleting flight ID {flight_id}: {e}")

# import DBbase as db  # Import the custom DBbase module for database operations
# import csv  # Import the csv module for reading CSV files
#
# class Flight:
#     def __init__(self, row):
#         # Initialize Flight object attributes based on the CSV row
#         self.flight_id = row[0]  # Read flight_id from the row
#         self.airport_to = row[1]  # Read destination airport from the row
#         self.departure_date = row[2]  # Read departure date from the row
#         self.departure_gate = row[3]  # Read departure gate from the row
#         self.arrival_gate = row[4]  # Read arrival gate from the row
#         self.price = row[5]  # Read price as a single value from the row
















































































































# # class Flight_mod(db.DBbase):
# #     # Define a class that inherits from DBbase for handling CSV operations related to flight data
# #
# #     def reset_or_create_db(self):
# #         # Method to drop and recreate the Flight table in the database
# #         try:
# #             sql = """
# #                 DROP TABLE IF EXISTS Flight;
# #
# #                 CREATE TABLE Flight (
# #                     flight_id INTEGER NOT NULL PRIMARY KEY,
# #                     airport_to TEXT NOT NULL,
# #                     departure_date TEXT NOT NULL,
# #                     departure_gate TEXT NOT NULL,
# #                     arrival_gate TEXT NOT NULL,
# #                     price INTEGER
# #                 );
# #             """
# #             super().execute_script(sql)  # Execute the SQL script to drop and create the table
# #
# #         except Exception as e:  # Catch any exceptions that occur
# #             print(e)  # Print the exception message
#
#     def read_flight_data(self, file_name):
#         # Method to read flight data from a CSV file
#         self.flight_list = []  # Initialize an empty list to hold Flight objects
#
#         try:
#             with open(file_name, 'r') as record:  # Open the CSV file for reading
#                 csv_contents = csv.reader(record)  # Create a CSV reader object
#                 next(record)  # Skip the header row
#                 for row in csv_contents:  # Iterate over the remaining rows in the CSV
#                     flight = Flight(row)  # Create a Flight object for each row
#                     self.flight_list.append(flight)  # Add the Flight object to the list
#
#         except Exception as e:  # Catch any exceptions that occur
#             print(e)  # Print the exception message
#
#     def save_to_database(self):
#         # Method to save flight data to the database
#         print("Number of records to save: ", len(self.flight_list))  # Print the number of records
#         save = input("Continue? (y/n)").lower()  # Prompt the user to confirm saving
#
#         if save == "y":  # If the user confirms
#             for item in self.flight_list:  # Iterate over each Flight object in the list
#                 try:
#                     super().get_cursor.execute("""INSERT INTO Flight
#                     (flight_id, airport_to, departure_date, departure_gate, arrival_gate, price)
#                     VALUES (?, ?, ?, ?, ?, ?)""",
#                     (item.flight_id, item.airport_to, item.departure_date,
#                      item.departure_gate, item.arrival_gate, item.price))  # Insert flight data into the database
#                     super().get_connection.commit()  # Commit the transaction to the database
#
#                     print("Saved item: ", item.flight_id, item.airport_to, item.departure_date,
#                            item.departure_gate, item.arrival_gate, item.price)  # Confirm save
#
#                 except Exception as e:  # Catch any exceptions that occur during the insert
#                     print(e)  # Print the exception message
#             else:
#                 print("Save to DB aborted")  # If the user doesn't confirm, print a message
#
# # Create an instance of Flight_mod with the database filename
# flight = Flight_mod("FlightDB.sqlite")
# flight.reset_or_create_db()  # Uncomment to reset or create the database
# flight.read_flight_data("flight_list.csv")  # Read flight data from the CSV file
# flight.save_to_database()  # Save the flight data to the database
