# Ticket.py
from datetime import datetime

import db_base as db

class Ticket(db.DBbase):
    def __init__(self, db_name='AirAsiaTicketingDB.sqlite'):
        super().__init__(db_name)

    def book_ticket(self):

        print("Please enter your details")
        #collecting details of passenger booking ticket and storing in the passenger table
        title = input("Enter Title: ")
        first_name = input("Enter First Name: ")
        last_name = input("Enter Last Name: ")
        dob = input("Enter Date of Birth (YYYY-MM-DD): ")
        email = input("Enter Email: ")
        phone = input("Enter Phone Number: ")
        age = int(input("Enter Age: "))

        try:
            # Insert the passenger details into the Passenger table
            super().get_cursor.execute("""
                    INSERT INTO Passenger (title, firstName, lastName, DOB, email, phone, age) 
                    VALUES (?, ?, ?, ?, ?, ?, ?)""",
                                    (title, first_name, last_name, dob, email, phone, age)
                                    )
            super().get_connection.commit()  # Commit to save passenger details

            # Get the user_id of the newly inserted passenger
            user_id = super().get_cursor.lastrowid

        except Exception as e:
            print(f"Error saving passenger details: {e}")
            return


       #Displaying flight details for the passenger to select according to their choice
        try:
            print("\n=== Available Flights ===")
            super().get_cursor.execute("""
                    SELECT flightID, airportFrom, airportTo, departureDate, departureTime 
                    FROM Flight
                """)
            flights = super().get_cursor.fetchall()

            if flights:
                for flight in flights:
                    print(
                        f"Flight ID: {flight[0]}, From: {flight[1]} To: {flight[2]}, Departure: {flight[3]} {flight[4]}")
                print("-" * 30)
            else:
                print("No available flights at the moment.")
                return
        except Exception as e:
            print(f"Error retrieving flights: {e}")
            return



    # Step 2: Ask the user to select a flight
        flight_id = input("Enter the Flight ID you want to book a ticket for: ")

        # Verify the flight ID exists
        try:
            super().get_cursor.execute("SELECT flightID FROM Flight WHERE flightID = ?", (flight_id,))
            if not super().get_cursor.fetchone():
                print(f"Flight with ID {flight_id} does not exist.")
                return
        except Exception as e:
            print(f"Error verifying flight ID: {e}")
            return

        # Step 4: Automatically generate booking date and calculate price
        booking_date = datetime.today().strftime('%Y-%m-%d')  # Use today's date
        super().get_cursor.execute("""SELECT duration FROM Flight WHERE flightID = ?""", (flight_id,))
        duration_row = super().get_cursor.fetchone()
          # Calculate price based on duration
        duration=duration_row[0]
        price=duration*30

        try:
            # Insert ticket into the Ticket table
            super().get_cursor.execute("""
                INSERT INTO Ticket (user_id, flightID, booking_date, price) 
                VALUES (?, ?, ?, ?)""",
                                    (user_id, flight_id, booking_date, price)
                                    )
            super().get_connection.commit()  # Commit to save the ticket booking

            # Get the ticket number (ID) of the newly booked ticket
            ticket_id = super().get_cursor.lastrowid

        except Exception as e:
            print(f"Error booking ticket: {e}")
            return


        # Step 5: Display ticket with flight and passenger details
        try:
            # Fetch flight details
            super().get_cursor.execute("""
                SELECT airportFrom, airportTo, departureDate, departureTime 
                FROM Flight WHERE flightID = ?""", (flight_id,))
            flight_details = super().get_cursor.fetchone()


            if flight_details:
                print("\n=== Ticket Booked Successfully ===")
                print(f"Ticket ID: {ticket_id}")
                print(f"Passenger: {title} {first_name} {last_name}")
                print(f"Flight: From {flight_details[0]} To {flight_details[1]}")
                print(f"  Departure: {flight_details[2]} {flight_details[3]}")
                print(f"  Booking Date: {booking_date}")
                print(f"  Price: ${price}")
                print("-" * 30)
            else:
                print("Error: Flight details not found.")
        except Exception as e:
            print(f"Error displaying ticket details: {e}")




        # user_id = input("Enter user ID: ")
        # flight_id = input("Enter flight ID: ")
        # booking_date = input("Enter booking date (YYYY-MM-DD): ")
        # price = float(input("Enter price: "))
        #
        # try:
        #     self.get_cursor.execute("""
        #         INSERT INTO Ticket (user_id, flightID, booking_date, price)
        #         VALUES (?, ?, ?, ?)""",
        #         (user_id, flight_id, booking_date, price)
        #     )
        #     self.get_connection.commit()  # Commit the transaction
        #     print("Ticket booked successfully.")
        # except Exception as e:
        #     print(f"An error booking ticket occurred: {e}")

    def view_tickets(self):
        try:
            self.get_cursor.execute("SELECT * FROM Ticket")
            tickets = self.get_cursor.fetchall()
            for ticket in tickets:
                print(f"Ticket ID: {ticket[0]}, User ID: {ticket[1]}, Flight ID: {ticket[2]}")
        except Exception as e:
            print(f"Error retrieving tickets: {e}")

    def update_ticket(self, ticket_id):
        # Implement update logic here
        pass

    def cancel_ticket(self, ticket_id):
        # Implement delete logic here
        pass

