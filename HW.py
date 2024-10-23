from collections import namedtuple  # Importing namedtuple for creating tuple-like data structures (not used in the current code).
import sqlite3  # Importing sqlite3 module to manage SQLite database connections and operations.
import DBbase as db  # Importing a custom database base class to handle SQLite connections.

# Class to manage users in the database
class User(db.DBbase):
    def __init__(self):
        # Initialize the User class and connect to the PassengerDB.sqlite database
        super().__init__("PassengerDB.sqlite")

    def add_user(self, first_name, last_name, email):
        try:
            # Insert a new user into the Passenger table
            super().get_cursor.execute(
                "INSERT INTO Passenger (first_name, last_name, email) VALUES (?, ?, ?);",
                (first_name, last_name, email)  # Use placeholders to avoid SQL injection
            )
            super().get_connection.commit()  # Commit the transaction to save changes
            print(f"Added passenger {first_name} {last_name} successfully.")  # Success message
        except Exception as e:
            # Print any errors that occur during the insertion
            print("An error adding passenger occurred:", e)

    def fetch_user(self, user_id=None, email=None):
        try:
            # Fetch a user based on user_id or email
            if user_id is not None:
                return super().get_cursor.execute("SELECT * FROM Passenger WHERE user_id = ?;", (user_id,)).fetchone()  # Fetch one user by ID
            elif email is not None:
                return super().get_cursor.execute("SELECT * FROM Passenger WHERE email = ?;", (email,)).fetchone()  # Fetch one user by email
            else:
                return super().get_cursor.execute("SELECT * FROM Passenger;").fetchall()  # Fetch all users if no criteria is given
        except Exception as e:
            # Print any errors that occur during the fetching
            print("An error fetching passenger occurred:", e)

    def delete_user(self, user_id):
        try:
            # Delete a user from the Passenger table based on user_id
            super().get_cursor.execute("DELETE FROM Passenger WHERE user_id = ?;", (user_id,))
            super().get_connection.commit()  # Commit the transaction
            print(f"Deleted passenger ID {user_id} successfully.")  # Success message
        except Exception as e:
            # Print any errors that occur during the deletion
            print("An error deleting passenger occurred:", e)

    def reset_database(self):
        try:
            # Reset the Passenger table by dropping it and recreating it
            sql = """
                DROP TABLE IF EXISTS Passenger;  -- Drop the table if it exists
                CREATE TABLE Passenger (           -- Create a new Passenger table
                    user_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,  -- Auto-incrementing user ID
                    first_name TEXT NOT NULL,  -- First name of the passenger
                    last_name TEXT NOT NULL,   -- Last name of the passenger
                    email TEXT UNIQUE NOT NULL  -- Unique email for the passenger
                );
            """
            super().execute_script(sql)  # Execute the SQL script
            print("Users table successfully created.")  # Success message
        except Exception as e:
            # Print any errors that occur during the reset
            print("An error resetting user occurred:", e)

