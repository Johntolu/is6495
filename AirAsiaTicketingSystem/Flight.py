# Flight.py
import db_base as db
from datetime import datetime

class Flight(db.DBbase):
    def __init__(self, db_name='AirAsiaTicketingDB.sqlite'):
        super().__init__(db_name)

    def add_flight(self):
        airport_from = input("Enter departure airport: ")
        airport_to = input("Enter arrival airport: ")
        aircraft_id = input("Enter aircraft ID: ")

        # Validate departure date
        while True:
            departure_date = input("Enter departure date (YYYY-MM-DD): ")
            if self.validate_date(departure_date):
                break
            print("Error: Invalid date format. Please use YYYY-MM-DD.")

        # Validate departure time
        while True:
            departure_time = input("Enter departure time (HH:MM): ")
            if self.validate_time(departure_time):
                break
            print("Error: Invalid time format. Please use HH:MM.")

        departure_gate = input("Enter departure gate: ")
        arrival_gate = input("Enter arrival gate: ")
        
        # Validate duration
        while True:
            try:
                duration = float(input("Enter duration (in hours): "))
                break
            except ValueError:
                print("Error: Duration must be a number.")

        # Validate arrival date
        while True:
            arrival_date = input("Enter arrival date (YYYY-MM-DD): ")
            if self.validate_date(arrival_date):
                break
            print("Error: Invalid date format. Please use YYYY-MM-DD.")

        # Validate arrival time
        while True:
            arrival_time = input("Enter arrival time (HH:MM): ")
            if self.validate_time(arrival_time):
                break
            print("Error: Invalid time format. Please use HH:MM.")

        try:
            # Insert the flight data and get the flight ID of the new entry
            self.get_cursor.execute("""
                INSERT INTO Flight (airportFrom, airportTo, aircraftID, departureDate,
                departureTime, departureGate, arrivalGate, duration, arrivalDate, arrivalTime)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (airport_from, airport_to, aircraft_id, departure_date,
                departure_time, departure_gate, arrival_gate, duration,
                arrival_date, arrival_time)
            )
            self.get_connection.commit()  # Commit the transaction

            # Retrieve the last inserted ID
            new_flight_id = self.get_cursor.lastrowid
            print(f"Flight added successfully with Flight ID: {new_flight_id}")
            
        except Exception as e:
            print(f"An error adding flight occurred: {e}")


    def validate_time(self, time_str):
        """Check if the time is in HH:MM format."""
        try:
            datetime.strptime(time_str, '%H:%M')
            return True
        except ValueError:
            return False

    def view_flights(self):
        """Display details of a specific flight based on flight ID or show all flights if no ID is provided."""
        flight_id = input("Enter the Flight ID to view a specific flight (leave blank to view all flights): ")

        try:
            if flight_id:
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
        """Update flight information for a specific flight ID."""
        flight_id = input("Enter the Flight ID of the flight to update: ")
        print(f"Updating flight details for flight ID: {flight_id}")

        field = input(
            "Enter the field to update (airportFrom, airportTo, aircraftID, departureDate, "
            "departureTime, departureGate, arrivalGate, duration, arrivalDate, arrivalTime): "
        )
        new_value = input(f"Enter the new value for {field}: ")

        try:
            sql = f"UPDATE Flight SET {field} = ? WHERE flightID = ?"
            super().get_cursor.execute(sql, (new_value, flight_id))
            super().get_connection.commit()
            print(f"Flight ID {flight_id} updated successfully.")
        except Exception as e:
            print(f"Error updating flight ID {flight_id}: {e}")

    def delete_flight(self):
        """Delete a flight based on flight ID."""
        flight_id = input("Enter the Flight ID of the flight to delete: ")
        confirmation = input(f"Are you sure you want to delete flight ID {flight_id}? (yes/no): ")
        if confirmation.lower() != 'yes':
            print("Flight deletion cancelled.")
            return
        try:
            super().get_cursor.execute("DELETE FROM Flight WHERE flightID = ?", (flight_id,))
            super().get_connection.commit()
            print(f"Flight ID {flight_id} deleted successfully.")
        except Exception as e:
            print(f"Error deleting flight ID {flight_id}: {e}")

    def validate_date(self, date_str):
        """Check if the date is in YYYY-MM-DD format."""
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    def validate_time(self, time_str):
        """Check if the time is in HH:MM format."""
        try:
            datetime.strptime(time_str, '%H:%M')
            return True
        except ValueError:
            return False
