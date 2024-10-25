

# Import the db_base  module for database operations

import db_base as db
class Passenger(db.DBbase):

    # Define a class to represent a passenger
    def __init__(self, db_name='AirAsiaTicketingDB.sqlite'):
            super().__init__(db_name)


    def add_passenger(self):
        title = input("Enter Title: ")
        first_name = input("Enter First Name: ")
        last_name = input("Enter Last Name: ")
        dob = input("Enter Date of Birth (YYYY-MM-DD): ")
        email = input("Enter Email: ")
        phone = input("Enter Phone Number: ")
        age = int(input("Enter Age: "))
        try:

            super().get_cursor.execute("""
                INSERT INTO Passenger (title, firstName, lastName, DOB, email, phone, age) VALUES (?, ?, ?,?,?,?,?)""", # Use placeholders to avoid SQL injection
                                       (title, first_name, last_name, dob, email, phone, age)
            )
            super().get_connection.commit()  # Commit the transaction to save changes
            print(f"Added passenger {first_name} {last_name} successfully.")  # Success message
        except Exception as e:
            # Print any errors that occur during the insertion
            print("An error adding passenger occurred:", e)

    def update_passenger(self):

        user_id=input("Enter the user_id of the passenger whose details you want to update")
        #Update user information for a specific user ID.
        print(f"Updating passenger details for user ID: {user_id}")

        # Choose the field to update
        field = input(
            "Enter the field to update (title,firstName,lastName,DOB,email,phone,age): ")
        new_value = input(f"Enter the new value for {field}: ")

        try:
            sql = f"UPDATE Passenger SET {field} = ? WHERE user_id = ?"
            super().get_cursor.execute(sql, (new_value, user_id))
            super().get_connection.commit()  # Commit the changes
            print(f"User ID {user_id} updated successfully.")
        except Exception as e:
            print(f"Error updating flight ID {user_id}: {e}")



    def view_passenger(self):
        print("To view, enter either user ID or email, and leave the other blank!")
        user_id = input("Enter user ID (leave blank if unknown): ")
        email = input("Enter email (leave blank if unknown): ")

        try:
            # Fetch a user based on user_id or email
            if user_id:  # If user_id is provided
                passenger = super().get_cursor.execute("SELECT * FROM Passenger WHERE user_id = ?;",
                                                       (user_id,)).fetchone()
            elif email:  # If email is provided
                passenger = super().get_cursor.execute("SELECT * FROM Passenger WHERE email = ?;", (email,)).fetchone()
            else:
                print("Please provide either a user ID or an email.")
                return None

            if passenger:
                print(
                    f"Passenger ID: {passenger[0]}, Name: {passenger[2]} {passenger[3]}, Email: {passenger[4]}, Phone: {passenger[5]}, Age: {passenger[6]}")
                return passenger
            else:
                print("No passenger found with the given information.")
                return None

        except Exception as e:
            print("An error fetching passenger occurred:", e)

    def delete_passenger(self):
        """Delete a passenger from the database based on Passenger ID."""
        passenger_id = input("Enter the Passenger ID to delete: ")
        confirm = input(f"Are you sure you want to delete Passenger ID {passenger_id}? (yes/no): ")

        if confirm.lower() == 'yes':
            try:
                super().get_cursor.execute("DELETE FROM Passenger WHERE user_id = ?", (passenger_id,))
                super().get_connection.commit()  # Commit the transaction
                print(f"Passenger ID {passenger_id} deleted successfully.")
            except Exception as e:
                print(f"Error deleting passenger ID {passenger_id}: {e}")
        else:
            print("Deletion cancelled.")









    # def reset_database(self):
    #     try:
    #         # Reset the Passenger table by dropping it and recreating it
    #         sql = """
    #             DROP TABLE IF EXISTS Passenger;  -- Drop the table if it exists
    #             CREATE TABLE Passenger (           -- Create a new Passenger table
    #                 user_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,  -- Auto-incrementing user ID
    #                 first_name TEXT NOT NULL,  -- First name of the passenger
    #                 last_name TEXT NOT NULL,   -- Last name of the passenger
    #                 email TEXT UNIQUE NOT NULL  -- Unique email for the passenger
    #             );
    #         """
    #         super().execute_script(sql)  # Execute the SQL script
    #         print("Users table successfully created.")  # Success message
    #     except Exception as e:
    #         # Print any errors that occur during the reset
    #         print("An error resetting user occurred:", e)
















 # self.user_id = row[0]