# Class to manage tickets in the database
class Ticket(db.DBbase):
    def __init__(self):
        # Initialize the Ticket class and connect to the ticketDB.sqlite database
        super().__init__("ticketDB.sqlite")

    def update(self, flight_id, user_id):
        try:
            # Update the ticket record for a specific user
            super().get_cursor.execute("UPDATE Ticket SET flight_id = ? WHERE user_id = ?;", (flight_id, user_id))
            super().get_connection.commit()  # Commit the transaction
            print(f"Updated record for user ID {user_id} successfully.")  # Success message
        except Exception as e:
            # Print any errors that occur during the update
            print("An error updating occurred:", e)

    def add(self, user_id, flight_id):
        if self.user_exists(user_id):  # Check if the user exists before adding a ticket
            try:
                # Add a new ticket for the user
                super().get_cursor.execute("INSERT OR IGNORE INTO Ticket (user_id, flight_id) VALUES (?, ?);", (user_id, flight_id))
                super().get_connection.commit()  # Commit the transaction
                print(f"Added ticket for user ID {user_id} successfully.")  # Success message
            except Exception as e:
                # Print any errors that occur during the addition
                print("An error adding occurred:", e)
        else:
            print(f"User ID {user_id} does not exist.")  # Message if the user does not exist

    def user_exists(self, user_id):
        # Check if a user exists in the Passenger table
        return super().get_cursor.execute("SELECT 1 FROM Passenger WHERE user_id = ?;", (user_id,)).fetchone() is not None

    def delete(self, user_id):
        try:
            # Delete a ticket for a specific user
            super().get_cursor.execute("DELETE FROM Ticket WHERE user_id = ?;", (user_id,))
            super().get_connection.commit()  # Commit the transaction
            print(f"Deleted ticket for user ID {user_id} successfully.")  # Success message
            return True
        except Exception as e:
            # Print any errors that occur during the deletion
            print("An error deleting occurred:", e)
            return False

    def fetch(self, flight_id=None, user_id=None):
        try:
            # Fetch ticket records based on flight_id or user_id
            if flight_id is not None:
                return super().get_cursor.execute("SELECT * FROM Ticket WHERE flight_id = ?", (flight_id,)).fetchone()  # Fetch ticket by flight ID
            elif user_id is not None:
                return super().get_cursor.execute("SELECT * FROM Ticket WHERE user_id = ?", (user_id,)).fetchone()  # Fetch ticket by user ID
            else:
                return super().get_cursor.execute("SELECT * FROM Ticket").fetchall()  # Fetch all tickets if no criteria is given
        except Exception as e:
            # Print any errors that occur during the fetching
            print("An error fetching occurred:", e)

    def reset_database(self):
        try:
            # Reset the Ticket table by dropping it and recreating it
            sql = """
                DROP TABLE IF EXISTS Ticket;  -- Drop the table if it exists
                CREATE TABLE Ticket (           -- Create a new Ticket table
                    ticket_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,  -- Auto-incrementing ticket ID
                    user_id INTEGER NOT NULL,  -- User ID associated with the ticket
                    flight_id INTEGER NOT NULL,  -- Flight ID associated with the ticket
                    FOREIGN KEY (user_id) REFERENCES Passenger(user_id),  -- Foreign key constraint to Passenger
                    FOREIGN KEY (flight_id) REFERENCES Flight(flight_id)   -- Foreign key constraint to Flight
                );
            """
            super().execute_script(sql)  # Execute the SQL script
            print("Ticket table successfully created.")  # Success message
        except Exception as e:
            # Print any errors that occur during the reset
            print("An error resetting occurred:", e)

# Class to manage flights in the database
class Flight(db.DBbase):
    def __init__(self):
        # Initialize the Flight class and connect to the FlightDB.sqlite database
        super().__init__("FlightDB.sqlite")

    def add_flight(self, flight_id, airport_to, departure_date, departure_gate, arrival_gate, price):
        try:
            # Insert a new flight record
            super().get_cursor.execute(
                """INSERT INTO Flight (flight_id, airport_to, departure_date, departure_gate, arrival_gate, price) 
                VALUES (?, ?, ?, ?, ?, ?);""",
                (flight_id, airport_to, departure_date, departure_gate, arrival_gate, price)  # Use placeholders for values
            )
            super().get_connection.commit()  # Commit the transaction
            print(f"Flight ID: {flight_id} added successfully.")  # Success message
        except Exception as ex:
            # Print any errors that occur during the addition
            print("An error occurred in the flight class:", ex)

    def update_flight(self, flight_id, airport_to, departure_date, departure_gate, arrival_gate, price):
        try:
            # Update flight record with new details
            super().get_cursor.execute(
                """UPDATE Flight SET airport_to = ?, departure_date = ?, departure_gate = ?, 
                arrival_gate = ?, price = ? WHERE flight_id = ?;""",
                (airport_to, departure_date, departure_gate, arrival_gate, price, flight_id)  # Use placeholders for values
            )
            super().get_connection.commit()  # Commit the transaction
            print("Updated flight ID record successfully.")  # Success message
            return True
        except Exception as e:
            # Print any errors that occur during the update
            print("An error updating inventory occurred:", e)
            return False

    def delete_flight(self, flight_id):
        try:
            # Delete a flight record by flight ID
            super().get_cursor.execute("DELETE FROM Flight WHERE flight_id = ?;", (flight_id,))
            super().get_connection.commit()  # Commit the transaction
            print(f"Deleted flight ID {flight_id} successfully.")  # Success message
        except Exception as e:
            # Print any errors that occur during the deletion
            print("An error occurred in flight delete:", e)

    def fetch_flight(self, flight_id=None):
        try:
            # Fetch flight records based on flight_id
            if flight_id is not None:
                return super().get_cursor.execute("SELECT * FROM Flight WHERE flight_id = ?;", (flight_id,)).fetchone()  # Fetch flight by ID
            else:
                return super().get_cursor.execute("SELECT * FROM Flight;").fetchall()  # Fetch all flights if no ID is specified
        except Exception as e:
            # Print any errors that occur during the fetching
            print("An error fetching flights occurred:", e)

    def reset_database(self):
        try:
            # Reset the Flight table by dropping it and recreating it
            sql = """
                DROP TABLE IF EXISTS Flight;  -- Drop the table if it exists
                CREATE TABLE Flight (           -- Create a new Flight table
                    flight_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,  -- Auto-incrementing flight ID
                    airport_to TEXT NOT NULL,  -- Destination airport
                    departure_date TEXT NOT NULL,  -- Departure date
                    departure_gate TEXT NOT NULL,  -- Departure gate
                    arrival_gate TEXT NOT NULL,  -- Arrival gate
                    price INTEGER NOT NULL  -- Price of the flight
                );
            """
            super().execute_script(sql)  # Execute the SQL script
            print("Flight table successfully created.")  # Success message
        except Exception as e:
            # Print any errors that occur during the reset
            print("An error resetting flight occurred:", e)

