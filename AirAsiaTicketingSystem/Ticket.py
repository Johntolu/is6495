import re
from datetime import datetime
import db_base as db

class Ticket(db.DBbase):
    valid_titles = {"Mr.", "Ms.", "Mrs.", "Miss", "Dr."}

    def __init__(self, db_name='AirAsiaTicketingDB.sqlite'):
        super().__init__(db_name)

    def validate_date(self, date_str):
        """Check if the date is in YYYY-MM-DD format."""
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    def validate_phone(self, phone):
        """Check if the phone number matches xxx-xxx-xxxx format."""
        return bool(re.fullmatch(r'\d{3}-\d{3}-\d{4}', phone))

    def validate_age(self, age):
        """Ensure age is a positive integer."""
        return age.isdigit() and int(age) > 0

    def validate_email(self, email):
        """Simple email format validation."""
        return bool(re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email))

    def email_exists(self, email):
        """Check if the email already exists in the database."""
        try:
            self.get_cursor.execute("SELECT email FROM Passenger WHERE email = ?", (email,))
            return self.get_cursor.fetchone() is not None
        except Exception as e:
            print(f"Error checking email existence: {e}")
            return False

    def book_ticket(self):
        """Collect passenger details with validation for each input field."""

        # Collect and validate title
        title = input("Enter Title: ")
        while title not in self.valid_titles:
            print("Error: Invalid title. Valid options are: Mr., Ms., Mrs., Miss, Dr.")
            title = input("Enter Title: ")

        first_name = input("Enter First Name: ")
        last_name = input("Enter Last Name: ")

        # Validate date of birth
        while True:
            dob = input("Enter Date of Birth (YYYY-MM-DD): ")
            if self.validate_date(dob):
                break
            print("Error: Invalid date format. Please use YYYY-MM-DD.")

        # Validate email
        while True:
            email = input("Enter Email: ")
            if self.validate_email(email):
                if not self.email_exists(email):
                    break
                print("Error: Email already exists in the system. Please use a different email.")
            else:
                print("Error: Invalid email format. Please enter a valid email address.")

        # Validate phone
        while True:
            phone = input("Enter Phone Number: ")
            if self.validate_phone(phone):
                break
            print("Error: Invalid phone number format. Please use xxx-xxx-xxxx.")

        # Validate age
        while True:
            age = input("Enter Age: ")
            if self.validate_age(age):
                age = int(age)
                break
            print("Error: Age must be a positive integer.")

        try:
            # Insert passenger details into the Passenger table
            super().get_cursor.execute("""
                INSERT INTO Passenger (title, firstName, lastName, DOB, email, phone, age) 
                VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (title, first_name, last_name, dob, email, phone, age)
            )
            super().get_connection.commit()  # Commit to save passenger details

            # Get user_id of the newly inserted passenger
            user_id = super().get_cursor.lastrowid

            print(f"Passenger {first_name} {last_name} added successfully with User ID: {user_id}")

        except Exception as e:
            print(f"Error saving passenger details: {e}")
            return

        # Display available flights and collect flight ID
        try:
            print("\n=== Available Flights ===")
            self.get_cursor.execute("SELECT flightID, airportFrom, airportTo, departureDate, departureTime FROM Flight")
            flights = self.get_cursor.fetchall()

            if flights:
                for flight in flights:
                    print(f"Flight ID: {flight[0]}, From: {flight[1]} To: {flight[2]}, Departure: {flight[3]} {flight[4]}")
                print("-" * 30)
            else:
                print("No available flights at the moment.")
                return

        except Exception as e:
            print(f"Error retrieving flights: {e}")
            return

        # Validate selected flight ID
        while True:
            flight_id = input("Enter the Flight ID you want to book a ticket for: ")
            try:
                self.get_cursor.execute("SELECT flightID FROM Flight WHERE flightID = ?", (flight_id,))
                if self.get_cursor.fetchone():
                    break
                else:
                    print(f"Flight with ID {flight_id} does not exist. Please enter a valid Flight ID.")
            except Exception as e:
                print(f"Error verifying flight ID: {e}")
                return

        # Generate booking date and calculate price based on duration
        booking_date = datetime.today().strftime('%Y-%m-%d')
        self.get_cursor.execute("SELECT duration FROM Flight WHERE flightID = ?", (flight_id,))
        duration_row = self.get_cursor.fetchone()
        duration = duration_row[0]
        price = duration * 30  # Price calculation based on duration

        # Insert ticket into the Ticket table
        try:
            self.get_cursor.execute("""
                INSERT INTO Ticket (user_id, flightID, booking_date, price) 
                VALUES (?, ?, ?, ?)""",
                (user_id, flight_id, booking_date, price)
            )
            self.get_connection.commit()
            ticket_id = self.get_cursor.lastrowid
            print(f"Ticket booked successfully with Ticket ID: {ticket_id}.")

        except Exception as e:
            print(f"Error booking ticket: {e}")

    def view_ticket(self):
        """View ticket details based on Ticket ID."""
        ticket_id = input("Enter your Ticket Number: ")

        try:
            # Retrieve ticket details with passenger and flight information
            self.get_cursor.execute("""
                SELECT 
                    Ticket.ticketNum, 
                    Passenger.title, 
                    Passenger.firstName, 
                    Passenger.lastName, 
                    Flight.airportFrom, 
                    Flight.airportTo, 
                    Flight.departureDate, 
                    Flight.departureTime, 
                    Ticket.booking_date, 
                    Ticket.price
                FROM Ticket
                JOIN Passenger ON Ticket.user_id = Passenger.user_id
                JOIN Flight ON Ticket.flightID = Flight.flightID
                WHERE Ticket.ticketNum = ?
            """, (ticket_id,))

            ticket = self.get_cursor.fetchone()

            if ticket:
                print("\n=== Ticket Details ===")
                print(f"Ticket Number: {ticket[0]}")
                print(f"Passenger: {ticket[1]} {ticket[2]} {ticket[3]}")
                print(f"Flight: From {ticket[4]} to {ticket[5]}")
                print(f"Departure: {ticket[6]} {ticket[7]}")
                print(f"Booking Date: {ticket[8]}")
                print(f"Price: ${ticket[9]:.2f}")
                print("-" * 30)
            else:
                print("No ticket found with the given Ticket Number.")
                
        except Exception as e:
            print(f"Error retrieving ticket details: {e}")

    def update_ticket(self):
        """Update ticket information, specifically for changing the flight associated with the ticket."""
        ticket_id = input("Enter your Ticket Number: ")

        # Verify if the ticket exists
        try:
            self.get_cursor.execute("SELECT ticketNum FROM Ticket WHERE ticketNum = ?", (ticket_id,))
            if not self.get_cursor.fetchone():
                print(f"Ticket with ID {ticket_id} does not exist.")
                return

            print("\n=== Current Ticket Details ===")
            self.get_cursor.execute("""
                SELECT 
                    Ticket.ticketNum, 
                    Passenger.title, 
                    Passenger.firstName, 
                    Passenger.lastName, 
                    Flight.airportFrom, 
                    Flight.airportTo, 
                    Flight.departureDate, 
                    Flight.departureTime, 
                    Ticket.booking_date, 
                    Ticket.price
                FROM Ticket
                JOIN Passenger ON Ticket.user_id = Passenger.user_id
                JOIN Flight ON Ticket.flightID = Flight.flightID
                WHERE Ticket.ticketNum = ?
            """, (ticket_id,))
            ticket = self.get_cursor.fetchone()

            if ticket:
                print(f"Ticket ID: {ticket[0]}")
                print(f"Passenger: {ticket[1]} {ticket[2]} {ticket[3]}")
                print(f"Flight: From {ticket[4]} to {ticket[5]}")
                print(f"Departure: {ticket[6]} {ticket[7]}")
                print(f"Booking Date: {ticket[8]}")
                print(f"Price: ${ticket[9]:.2f}")
                print("-" * 30)
            else:
                print("Ticket details not found.")
                return

            # Display all available flights to choose from
            print("\n=== Available Flights ===")
            self.get_cursor.execute("""
                SELECT flightID, airportFrom, airportTo, departureDate, departureTime 
                FROM Flight
            """)
            flights = self.get_cursor.fetchall()

            if flights:
                for flight in flights:
                    print(f"Flight ID: {flight[0]}, From: {flight[1]} to {flight[2]}, Departure: {flight[3]} {flight[4]}")
                print("-" * 30)
            else:
                print("No available flights at the moment.")
                return

            # Prompt for new flight ID
            new_flight_id = input("Enter the new Flight ID for this ticket: ")

            # Check if the new flight ID is valid
            self.get_cursor.execute("SELECT flightID, duration FROM Flight WHERE flightID = ?", (new_flight_id,))
            flight = self.get_cursor.fetchone()
            if not flight:
                print(f"Flight with ID {new_flight_id} does not exist.")
                return

            # Calculate the new price based on the flight duration
            new_price = flight[1] * 30  # Assuming price is duration multiplied by a rate

            # Update the ticket with the new flight ID and recalculated price
            self.get_cursor.execute("""
                UPDATE Ticket 
                SET flightID = ?, price = ?
                WHERE ticketNum = ?
            """, (new_flight_id, new_price, ticket_id))
            self.get_connection.commit()  # Commit changes

            print(f"Ticket ID {ticket_id} updated successfully to Flight ID {new_flight_id}.")

        except Exception as e:
            print(f"An error occurred while updating the ticket: {e}")

    def cancel_ticket(self):
        """Cancel a ticket by ticket number, with validation and confirmation."""
        ticket_id = input("Enter the Ticket Number to cancel: ")

        # Check if the ticket exists
        try:
            self.get_cursor.execute("SELECT user_id, flightID FROM Ticket WHERE ticketNum = ?", (ticket_id,))
            result = self.get_cursor.fetchone()
            if not result:
                print(f"Ticket with ID {ticket_id} does not exist.")
                return

            user_id, flight_id = result

            # Confirm cancellation
            confirm = input(f"Are you sure you want to cancel Ticket ID {ticket_id}? (yes/no): ").lower()
            if confirm != 'yes':
                print("Cancellation aborted.")
                return

            # Delete the ticket
            self.get_cursor.execute("DELETE FROM Ticket WHERE ticketNum = ?", (ticket_id,))
            self.get_connection.commit()  # Commit the deletion

            print(f"Ticket ID {ticket_id} has been canceled successfully.")

        except Exception as e:
            print(f"An error occurred while canceling the ticket: {e}")



