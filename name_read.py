# The code below creates the Passenger database from the name_list.csv.
# name_list.csv can be updated to include the 20 names minimum for the project

import DBbase as db  # Import the custom DBbase module for database operations
import csv  # Import the csv module for reading CSV files

class Passenger:
    # Define a class to represent a passenger

    def __init__(self, row):
        # Initialize the Passenger object with data from a CSV row
        self.user_id = row[0]
        self.first_name = row[1]  # Set the first name from the first column of the row
        self.last_name = row[2]   # Set the last name from the second column of the row
        self.email = row[3]       # Set the email from the third column of the row

class Passenger_mod(db.DBbase):
    # Define a class that inherits from DBbase for handling CSV operations related to the database

    def reset_or_create_db(self):
        # Method to drop and recreate the Passenger table
        try:
            sql = """
                DROP TABLE IF EXISTS Passenger;  

                CREATE TABLE Passenger (
                    user_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL               
                );
            """
            super().execute_script(sql)  # Execute the SQL script to drop and create the table

        except Exception as e:  # Catch any exceptions that occur
            print(e)  # Print the exception message

    def read_passenger_data(self, file_name):
        # Method to read passenger data from a CSV file
        self.passenger_list = []  # Initialize an empty list to hold Passenger objects

        try:
            with open(file_name, 'r') as record:  # Open the CSV file for reading
                csv_contents = csv.reader(record)  # Create a CSV reader object
                next(record)  # Skip the header row
                for row in csv_contents:  # Iterate over the remaining rows in the CSV
                    # print(row)  # Uncomment to print each row for debugging
                    passenger = Passenger(row)  # Create a Passenger object for each row
                    self.passenger_list.append(passenger)  # Add the Passenger object to the list

        except Exception as e:  # Catch any exceptions that occur
            print(e)  # Print the exception message

    def save_to_database(self):
        # Method to save the passenger data to the database
        print("Number of records to save: ", len(self.passenger_list))  # Print the number of records
        save = input("Continue? (y/n)").lower()  # Prompt the user to confirm saving

        if save == "y":  # If the user confirms
            for item in self.passenger_list:  # Iterate over each Passenger object in the list
                # User to clean data as needed (optional)
                # item.first_name = item.first_name.replace("", "")
                # item.last_name = item.last_name.replace("", "")
                # item.email = item.email.replace("", "")

                try:
                    super().get_cursor.execute("""INSERT INTO Passenger
                    (user_id, first_name, last_name, email)
                        VALUES(?,?,?,?)""",
                         (item.user_id, item.first_name, item.last_name, item.email))  # Insert passenger data into the database
                    super().get_connection.commit()  # Commit the transaction to the database

                    print("Saved item: ", item.first_name, item.last_name, item.email)  # Confirm save

                except Exception as e:  # Catch any exceptions that occur during the insert
                    print(e)  # Print the exception message
            else:
                print("Save to DB aborted")  # If the user doesn't confirm, print a message

# Create an instance of CsvLab with the database filename
passenger = Passenger_mod("PassengerDB.sqlite")
passenger.reset_or_create_db()  # Uncomment to reset or create the database
passenger.read_passenger_data("name_list.csv")  # Read passenger data from the CSV file
passenger.save_to_database()  # Save the passenger data to the database
