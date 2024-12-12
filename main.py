import pickle
import csv
import random
import mysql.connector
from mysql.connector import Error

SEAT_PRICES = {
    'Economy': 7000,
    'Premium Economy': 15000,
    'Business': 40000
}

# Connect to MySQL
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='123456',
            database='ESA'
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
    age = input("Enter age: ").strip()
    sex = input("Enter sex (M/F): ").strip()
    destination = input("Enter destination: ").strip()
    start_place = input("Enter start place: ").strip()

    if all([customer_number, fn, age, sex, destination, start_place]):
        customer = [customer_number, fn, age, sex, destination, start_place]
        with open('customer_data.dat', 'ab') as file:
            pickle.dump(customer, file)
        print("Customer data saved successfully.")
    else:
        print("Error: All fields must be filled.")


def search_customer_cli():
    customer_number = input("Enter customer number to search (e.g., ESA1234): ").strip()
    
    # First, try to fetch customer data from the database
    customer = fetch_customer_data(customer_number)
    
    if customer:
        print(f"\n--- Customer Details ---")
        print(f"Customer ID : {customer['customer_number']}")
        print(f"Full Name : {customer['full_name']}")
        print(f"Age : {customer['age']}")
        print(f"Sex : {customer['sex']}")
        print(f"Destination : {customer['destination']}")
        print(f"Start Place : {customer['start_place']}")
    else:
        # If not found in the database, check the binary file
        customer = search_customer_in_file(customer_number)
        
        if customer:
            print(f"\n--- Customer Details (from file) ---")
            print(f"Customer ID : {customer[0]}")
            print(f"Full Name : {customer[1]}")
            print(f"Age : {customer[2]}")
            print(f"Sex : {customer[3]}")
            print(f"Destination : {customer[4]}")
            print(f"Start Place : {customer[5]}")
        else:
            print("Error: Customer not found.")

def search_customer_in_file(customer_number):
    try:
        with open('customer_data.dat', 'rb') as file:
            while True:
                try:
                    customer = pickle.load(file)
                    if customer[0] == customer_number:
                        return customer
                except EOFError:
                    break
    except FileNotFoundError:
        print("Error: No customer data found.")
    
    return None

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
    pass


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

def fetch_customer_data(customer_number):
    connection = create_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM user WHERE customer_number = %s"
        cursor.execute(query, (customer_number,))
        customer = cursor.fetchone()
        cursor.close()
        connection.close()
        return customer
    return None


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

def get_seating_price(seat_class):
    return SEAT_PRICES.get(seat_class, 0)


def generate_invoice(customer_number):
    customer = fetch_customer_data(customer_number)
    
    if not customer:
        print(f"Error: Customer {customer_number} not found.")
        return
    
    full_name = customer['full_name']
    
    # Generate and display invoice summary here
    print("\n--- Invoice ---")
    print(f"Customer Name : {full_name}")
    
    # Assuming you have stored amount_paid in your database
    amount_paid = get_seating_price('Economy')  # Adjust based on actual payment logic
    print(f"Amount Paid : {amount_paid}")
    
    print("------------------------")




