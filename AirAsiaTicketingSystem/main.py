
from Passenger import Passenger
from Flight import Flight
from Ticket import Ticket


def main_menu():
    while True:
        print("\n=== AirAsia Ticketing System ===")
        print("1. Manage Passengers")
        print("2. Manage Flights")
        print("3. Manage Tickets")
        print("4. Exit")

        choice = input("Select an option: ")

        if choice == '1':
            manage_passengers()

        elif choice == '2':
            manage_flights()
        elif choice == '3':
            manage_tickets()
        elif choice == '4':
            print("Exiting system. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


def manage_flights():
    flight_manager = Flight()

    while True:
        print("\n=== Manage Flights ===")
        print("1. Add a Flight")
        print("2. View All Flights")
        print("3. Update Flight Information")
        print("4. Delete a Flight")
        print("5. Back to Main Menu")

        choice = input("Select an option: ")

        if choice == '1':
            # Call the function to add a flight
            flight_manager.add_flight()
        elif choice == '2':
            # Call the function to view all flights
            flight_manager.view_flights()
        elif choice == '3':
            # Call the function to update a flight
            flight_manager.update_flight()
        elif choice == '4':
            # Call the function to delete a flight
            flight_manager.delete_flight()
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")


def manage_passengers():
    passenger_manager = Passenger()  # Instantiate the Passenger class
    while True:
        print("\n=== Manage Passengers ===")
        print("1. Add a Passenger")
        print("2. View Passenger")
        print("3. Update Passenger Information")
        print("4. Delete a Passenger")
        print("5. Back to Main Menu")

        choice = input("Select an option: ")

        if choice == '1':
            passenger_manager.add_passenger()  # Call add_passenger method
        elif choice == '2':
            passenger_manager.view_passenger()  # Call view_passengers method
        elif choice == '3':
            passenger_manager.update_passenger()  # Call update_passenger method
        elif choice == '4':
            passenger_manager.delete_passenger()  # Call delete_passenger method
        elif choice == '5':
            passenger_manager.close_db()  # Close DB connection before returning
            break  # Exit back to main menu
        else:
            print("Invalid choice. Please try again.")


def manage_tickets():
    ticket_manager=Ticket()
    while True:
        print("\n=== Manage Tickets ===")
        print("1. Book a Ticket")
        print("2. View  your Ticket")
        print("3. Update Ticket Information")
        print("4. Cancel a Ticket")
        print("5. Back to Main Menu")

        choice = input("Select an option: ")

        if choice == '1':
            # Call the function to book a ticket
            ticket_manager.book_ticket()
        elif choice == '2':
            # Call the function to view all tickets
            ticket_manager.view_ticket()
        elif choice == '3':
            # Call the function to update a ticket
           ticket_manager.update_ticket()
        elif choice == '4':
            # Call the function to cancel a ticket
            ticket_manager.cancel_ticket()
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":

    main_menu()
