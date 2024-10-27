import db_base as db
import re  # For regular expression validation
from datetime import datetime

class Passenger(db.DBbase):
    valid_titles = {"Mr.", "Ms.", "Mrs.", "Miss", "Dr."}  # Define valid titles

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
        return bool(re.match(r"^\d{3}-\d{3}-\d{4}$", phone))

    def validate_email(self, email):
        """Check if the email format is valid."""
        return bool(re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email))

    def validate_age(self, age):
        """Ensure age is a positive integer."""
        return age.isdigit() and int(age) > 0

    def email_exists(self, email):
        """Check if the email already exists in the database."""
        try:
            self.get_cursor.execute("SELECT email FROM Passenger WHERE email = ?", (email,))
            return self.get_cursor.fetchone() is not None
        except Exception as e:
            print(f"Error checking email existence: {e}")
            return False

    def add_passenger(self):
        """Add a new passenger with validation for fields."""
        while True:
            title = input("Enter Title: ")
            if title not in self.valid_titles:
                print("Error: Invalid title. Valid options are: Mr., Ms., Mrs., Miss, Dr.")
            else:
                break

        first_name = input("Enter First Name: ")
        last_name = input("Enter Last Name: ")

        while True:
            dob = input("Enter Date of Birth (YYYY-MM-DD): ")
            if self.validate_date(dob):
                break
            print("Error: Invalid date format. Please use YYYY-MM-DD.")

        while True:
            email = input("Enter Email: ")
            if not self.validate_email(email):
                print("Error: Invalid email format. Please enter a valid email.")
            elif self.email_exists(email):
                print("Error: Email already exists in the system.")
            else:
                break

        while True:
            phone = input("Enter Phone Number: ")
            if self.validate_phone(phone):
                break
            print("Error: Invalid phone number format. Please use xxx-xxx-xxxx.")

        while True:
            age = input("Enter Age: ")
            if self.validate_age(age):
                age = int(age)  # Convert age to an integer once validated
                break
            print("Error: Age must be a positive integer.")

        try:
            self.get_cursor.execute("""
                INSERT INTO Passenger (title, firstName, lastName, DOB, email, phone, age)
                VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (title, first_name, last_name, dob, email, phone, age)
            )
            self.get_connection.commit()  # Commit the transaction
            user_id = self.get_cursor.lastrowid  # Retrieve the newly assigned user_id
            print(f"Added passenger {first_name} {last_name} successfully with User ID: {user_id}")
        except Exception as e:
            print("An error occurred while adding the passenger:", e)

    def update_passenger(self):
        """Update passenger information for a specific user ID."""
        user_id = input("Enter the user ID of the passenger to update: ")
        print(f"Updating passenger details for user ID: {user_id}")

        field = input(
            "Enter the field to update (title, firstName, lastName, DOB, email, phone, age): "
        )
        new_value = input(f"Enter the new value for {field}: ")

        if field == "title":
            if new_value not in self.valid_titles:
                print("Error: Invalid title. Valid options are: Mr., Ms., Mrs., Miss, Dr.")
                return
        elif field == "DOB":
            if not self.validate_date(new_value):
                print("Error: Invalid date format. Please use YYYY-MM-DD.")
                return
        elif field == "phone":
            if not self.validate_phone(new_value):
                print("Error: Invalid phone number format. Please use xxx-xxx-xxxx.")
                return
        elif field == "email":
            if not self.validate_email(new_value):
                print("Error: Invalid email format.")
                return
            if self.email_exists(new_value):
                print("Error: Email already exists in the system.")
                return
        elif field == "age":
            if not self.validate_age(new_value):
                print("Error: Age must be a positive integer.")
                return

        try:
            sql = f"UPDATE Passenger SET {field} = ? WHERE user_id = ?"
            self.get_cursor.execute(sql, (new_value, user_id))
            self.get_connection.commit()  # Commit the transaction
            print(f"User ID {user_id} updated successfully.")
        except Exception as e:
            print(f"Error updating passenger ID {user_id}: {e}")

    def view_passenger(self):
        """View passenger details based on user ID or email."""
        print("To view, enter either user ID or email, and leave the other blank.")
        user_id = input("Enter user ID (leave blank if unknown): ")
        email = input("Enter email (leave blank if unknown): ")

        try:
            if user_id:
                passenger = self.get_cursor.execute(
                    "SELECT user_id, title, firstName, lastName, DOB, email, phone, age FROM Passenger WHERE user_id = ?;",
                    (user_id,)
                ).fetchone()
            elif email:
                passenger = self.get_cursor.execute(
                    "SELECT user_id, title, firstName, lastName, DOB, email, phone, age FROM Passenger WHERE email = ?;",
                    (email,)
                ).fetchone()
            else:
                print("Error: Please provide either a user ID or an email.")
                return

            if passenger:
                print(
                    f"Passenger ID: {passenger[0]}, Title: {passenger[1]}, Name: {passenger[2]} {passenger[3]}, "
                    f"DOB: {passenger[4]}, Email: {passenger[5]}, Phone: {passenger[6]}, Age: {passenger[7]}"
                )
            else:
                print("No passenger found with the given information.")
        except Exception as e:
            print("An error occurred while fetching the passenger:", e)

    def delete_passenger(self):
        """Delete a passenger based on user ID."""
        passenger_id = input("Enter the Passenger ID to delete: ")
        confirm = input(f"Are you sure you want to delete Passenger ID {passenger_id}? (yes/no): ").lower()

        if confirm == 'yes':
            try:
                self.get_cursor.execute("DELETE FROM Passenger WHERE user_id = ?", (passenger_id,))
                self.get_connection.commit()
                print(f"Passenger ID {passenger_id} deleted successfully.")
            except Exception as e:
                print(f"Error deleting passenger ID {passenger_id}: {e}")
        else:
            print("Deletion cancelled.")