# Seating Management Functions
def display_seating_cli():
    # Define seating sections and total seats per section
    seating_sections = {
        'Business': 10,           # 10 seats in Business
        'Premium Economy': 10,    # 10 seats in Premium Economy
        'Economy': 10             # 10 seats in Economy
    }

    seats = {'Business': [], 'Premium Economy': [], 'Economy': []}
    
    # Randomly generate seating arrangements (Fixed order now)
    for section, total_seats in seating_sections.items():
        for seat_number in range(1, total_seats + 1):
            status = 'Available' if random.choice([True, False]) else 'Booked'
            seats[section].append({'seat': f"{seat_number}", 'status': status})
    
    # Display seats (show up to 5 random available seats per section)
    print("\n--- Available Seats ---")
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

    # Fetch customer data from the database
    customer = fetch_customer_data(customer_number)
    if not customer:
        # If not found in the database, check the binary file
        customer = search_customer_in_file(customer_number)
        if not customer:
            print(f"Error: Customer {customer_number} not found in the system.")
            return

    # Display available seats
    display_seating_cli()

    # Ask the user for their seat choice
    seat_class = input("\nEnter seat class (Business/Premium Economy/Economy): ").strip()
    seat_number = input("Enter seat number: ").strip()

    if not seat_class or not seat_number:
        print("Error: Both seat class and seat number are required.")
        return

    # Process seat booking
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        
        # Check if the seat is available
        cursor.execute("SELECT * FROM seating WHERE seat_class = %s AND seat_number = %s", (seat_class, seat_number))
        row = cursor.fetchone()
        
        if row and row['status'] == 'Available':
            # Book the seat
            cursor.execute("""
                UPDATE seating SET status = 'Booked', customer_number = %s
                WHERE seat_class = %s AND seat_number = %s
            """, (customer_number, seat_class, seat_number))
            connection.commit()
            print(f"Seat {seat_number} in {seat_class} successfully booked for customer {customer_number}.")
        else:
            print("Error: Seat is not available.")
        
        cursor.close()
        connection.close()
    else:
        print("Error: Could not connect to the database.")


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
            seating_management_menu()  # Ensure this function is defined elsewhere
        elif ch == '3':
            billing_section()  # Ensure this function is defined elsewhere
        elif ch == '4':
            print("Exiting program.")
            break
        else:
            print("Invalid option, please try again.")

def generate_invoice(customer_number):
    # Fetching invoice details from the database (or can be adjusted based on requirements)
    customer = fetch_customer_data(customer_number)
    
    if not customer:
        print(f"Error: Customer {customer_number} not found.")
        return
    
    full_name = customer['full_name']
    
    # Generate and display invoice summary here
    print("\n--- Invoice ---")
    print(f"Customer Name : {full_name}")
    print(f"Amount Paid : {get_seating_price('Economy')}")  # Adjust based on actual payment logic
    print("------------------------")

def customer_management_menu():
    while True:
        print("\n--- Customer Management Menu ---")
        print("1. Add Customer")
        print("2. Search Customer")
        print("3. Back to Main Menu")

        choice = input("Select an option: ").strip()

        if choice == '1':
            add_customer_cli()
        elif choice == '2':
            search_customer_cli()
        elif choice == '3':
            break  # Go back to main menu
        else:
            print("Invalid option, please try again.")

def billing_section():
    print("\n--- Billing ---")
    # Ask the user for their customer number
    customer_number = input("Enter your customer number (e.g., ESA1234): ").strip()
    
    # Fetch customer data from the database
    customer = fetch_customer_data(customer_number)
    if not customer:
        print(f"Error: Customer {customer_number} not found in the system.")
        return
    
    # Automatically fill in billing details using the data from the database
    full_name = customer['full_name']
    seat_class = customer['seat_class']
    
    print(f"\nCustomer found: {full_name}")
    print(f"Seat Class : {seat_class}")
    
    # Display seat price
    amount_due = get_seating_price(seat_class)
    print(f"Total Amount Due: {amount_due}")
    
    # Prompt for credit card details
    card_number = input("Enter your credit card number: ").strip()
    cvv = input("Enter your CVV: ").strip()
    exp_date = input("Enter credit card expiry date (MM/YY): ").strip()
    
    # Mask sensitive information for display
    masked_card_number = '*' * (len(card_number) - 4) + card_number[-4:]
    masked_cvv = '*' * len(cvv)
    
    # Confirm payment
    confirm_payment = input("\nConfirm payment? (y/n): ").strip().lower()
    
    if confirm_payment == 'y':
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            try:
                # Insert billing information into the database
                query = """ 
                INSERT INTO billing (customer_number, full_name, card_number, cvv, exp_date, amount_paid) 
                VALUES (%s, %s, %s, %s, %s, %s) 
                """
                cursor.execute(query, (customer_number, full_name, masked_card_number, masked_cvv, exp_date, amount_due))
                connection.commit()
                
                print("\nPayment processed successfully!")
                
                # Generate and display invoice
                generate_invoice(customer_number)
                
            except Error as e:
                print(f"Error inserting data: {e}")
                connection.rollback()
            finally:
                cursor.close()
                connection.close()
        else:
            print("Error: Could not connect to the database.")
    else:
        print("Payment canceled.")


