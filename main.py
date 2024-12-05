import pickle
import csv
import random
import mysql.connector
from mysql.connector import Error

# Connect to MySQL
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',  # Change if needed
            user='root',       # MySQL username
            password='yourpassword',  # MySQL password
            database='ESA'     # Database name
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error: {e}")
    return None

# Functions for customer management
def add_customer_cli():
    while True:
        customer_number = input("Enter customer number (e.g., ESA1234): ").strip()
        if customer_number.startswith("ESA") and customer_number[3:].isdigit():
            break
        print("Error: Customer number must start with 'ESA' followed by numbers.")

    fn = input("Enter full name: ").strip()
    if not fn:
        print("Operation canceled.")
        return

    age = input("Enter age: ").strip()
    if not age:
        print("Operation canceled.")
        return

    sex = input("Enter sex (M/F): ").strip()
    if not sex:
        print("Operation canceled.")
        return

    destination = input("Enter destination: ").strip()
    if not destination:
        print("Operation canceled.")
        return

    start_place = input("Enter start place: ").strip()
    if not start_place:
        print("Operation canceled.")
        return

    if customer_number and fn and age and sex and destination and start_place:
        customer = [customer_number, fn, age, sex, destination, start_place]
        with open('customer_data.dat', 'ab') as file:
            pickle.dump(customer, file)
        print("Customer data saved successfully.")
    else:
        print("Error: All fields must be filled.")


def search_customer_cli():
    name = input("Enter the name to search: ").strip()
    found = False
    if name:
        try:
            with open('customer_data.dat', 'rb') as file:
                while True:
                    try:
                        customer = pickle.load(file)
                        if customer[1].lower() == name.lower():
                            print(f"Customer Found: {customer}")
                            found = True
                            break
                    except EOFError:
                        break
        except FileNotFoundError:
            print("Error: No customer data found.")

        if not found:
            print("Customer not found.")
    else:
        print("Error: Name field is required.")


def modify_customer_cli():
    customer_number = input("Enter the customer number to modify: ").strip()
    customers = []
    found = False

    if not customer_number:
        print("Error: Customer number field is required.")
        return

    try:
        with open('customer_data.dat', 'rb') as file:
            while True:
                try:
                    customer = pickle.load(file)
                    customers.append(customer)
                except EOFError:
                    break
    except FileNotFoundError:
        print("Error: No customer data found.")
        return

    for customer in customers:
        if customer[0] == customer_number:
            new_name = input(f"Enter new full name ({customer[1]}): ") or customer[1]
            new_age = input(f"Enter new age ({customer[2]}): ") or customer[2]
            new_sex = input(f"Enter new sex (M/F) ({customer[3]}): ") or customer[3]
            new_destination = input(f"Enter new destination ({customer[4]}): ") or customer[4]
            new_start_place = input(f"Enter new start place ({customer[5]}): ") or customer[5]
            customer[1], customer[2], customer[3], customer[4], customer[5] = new_name, new_age, new_sex, new_destination, new_start_place
            found = True
            break

    if found:
        with open('customer_data.dat', 'wb') as file:
            for customer in customers:
                pickle.dump(customer, file)
        print("Customer details updated successfully.")
    else:
        print("Customer not found.")


def delete_customer_cli():
    customer_number = input("Enter the customer number to delete: ").strip()
    customers = []
    found = False

    if not customer_number:
        print("Error: Customer number field is required.")
        return

    try:
        with open('customer_data.dat', 'rb') as file:
            while True:
                try:
                    customer = pickle.load(file)
                    if customer[0] != customer_number:
                        customers.append(customer)
                    else:
                        found = True
                except EOFError:
                    break
    except FileNotFoundError:
        print("Error: No customer data found.")
        return

    if found:
        with open('customer_data.dat', 'wb') as file:
            for customer in customers:
                pickle.dump(customer, file)
        print("Customer record deleted successfully.")
    else:
        print("Customer not found.")