# Class to run the project and manage user interactions
class Project:
    def __init__(self):
        self.flight = Flight()  # Create an instance of the Flight class
        self.ticket = Ticket()  # Create an instance of the Ticket class
        self.user = User()  # Create an instance of the User class

    def run(self):
        # Define available options for user interactions
        flight_options = {
            "get": "Get all flights",
            "getby": "Get flight by user ID",
            "update": "Update flights",
            "add": "Add flights",
            "delete": "Delete flights",
            "reset": "Reset database",
            "exit": "Exit program"
        }

        print("Welcome to the flight selection program, please choose a selection")  # Welcome message

        user_selection = ""  # Initialize user selection

        while user_selection != "exit":  # Loop until the user chooses to exit
            print("*** Option list ***")  # Print options header
            for option in flight_options.items():  # Iterate over flight options
                print(f"{option[0]}: {option[1]}")  # Print each option

            user_selection = input("Select an option: ").lower()  # Get user input in lowercase

            if user_selection == "get":
                results = self.flight.fetch_flight()  # Fetch all flights
                if results:
                    for item in results:
                        # Print flight details
                        print(f"Flight ID: {item[0]}, Airport To: {item[1]}, "
                              f"Departure Date: {item[2]}, Departure Gate: {item[3]}, "
                              f"Arrival Gate: {item[4]}, Price: {item[5]}")
                else:
                    print("No flights available.")  # Message if no flights exist

            elif user_selection == "getby":
                flight_id = input("Enter flight ID: ")  # Prompt for flight ID
                result = self.flight.fetch_flight(flight_id)  # Fetch flight by ID
                print(result)  # Print the result
                input("Press return to continue ")  # Wait for user input

            elif user_selection == "update":
                # Prompt for flight details to update
                flight_id = input("Flight ID: ")
                airport_to = input("Enter airport to: ")
                departure_date = input("Enter departure date: ")
                departure_gate = input("Enter departure gate: ")
                arrival_gate = input("Enter arrival gate: ")
                price = input("Enter cost in $: ")
                self.flight.update_flight(flight_id, airport_to, departure_date, departure_gate, arrival_gate, price)  # Update flight
                input("Press return to continue ")  # Wait for user input

            elif user_selection == "add":
                # Prompt for flight details to add
                flight_id = input("Flight ID: ")
                airport_to = input("Enter airport to: ")
                departure_date = input("Enter departure date: ")
                departure_gate = input("Enter departure gate: ")
                arrival_gate = input("Enter arrival gate: ")
                price = input("Enter cost in $: ")
                self.flight.add_flight(flight_id, airport_to, departure_date, departure_gate, arrival_gate, price)  # Add flight
                print("Done\n")  # Success message
                input("Press return to continue ")  # Wait for user input

            elif user_selection == "delete":
                flight_id = input("Enter flight ID: ")  # Prompt for flight ID to delete
                self.flight.delete_flight(flight_id)  # Delete flight by ID
                print("Done\n")  # Success message
                input("Press return to continue ")  # Wait for user input

            elif user_selection == "reset":
                # Prompt for confirmation before resetting database
                confirm = input("This will delete all records in flights, tickets, and users, continue? (y/n) ").lower()
                if confirm == "y":
                    self.flight.reset_database()  # Reset flight database
                    self.ticket.reset_database()  # Reset ticket database
                    self.user.reset_database()  # Reset user database
                    print("Reset complete")  # Success message
                    input("Press return to continue ")  # Wait for user input
                else:
                    print("Reset aborted")  # Message if reset is aborted

            else:
                if user_selection != "exit":
                    print("Invalid selection, please try again\n")  # Message for invalid option

# Main entry point of the program
if __name__ == "__main__":
    project = Project()  # Create a new Project instance
    project.run()  # Run the project
