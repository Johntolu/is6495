# The code below creates the Passenger database from the Passenger.csv.
# Passenger.csv can be updated to include the 20 names minimum for the project

import DBbase as db  # Import the custom DBbase module for database operations
import csv  # Import the csv module for reading CSV files

class Passenger(db.base):
    # Define a class to represent a passenger

    def __init__(self, row):


        super().__init__("AirAsiaTicketingDB.sqlite")

        self.user_id = row[0]
        self.title = row[1]  # Set the first name from the first column of the row
        self.firstName = row[2]   # Set the last name from the second column of the row
        self.lastName = row[3]
        self.DOB=row[4]
        self.email=row[5]
        self.phone=row[6]
        self.age=row[7]#set the values frm csv file to the passenger object

class PassengerDatabase(db.DBbase):
    # Define a class that inherits from DBbase for handling CSV operations related to the database
    def __init__(self, row):
        # Initialize the User class and connect to the PassengerDB.sqlite database
        super().__init__("AirAsiaTicketingDB.sqlite")
    # def reset_or_create_db(self):
    #     # Method to drop and recreate the Passenger table
    #     try:
    #         sql = """
    #             DROP TABLE IF EXISTS Passenger;
    #
    #             CREATE TABLE Passenger (
    #                 user_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    #                 first_name TEXT NOT NULL,
    #                 last_name TEXT NOT NULL,
    #                 email TEXT UNIQUE NOT NULL
    #             );
    #         """
    #         super().execute_script(sql)  # Execute the SQL script to drop and create the table
    #
    #     except Exception as e:  # Catch any exceptions that occur
    #         print(e)  # Print the exception message

    def read_passenger_data(self, file_name):
        # Method to read passenger data from a CSV file
        self.passenger_list = []  # Initialize an empty list to hold Passenger objects

        try:
            with open(file_name, 'r') as record:  # Open the CSV file for reading
                csv_contents = csv.reader(record)  # Create a CSV reader object
                #next(record)  # Skip the header row
                next(csv_contents)
                for row in csv_contents:  # Iterate over the remaining rows in the CSV
                    # print(row)  # Uncomment to print each row for debugging
                    passenger = Passenger(row)  # Create a Passenger object for each row
                    self.passenger_list.append(passenger)  # Add the Passenger object to the list

        except Exception as e:  # Catch any exceptions that occur
            print(e)  # Print the exception message

    def save_to_database(self):
        # Method to save the passenger data to the database
        # print("Number of records to save: ", len(self.passenger_list))  # Print the number of records
        # save = input("Continue? (y/n)").lower()  # Prompt the user to confirm saving

       # if save == "y":  # If the user confirms
            for item in self.passenger_list:  # Iterate over each Passenger object in the list
                # User to clean data as needed (optional)
                # item.first_name = item.first_name.replace("", "")
                # item.last_name = item.last_name.replace("", "")
                # item.email = item.email.replace("", "")

                try:
                    super().get_cursor.execute("""INSERT INTO Passenger
                    (user_id,title,firstName,lastName,DOB,email,phone,age)
                        VALUES(?,?,?,?)""",
                         (item.user_id,item.title,item.firstName, item.lastName,item.DOB,item.email,item.phone,item.age))  # Insert passenger data into the database
                    super().get_connection.commit()  # Commit the transaction to the database

                    print("Saved item: ", item.firstName, item.lastName, item.email)  # Confirm save
                    super().execute_script("select * from Passenger")
                except Exception as e:  # Catch any exceptions that occur during the insert
                    print(e)  # Print the exception message
            else:
                print("Save to DB aborted")  # If the user doesn't confirm, print a message

# Create an instance of CsvLab with the database filename
# passenger = Passenger_mod("PassengerDB.sqlite")
# passenger.reset_or_create_db()  # Uncomment to reset or create the database


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
