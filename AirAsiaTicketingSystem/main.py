from Passenger import Passenger
from Flight import Flight
from Ticket import Ticket
from initialize_db import AirAsiaDatabase

def main_menu():
    """Display the main menu and handle user choices."""
    try:
        while True:
            print("\n=== AirAsia Ticketing System ===")
            print("1. Initialize Database (Reset and Load CSV Data)")
            print("2. Manage Passengers")
            print("3. Manage Flights")
            print("4. Manage Tickets")
            print("5. Exit")

            choice = get_menu_choice(5)
            if choice == 1:
                confirm = input("Warning: This will reset the database. Proceed? (yes/no): ").lower()
                if confirm == "yes":
                    initialize_database()
            elif choice == 2:
                manage_passengers()
            elif choice == 3:
                manage_flights()
            elif choice == 4:
                manage_tickets()
            elif choice == 5:
                print("Exiting system. Goodbye!")
                break
    except KeyboardInterrupt:
        print("\nProgram interrupted. Exiting system. Goodbye!")

def get_menu_choice(max_option):
    """Helper function to validate and return user choice for menus."""
    while True:
        try:
            choice = int(input("Select an option: "))
            if 1 <= choice <= max_option:
                return choice
            print(f"Invalid choice. Please enter a number between 1 and {max_option}.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def initialize_database():
    """Initialize the database, resetting and loading data from CSV files."""
    airasia_db = AirAsiaDatabase()
    airasia_db.reset_database()  # Create/reset the database

    # Load passenger, flight, and ticket data
    airasia_db.read_passenger_data("Passenger_list.csv")
    airasia_db.save_passenger_to_database()
    airasia_db.read_flight_data("flight_list.csv")
    airasia_db.save_flight_to_database()
    airasia_db.read_ticket_data("ticket_list.csv")
    airasia_db.save_ticket_to_database()
    airasia_db.close_db()
    print("Database initialized and data loaded successfully.")

def manage_flights():
    """Manage the flights section with CRUD options."""
    flight_manager = Flight()
    try:
        while True:
            print("\n=== Manage Flights ===")
            print("1. Add a Flight")
            print("2. View All Flights")
            print("3. Update Flight Information")
            print("4. Delete a Flight")
            print("5. Back to Main Menu")

            choice = get_menu_choice(5)
            if choice == 1:
                flight_manager.add_flight()
            elif choice == 2:
                flight_manager.view_flights()
            elif choice == 3:
                flight_manager.update_flight()
            elif choice == 4:
                flight_manager.delete_flight()
            elif choice == 5:
                flight_manager.close_db()
                break
    except KeyboardInterrupt:
        print("\nExiting flights menu.")

def manage_passengers():
    """Manage the passengers section with CRUD options."""
    passenger_manager = Passenger()
    try:
        while True:
            print("\n=== Manage Passengers ===")
            print("1. Add a Passenger")
            print("2. View Passenger")
            print("3. Update Passenger Information")
            print("4. Delete a Passenger")
            print("5. Back to Main Menu")

            choice = get_menu_choice(5)
            if choice == 1:
                passenger_manager.add_passenger()
            elif choice == 2:
                passenger_manager.view_passenger()
            elif choice == 3:
                passenger_manager.update_passenger()
            elif choice == 4:
                passenger_manager.delete_passenger()
            elif choice == 5:
                passenger_manager.close_db()
                break
    except KeyboardInterrupt:
        print("\nExiting passengers menu.")

def manage_tickets():
    """Manage the tickets section with CRUD options."""
    ticket_manager = Ticket()
    try:
        while True:
            print("\n=== Manage Tickets ===")
            print("1. Book a Ticket")
            print("2. View your Ticket")
            print("3. Update Ticket Information")
            print("4. Cancel a Ticket")
            print("5. Back to Main Menu")

            choice = get_menu_choice(5)
            if choice == 1:
                ticket_manager.book_ticket()
            elif choice == 2:
                ticket_manager.view_ticket()
            elif choice == 3:
                ticket_manager.update_ticket()
            elif choice == 4:
                ticket_manager.cancel_ticket()
            elif choice == 5:
                ticket_manager.close_db()
                break
    except KeyboardInterrupt:
        print("\nExiting tickets menu.")

if __name__ == "__main__":
    main_menu()