def read_customer_data_cli():
    try:
        with open('customer_data.dat', 'rb') as file:
            customer_list = []
            while True:
                try:
                    customer = pickle.load(file)
                    customer_list.append(customer)
                except EOFError:
                    break

        if customer_list:
            print("\n--- Customer Data ---")
            
            # Read seating data to cross-check if the customer has a seat booked
            try:
                with open('seating_data.csv', 'r') as file:
                    reader = csv.reader(file)
                    seating_data = [row for row in reader]
            except FileNotFoundError:
                print("Error: Seating data file not found.")
                seating_data = []

            # Loop through each customer and check if they have a booked seat
            for customer in customer_list:
                customer_number = customer[0]
                customer_name = customer[1]
                customer_age = customer[2]
                customer_sex = customer[3]
                customer_destination = customer[4]
                customer_start_place = customer[5]

                # Find if the customer has a seat booked
                booked_seat = None
                for row in seating_data:
                    if len(row) > 3 and row[3] == customer_number and row[2] == 'Booked':
                        booked_seat = f"Section: {row[0]}, Seat: {row[1]}"
                        break

                # Display customer info
                print(f"ID          : {customer_number}")
                print(f"Name        : {customer_name}")
                print(f"Age         : {customer_age}")
                print(f"Sex         : {customer_sex}")
                print(f"Destination : {customer_destination}")
                print(f"Start Place : {customer_start_place}")

                if booked_seat:
                    print(f"Booked Seat : {booked_seat}")
                else:
                    print("No seat booked by this customer yet.")
                
                print("-" * 30)  # Separator line
        else:
            print("No customer data available.")
    except FileNotFoundError:
        print("Error: No customer data found.")