def display_and_book_seat_cli():
    # Get customer number
    customer_number = input("Enter your customer number (e.g., ESA1234): ").strip()
    if not customer_number:
        print("Error: Customer number is required.")
        return

    # Read seating data from CSV
    seating_data = []
    try:
        with open('seating_data.csv', 'r') as file:
            reader = csv.reader(file)
            seating_data = [row for row in reader]
    except FileNotFoundError:
        print("Error: Seating data file not found.")
        return

    # Shuffle the seating data (excluding the header)
    random.shuffle(seating_data[1:])  # Shuffle only the data rows

    # Display available seats
    print("\n--- Available Seats ---")
    available_seats = []
    for row in seating_data[1:]:  # Skip header
        if len(row) > 3 and row[2] == 'Available':
            available_seats.append(row)

    if available_seats:
        for row in available_seats:
            print(f"Section: {row[0]}, Seat: {row[1]}")
    else:
        print("No available seats.")

    # Ask the user for their seat choice
    seat_class_alias = input("\nEnter seat class (B for Business, PE for Premium Economy, E for Economy): ").strip().upper()
    seat_number = input("Enter seat number: ").strip()

    # Map aliases to full class names
    seat_class_map = {
        'B': 'Business',
        'PE': 'Premium Economy',
        'E': 'Economy'
    }

    seat_class = seat_class_map.get(seat_class_alias)
    if not seat_class:
        print("Error: Invalid seat class alias.")
        return

    if not seat_number:
        print("Error: Seat number is required.")
        return

    # Check if the seat is available and book it
    seat_found = False
    for row in seating_data[1:]:  # Skip header
        if row[0] == seat_class and row[1] == seat_number:
            if row[2] == 'Available':
                row[2] = 'Booked'  # Update status to 'Booked'
                row[3] = customer_number  # Assign customer number
                seat_found = True
                print(f"Seat {seat_number} in {seat_class} has been successfully booked for {customer_number}.")
            else:
                print(f"Error: Seat {seat_number} in {seat_class} is already booked.")
            break

    if not seat_found:
        print(f"Error: Seat {seat_number} in {seat_class} not found.")

    # Write updated seating data back to CSV
    with open('seating_data.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(seating_data)

import csv
import random

# Function to create seating data
import csv
import random

def create_seating_data(filename):
    sections = ['Business'] * 5 + ['Premium Economy'] * 6 + ['Economy'] * 19
    seat_labels = [f"{row}{col}" for row in range(1, 31) for col in 'ABCDEF']  # 30 rows with seats A-F

    # Create seating data with random availability
    seating_data = [['Section', 'Seat Number', 'Status', 'Customer Number']]
    for section, seat_number in zip(sections, seat_labels):
        status = random.choice(['Available', 'Booked'])  # Randomly assign status
        seating_data.append([section, seat_number, status, ''])  # Customer Number is empty initially

    # Shuffle the seating data (excluding the header)
    random.shuffle(seating_data[1:])  # Shuffle only the data rows

    # Write to CSV
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(seating_data)

    print(f"{filename} created successfully with random seating arrangements.")


# Create the seating data CSV file
create_seating_data('seating_data.csv')

# Update the seating management menu to use the new function
def seating_management_menu():
    while True:
        print("\n--- Seating Management ---")
        print("1. Display and Book Seat")
        print("2. Cancel Seat Booking")
        print("3. Back to Main Menu")
        ch = input("Select an option: ").strip()

        if ch == '1':
            display_and_book_seat_cli()
        elif ch == '2':
            delete_seat_cli()
        elif ch == '3':
            break
        else:
            print("Invalid option, please try again.")
if __name__ == "__main__":
    main_menu()

if __name__ == "__main__":
    while True:
        billing_section()
