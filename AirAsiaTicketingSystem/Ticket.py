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
                print(f"Ticket Num: {ticket_id}")
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





    def view_ticket(self):
        ticket_id=input("Enter your ticket Number")

        try:
            # Retrieve ticket details with passenger and flight information
            super().get_cursor.execute("""
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

            tickets = super().get_cursor.fetchall()

            if tickets:
                for ticket in tickets:
                    print(f"Ticket Num: {ticket[0]}")
                    print(f"Passenger: {ticket[1]} {ticket[2]} {ticket[3]}")
                    print(f"Flight: From {ticket[4]} To {ticket[5]}")
                    print(f"  Departure: {ticket[6]} {ticket[7]}")
                    print(f"  Booking Date: {ticket[8]}")
                    print(f"  Price: ${ticket[9]}")
                    print("-" * 30)
            else:
                print("No tickets found.")
        except Exception as e:
            print(f"Error retrieving tickets: {e}")

    def update_ticket(self):
        try:
            ticket_id=input("Enter your Ticket Number")
            # Check if the ticket exists
            super().get_cursor.execute("SELECT ticketNum FROM Ticket WHERE ticketNum = ?", (ticket_id,))
            if not self.get_cursor.fetchone():
                print(f"Ticket with ID {ticket_id} does not exist.")
                return

            # Display current ticket details
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

            print("=== Current Ticket Details ===")
            print(f"Ticket ID: {ticket[0]}")
            print(f"Passenger: {ticket[1]} {ticket[2]} {ticket[3]}")
            print(f"Flight: From {ticket[4]} To {ticket[5]}")
            print(f"  Departure: {ticket[6]} {ticket[7]}")
            print(f"  Booking Date: {ticket[8]}")
            print(f"  Price: ${ticket[9]}")
            print("-" * 30)

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

            # Options to update flight or booking date
            new_flight_id= input("Enter the flight_id of the Flight you want to update to :  ")




            # Verify new flight ID
            self.get_cursor.execute("SELECT flightID, duration FROM Flight WHERE flightID = ?", (new_flight_id,))
            flight = self.get_cursor.fetchone()

            if not flight:
                print("Invalid flight ID.")
                return

            # Update ticket with new flight ID and recalculate price based on duration
            new_price = flight[1] * 30
            self.get_cursor.execute("""
                UPDATE Ticket 
                SET flightID = ?, price = ?
                WHERE ticketNum = ?
            """, (new_flight_id, new_price, ticket_id))



            self.get_connection.commit()
            print("Ticket updated successfully.")

        except Exception as e:
            print(f"Error updating ticket: {e}")


    def cancel_ticket(self):
        ticket_id = input("Enter your Ticket Number")
        try:
            # Check if the ticket exists and retrieve the associated user_id
            super().get_cursor.execute("SELECT user_id FROM Ticket WHERE ticketNum = ?", (ticket_id,))
            result = super().get_cursor.fetchone()
            if not result:
                print(f"Ticket with ID {ticket_id} does not exist.")
                return

            user_id = result[0]

            # Confirm cancellation
            confirm = input(
                f"Are you sure you want to cancel ticket Num {ticket_id} and delete the associated passenger? (yes/no): ").lower()
            if confirm != 'yes':
                print("Cancellation aborted.")
                return

            # Delete the ticket
            super().get_cursor.execute("DELETE FROM Ticket WHERE ticketNum = ?", (ticket_id,))
            super().get_connection.commit()

            # Delete the associated passenger
            super().get_cursor.execute("DELETE FROM Passenger WHERE user_id = ?", (user_id,))
            super().get_connection.commit()

            print(f"Ticket Number {ticket_id} and the associated passenger record have been canceled successfully.")

        except Exception as e:
            print(f"Error canceling ticket: {e}")