# Billing Section
def add_billing_cli():
    connection = create_connection()
    if connection is None:
        print("Error: Could not connect to database.")
        return

    # Get customer data
    customer_number = input("Enter customer number (e.g., ESA1234): ").strip()
    full_name = input("Enter your full name: ").strip()
    card_number = input("Enter your credit card number: ").strip()
    cvv = input("Enter your CVV: ").strip()
    exp_date = input("Enter credit card expiry date (MM/YY): ").strip()

    if not all([customer_number, full_name, card_number, cvv, exp_date]):
        print("Error: All fields are required.")
        return

    # Determine the amount paid (you can modify this logic as per your pricing model)
    print("\nSelect your seat type:")
    print("1. Economy - 7000")
    print("2. Premium Economy - 15000")
    print("3. Business - 40000")
    seat_type = input("Enter seat type number: ").strip()

    if seat_type == '1':
        amount_paid = 7000
    elif seat_type == '2':
        amount_paid = 15000
    elif seat_type == '3':
        amount_paid = 40000
    else:
        print("Invalid seat type. Defaulting to Economy.")
        amount_paid = 7000

    # Insert billing information into the database
    cursor = connection.cursor()
    try:
        query = """
            INSERT INTO user (customer_number, full_name, card_number, cvv, exp_date, amount_paid)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (customer_number, full_name, card_number, cvv, exp_date, amount_paid))
        connection.commit()
        print("Billing information stored successfully.")

        # Fetch the last inserted record (invoice summary)
        cursor.execute("SELECT * FROM user ORDER BY booking_date DESC LIMIT 1")
        invoice = cursor.fetchone()

        # Print the invoice summary
        print("\n--- Invoice Summary ---")
        print(f"Customer Number: {invoice[1]}")
        print(f"Full Name      : {invoice[2]}")
        print(f"Card Number    : {'*' * (len(invoice[3]) - 4) + invoice[3][-4:]}")
        print(f"CVV            : {'*' * len(invoice[4])}")
        print(f"Exp. Date      : {invoice[5]}")
        print(f"Amount Paid    : {invoice[6]}")
        print(f"Booking Date   : {invoice[7]}")
        print("-----------------------")
    except Error as e:
        print(f"Error inserting data: {e}")
        connection.rollback()
    finally:
        cursor.close()
        connection.close()


# Seating Management Functions
def display_seating_cli():
    # Define seating sections and total seats per section
    seating_sections = {
        'Business': 10,           # 10 seats in Business
        'Premium Economy': 15,    # 15 seats in Premium Economy
        'Economy': 20             # 20 seats in Economy
    }

    seats = {'Business': [], 'Premium Economy': [], 'Economy': []}
    
    # Randomly generate seating arrangements
    for section, total_seats in seating_sections.items():
        for seat_number in range(1, total_seats + 1):
            status = 'Available' if random.choice([True, False]) else 'Booked'
            seats[section].append({'seat': f"{seat_number}", 'status': status})
    
    # Display up to 5 available seats per section
    for section, seat_list in seats.items():
        available_seats = [seat['seat'] for seat in seat_list if seat['status'] == 'Available']
        if available_seats:
            random_seats = random.sample(available_seats, min(len(available_seats), 5))
            print(f"{section}: {', '.join(random_seats)}")  # Show up to 5 random available seats
        else:
            print(f"{section}: No available seats")


def book_seat_cli():
    customer_number = input("Enter your customer number (e.g., ESA1234): ").strip()
    if not customer_number:
        print("Error: Customer number is required.")
        return

    # Load the seating data from the CSV
    try:
        with open('seating_data.csv', 'r', newline='') as file:
            reader = csv.reader(file)
            seating_data = [row for row in reader]
    except FileNotFoundError:
        print("Seating data file not found.")
        return

    # Display available seats with their customer ID (if booked)
    print("\n--- Available Seats ---")
    for row in seating_data:
        if row[2] == 'Available':
            print(f"Section: {row[0]}, Seat: {row[1]} (Available)")
        elif row[2] == 'Booked':
            print(f"Section: {row[0]}, Seat: {row[1]} (Booked by {row[3]})")

    # Prompt the user to select a section and seat number
    section = input("\nEnter section (Business/Premium Economy/Economy): ").strip()
    seat_number = input("Enter seat number: ").strip()

    if not section or not seat_number:
        print("Error: Section and seat number are required.")
        return

    # Check if the seat is available and then book it
    seat_found = False
    updated_seating_data = []

    for row in seating_data:
        if row[0] == section and row[1] == seat_number:
            if row[2] == 'Available':
                # Mark the seat as booked and associate the customer ID with it
                row[2] = 'Booked'
                row.append(customer_number)  # Add the customer ID
                seat_found = True
            else:
                print(f"Error: Seat {seat_number} in {section} is already booked by {row[3]}.")
        updated_seating_data.append(row)

    if seat_found:
        # Save the updated seating data back to the CSV file
        with open('seating_data.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(updated_seating_data)
        print(f"Seat {seat_number} in {section} successfully booked for customer {customer_number}.")
    else:
        print("Seat not found or already booked.")


def delete_seat_cli():
    customer_number = input("Enter your customer number: ").strip()
    if not customer_number:
        print("Error: Customer number is required.")
        return

    # Load seating data
    try:
        with open('seating_data.csv', 'r') as file:
            reader = csv.reader(file)
            seating_data = [row for row in reader]
    except FileNotFoundError:
        print("Error: Seating data not found.")
        return

    # Display seats booked by the user
    user_seats = [row for row in seating_data if len(row) > 3 and row[3] == customer_number and row[2] == 'Booked']
    if not user_seats:
        print("You have no booked seats.")
        return

    print("\n--- Your Booked Seats ---")
    for row in user_seats:
        print(f"Section: {row[0]}, Seat: {row[1]}")

    # Prompt user for cancellation
    section = input("\nEnter section to cancel (Business/Premium Economy/Economy): ").strip()
    seat_number = input("Enter seat number to cancel: ").strip()

    if not section or not seat_number:
        print("Error: Section and seat number are required.")
        return

    # Attempt to cancel the booking
    seat_found = False
    updated_seating_data = []

    for row in seating_data:
        if row[0] == section and row[1] == seat_number and len(row) > 3 and row[3] == customer_number:
            if row[2] == 'Booked':
                row[2] = 'Available'
                row.pop()  # Remove customer association
                seat_found = True
                print(f"Seat {seat_number} in {section} successfully canceled.")
        updated_seating_data.append(row)

    if seat_found:
        with open('seating_data.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(updated_seating_data)
    else:
        print("Seat not found or not booked by you.")


# Main menu with billing option
def main_menu():
    while True:
        print("\n=== East Sky Airlines Management ===")
        print("1. Customer Management")
        print("2. Seating Management")
        print("3. Billing")
        print("4. Exit")
        ch = input("Select an option: ").strip()

        if ch == '1':
            customer_management_menu()
        elif ch == '2':
            seating_management_menu()
        elif ch == '3':
            add_billing_cli()
        elif ch == '4':
            print("Exiting program.")
            break
        else:
            print("Invalid option, please try again.")

# Customer management menu for CLI
def customer_management_menu():
    while True:
        print("\n--- Customer Management ---")
        print("1. Add Customer")
        print("2. Search Customer")
        print("3. Modify Customer")
        print("4. Delete Customer")
        print("5. Read Customer Data")
        print("6. Back to Main Menu")
        ch = input("Select an option: ").strip()

        if ch == '1':
            add_customer_cli()
        elif ch == '2':
            search_customer_cli()
        elif ch == '3':
            modify_customer_cli()
        elif ch == '4':
            delete_customer_cli()
        elif ch == '5':
            read_customer_data_cli()
        elif ch == '6':
            break
        else:
            print("Invalid option, please try again.")

# Seating management menu for CLI
def seating_management_menu():
    while True:
        print("\n--- Seating Management ---")
        print("1. Display Available Seats")
        print("2. Book Seat")
        print("3. Cancel Seat Booking")
        print("4. Back to Main Menu")
        ch = input("Select an option: ").strip()

        if ch == '1':
            display_seating_cli()
        elif ch == '2':
            book_seat_cli()
        elif ch == '3':
            delete_seat_cli()
        elif ch == '4':
            break
        else:
            print("Invalid option, please try again.")

if __name__ == "__main__":
    main_menu()