#         self.title = row[1]  # Set the first name from the first column of the row
#         self.firstName = row[2]   # Set the last name from the second column of the row
#         self.lastName = row[3]
#         self.DOB=row[4]
#         self.email=row[5]
#         self.phone=row[6]
#         self.age=row[7]#set the values frm csv file to the passenger object
#
# # r_create_db()  # Uncomment to reset or create the database


# class PassengerDatabase(db.DBbase):
#     # Define a class that inherits from DBbase for handling CSV operations related to the database
#     def __init__(self, row):
#         # Initialize the User class and connect to the PassengerDB.sqlite database
#         super().__init__("AirAsiaTicketingDB.sqlite")
#     # def reset_or_create_db(self):
#     #     # Method to drop and recreate the Passenger table
#     #     try:
#     #         sql = """
#     #             DROP TABLE IF EXISTS Passenger;
#     #
#     #             CREATE TABLE Passenger (
#     #                 user_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
#     #                 first_name TEXT NOT NULL,
#     #                 last_name TEXT NOT NULL,
#     #                 email TEXT UNIQUE NOT NULL
#     #             );
#     #         """
#     #         super().execute_script(sql)  # Execute the SQL script to drop and create the table
#     #
#     #     except Exception as e:  # Catch any exceptions that occur
#     #         print(e)  # Print the exception message
#
#     def read_passenger_data(self, file_name):
#         # Method to read passenger data from a CSV file
#         self.passenger_list = []  # Initialize an empty list to hold Passenger objects
#
#         try:
#             with open(file_name, 'r') as record:  # Open the CSV file for reading
#                 csv_contents = csv.reader(record)  # Create a CSV reader object
#                 #next(record)  # Skip the header row
#                 next(csv_contents)
#                 for row in csv_contents:  # Iterate over the remaining rows in the CSV
#                     # print(row)  # Uncomment to print each row for debugging
#                     passenger = Passenger(row)  # Create a Passenger object for each row
#                     self.passenger_list.append(passenger)  # Add the Passenger object to the list
#
#         except Exception as e:  # Catch any exceptions that occur
#             print(e)  # Print the exception message
#
#     def save_to_database(self):
#         # Method to save the passenger data to the database
#         # print("Number of records to save: ", len(self.passenger_list))  # Print the number of records
#         # save = input("Continue? (y/n)").lower()  # Prompt the user to confirm saving
#
#        # if save == "y":  # If the user confirms
#             for item in self.passenger_list:  # Iterate over each Passenger object in the list
#                 # User to clean data as needed (optional)
#                 # item.first_name = item.first_name.replace("", "")
#                 # item.last_name = item.last_name.replace("", "")
#                 # item.email = item.email.replace("", "")
#
#                 try:
#                     super().get_cursor.execute("""INSERT INTO Passenger
#                     (user_id,title,firstName,lastName,DOB,email,phone,age)
#                         VALUES(?,?,?,?)""",
#                          (item.user_id,item.title,item.firstName, item.lastName,item.DOB,item.email,item.phone,item.age))  # Insert passenger data into the database
#                     super().get_connection.commit()  # Commit the transaction to the database
#
#                     print("Saved item: ", item.firstName, item.lastName, item.email)  # Confirm save
#                     super().execute_script("select * from Passenger")
#                 except Exception as e:  # Catch any exceptions that occur during the insert
#                     print(e)  # Print the exception message
#             else:
#                 print("Save to DB aborted")  # If the user doesn't confirm, print a message
#
# # Create an instance of CsvLab with the database filename
# # passenger = Passenger_mod("PassengerDB.sqlite")
# # passenger.reset_o