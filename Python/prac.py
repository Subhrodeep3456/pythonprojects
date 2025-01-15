import csv
import pickle
import random
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import os

SEAT_PRICES = {'Economy': 7000, 'Premium Economy': 15000, 'Business': 40000}
SEATING_FILE = 'seating_data.csv'
def initialize_customer_data_file():
    if not os.path.exists('customer_data.dat'):
        open('customer_data.dat', 'wb').close()
        print("Initialized customer_data.dat file.")
initialize_customer_data_file()
def initialize_files():
    if not os.path.exists('customer_data.dat'):
        open('customer_data.dat', 'wb').close()
        print("Initialized customer_data.dat file.")

    if not os.path.exists(SEATING_FILE):
        create_seating_file()
        print("Initialized seating_data.csv file.")
def create_seating_file():
    with open(SEATING_FILE, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Row', 'Seat', 'Class', 'Status'])
        for row in range(1, 31):
            seat_class = ('Business' if row <= 4 else 'Premium Economy' if row <= 9 else 'Economy')
            for seat in 'ABCDEF':
                writer.writerow([row, seat, seat_class, random.choice(['Available', 'Booked'])])
initialize_files()
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost', user='root', password='subhro'
        )
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("CREATE DATABASE IF NOT EXISTS ESA")
            cursor.execute("USE ESA")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user (
                    customer_number VARCHAR(20) PRIMARY KEY,
                    full_name VARCHAR(100) NOT NULL,
                    age INT NOT NULL,
                    sex ENUM('M', 'F') NOT NULL,
                    destination VARCHAR(100) NOT NULL,
                    start_place VARCHAR(100) NOT NULL
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS billing (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    customer_number VARCHAR(20),
                    card_number VARCHAR(20),
                    cvv VARCHAR(3),
                    exp_date VARCHAR(5),
                    amount_paid DECIMAL(10, 2),
                    FOREIGN KEY (customer_number) REFERENCES user(customer_number)
                )
            """)
            cursor.close()
            return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
    return None
def sync_customers_to_mysql():
    connection = create_connection()
    if not connection:
        print("Error: Could not connect to the database.")
        return

    try:
        cursor = connection.cursor()

        with open('customer_data.dat', 'rb') as file:
            while True:
                try:
                    customer = pickle.load(file)
                    cursor.execute("""
                        INSERT INTO user (customer_number, full_name, age, sex, destination, start_place)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE
                        full_name = VALUES(full_name),
                        age = VALUES(age),
                        sex = VALUES(sex),
                        destination = VALUES(destination),
                        start_place = VALUES(start_place)
                    """, customer)
                except EOFError:
                    break

        connection.commit()
        print("Customer data successfully synced with MySQL.")
    except Exception as e:
        print(f"Error syncing data: {e}")
    finally:
        cursor.close()
        connection.close()
def add_customer_cli():
    customer_number = input("Enter customer number (e.g., ESA1234): ").strip()
    if not (customer_number.startswith("ESA") and customer_number[3:].isdigit()):
        print("Invalid customer number format.")
        return

    customer_data = [
        customer_number,
        input("Enter full name: ").strip(),
        input("Enter age: ").strip(),
        input("Enter sex (M/F): ").strip(),
        input("Enter destination: ").strip(),
        input("Enter start place: ").strip()
    ]

    if all(customer_data):
        with open('customer_data.dat', 'ab') as file:
            pickle.dump(customer_data, file)
        print("Customer data saved successfully.")
    else:
        print("Error: All fields must be filled.")
def modify_customer_cli():
    customer_number = input("Enter the customer number to modify: ").strip()
    customers = []
    found = False

    try:
        with open('customer_data.dat', 'rb') as file:
            while True:
                try:
                    customer = pickle.load(file)
                    if customer[0] == customer_number:
                        print("\n--- Current Details ---")
                        print(f"Full Name      : {customer[1]}")
                        print(f"Age            : {customer[2]}")
                        print(f"Sex            : {customer[3]}")
                        print(f"Destination    : {customer[4]}")
                        print(f"Start Place    : {customer[5]}")

                        customer[1] = input("Enter new full name (leave blank to keep current): ") or customer[1]
                        customer[2] = input("Enter new age (leave blank to keep current): ") or customer[2]
                        customer[3] = input("Enter new sex (leave blank to keep current): ") or customer[3]
                        customer[4] = input("Enter new destination (leave blank to keep current): ") or customer[4]
                        customer[5] = input("Enter new start place (leave blank to keep current): ") or customer[5]

                        found = True
                    customers.append(customer)
                except EOFError:
                    break
    except FileNotFoundError:
        print("Error: Customer data file not found.")
        return

    if found:
        with open('customer_data.dat', 'wb') as file:
            for customer in customers:
                pickle.dump(customer, file)
        print("Customer details updated successfully.")
    else:
        print("Error: Customer not found.")
def delete_customer_cli():
    customer_number = input("Enter the customer number to delete: ").strip()
    customers = []
    found = False

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
        print("Error: Customer data file not found.")
        return

    if found:
        with open('customer_data.dat', 'wb') as file:
            for customer in customers:
                pickle.dump(customer, file)
        print("Customer deleted successfully.")
    else:
        print("Error: Customer not found.")
def search_customer_cli():
    customer_number = input("Enter customer number to search (e.g., ESA1234): ").strip()
    customer = search_customer_in_file(customer_number)

    if customer:
        booked_seat = get_customer_booked_seat(customer[0])
        print("\n--- Customer Details ---")
        print(f"Customer ID    : {customer[0]}")
        print(f"Full Name      : {customer[1]}")
        print(f"Age            : {customer[2]}")
        print(f"Sex            : {customer[3]}")
        print(f"Destination    : {customer[4]}")
        print(f"Start Place    : {customer[5]}")
        print(f"Booked Seat    : {booked_seat}")
    else:
        print("Error: Customer not found.")
def read_all_customers_cli():
    try:
        with open('customer_data.dat', 'rb') as file:
            print("\n--- All Customer Records ---")
            print("{:<15} {:<20} {:<5} {:<5} {:<15} {:<15} {:<25}".format(
                "Customer ID", "Full Name", "Age", "Sex", "Destination", "Start Place", "Booked Seat"
            ))
            print("-" * 100)
            while True:
                try:
                    customer = pickle.load(file)
                    booked_seat = get_customer_booked_seat(customer[0])
                    print("{:<15} {:<20} {:<5} {:<5} {:<15} {:<15} {:<25}".format(
                        customer[0], customer[1], customer[2], customer[3],
                        customer[4], customer[5], booked_seat
                    ))
                except EOFError:
                    break
    except FileNotFoundError:
        print("Error: Customer data file not found.")
def read_all_data():
    connection = create_connection()
    if not connection:
        print("Error: Could not connect to the database.")
        return

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM user")
        rows = cursor.fetchall()

        print("\n--- Customer Data ---")
        for row in rows:
            customer_number, full_name, age, sex, destination, start_place, booked_seat = row
            seat_info = booked_seat if booked_seat else "No seat has been booked yet"
            print(f"Customer Number: {customer_number}, Name: {full_name}, Seat: {seat_info}")
    except Exception as e:
        print(f"Error reading customer data: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
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
        print("Error: Customer data file not found.")
    return None
def display_seats_with_classes():
    try:
        with open(SEATING_FILE, 'r') as file:
            reader = csv.DictReader(file)
            seats = list(reader)

        print("\n--- Seating Chart ---")
        print("   A   B   C   |   D   E   F")
        print("  ----------------------------------")

        def display_section(section_name, start_row, end_row):
            print(f"\n--- {section_name} ---")
            for row in range(start_row, end_row + 1):
                left_side = []
                right_side = []
                for seat in seats:
                    if int(seat['Row']) == row:
                        seat_display = f"{seat['Row']}{seat['Seat']} ({'A' if seat['Status'] == 'Available' else 'B'})"
                        if seat['Seat'] in "ABC":
                            left_side.append(seat_display)
                        else:
                            right_side.append(seat_display)

                print(f"Row {row:02} | {' '.join(left_side):<15} | {' '.join(right_side):<15}")

        # Display sections
        display_section("Business Class", 1, 4)
        display_section("Premium Economy", 5, 9)
        display_section("Economy", 10, 30)

    except FileNotFoundError:
        print("Error: Seating file not found.")

def verify_customer_in_mysql(customer_number):
    connection = create_connection()
    if not connection:
        print("Error: Could not connect to the database.")
        return False

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM user WHERE customer_number = %s", (customer_number,))
        result = cursor.fetchone()
        return result[0] > 0
    except Exception as e:
        print(f"Error verifying customer: {e}")
        return False
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def add_billing():
    connection = create_connection()
    if not connection:
        print("Error: Could not connect to the database.")
        return

    try:
        customer_number = input("Enter your customer number (e.g., ESA1234): ").strip()
        if not customer_number:
            print("Customer number cannot be blank.")
            return

        # Verify customer existence
        if not verify_customer_in_mysql(customer_number):
            print("Error: Customer does not exist. Billing cannot be added.")
            return

        card_number = input("Enter your credit card number: ").strip()
        if not card_number:
            print("Card number cannot be blank.")
            return

        exp_date = input("Enter credit card expiry date (MM/YY): ").strip()
        if not exp_date:
            print("Expiry date cannot be blank.")
            return

        cvv = input("Enter CVV: ").strip()
        if not cvv:
            print("CVV cannot be blank.")
            return

        amount_paid = 1000.00  # Example fixed amount
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO billing (customer_number, card_number, exp_date, amount_paid, cvv)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (customer_number, card_number, exp_date, amount_paid, cvv)
        )

        connection.commit()
        print("Billing information stored successfully.")

        # Generate Invoice
        masked_cvv = "*" * len(cvv)
        print(f"\n--- Invoice ---")
        print(f"Customer Number: {customer_number}")
        print(f"Card Number    : {card_number}")
        print(f"Expiry Date    : {exp_date}")
        print(f"Amount Paid    : ₹{amount_paid:.2f}")
        print(f"CVV            : {masked_cvv}")

    except Exception as e:
        print(f"Error during billing: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

sync_customers_to_mysql()
def generate_invoice(customer_number):
    connection = create_connection()
    if not connection:
        print("Error: Could not connect to the database.")
        return

    try:
        cursor = connection.cursor()
        # Fetch billing record for the customer
        cursor.execute("SELECT card_number, exp_date, amount_paid, cvv FROM billing WHERE customer_number = %s", (customer_number,))
        invoice = cursor.fetchone()

        # Check if an invoice was found
        if not invoice:
            print("No billing record found for the customer number provided.")
            cursor.close()  # Close the cursor before exiting
            return

        # Extract fields from the result
        card_number, exp_date, amount_paid, cvv = invoice

        # Validate fields to ensure no null or empty values
        if not card_number or not exp_date or not amount_paid or not cvv:
            print("Error: Billing record contains null or empty values.")
            cursor.close()  # Close the cursor before exiting
            exit(1)

        # Mask CVV for security
        masked_cvv = "*" * len(cvv)

        # Display invoice details
        print(f"Invoice for {customer_number}:")
        print(f"Card Number: {card_number}")
        print(f"Expiry Date: {exp_date}")
        print(f"Amount Paid: ${amount_paid:.2f}")
        print(f"CVV: {masked_cvv}")
    except Exception as e:
        print(f"Error generating invoice: {e}")
    finally:
        if cursor:
            cursor.close()  # Ensure the cursor is always closed
        if connection and connection.is_connected():
            connection.close()  # Ensure the connection is closed
def customer_management_menu():
    while True:
        print("\n--- Customer Management Menu ---")
        print("1. Add Customer")
        print("2. Modify Customer")
        print("3. Delete Customer")
        print("4. Search Customer")
        print("5. Read All Records")
        print("6. Back to Main Menu")
        choice = input("Choose an option: ").strip()

        if choice == '1':
            add_customer_cli()
        elif choice == '2':
            modify_customer_cli()
        elif choice == '3':
            delete_customer_cli()
        elif choice == '4':
            search_customer_cli()
        elif choice == '5':
            read_all_customers_cli()
        elif choice == '6':
            break
        else:
            print("Invalid option, please try again.")
def get_customer_booked_seat(customer_number):
    try:
        with open(SEATING_FILE, 'r') as file:
            reader = csv.DictReader(file)
            for seat in reader:
                if seat['Status'] == 'Booked' and seat.get('CustomerNumber') == customer_number:
                    return f"{seat['Row']}{seat['Seat']} ({seat['Class']})"
        return "No seat has been booked by the customer yet."
    except FileNotFoundError:
        return "Seating data file not found."
def seating_management_menu():
    while True:
        print("\n--- Seating Management Menu ---")
        print("1. Display Seating ")
        print("2. Book a Seat")
        print("3. Cancel/Delete Booking")
        print("4. Back to Main Menu")
        choice = input("Choose an option: ").strip()

        if choice == '1':
            display_seats_with_classes()
        elif choice == '2':
            book_seat()
        elif choice == '3':
            cancel_booking()
        elif choice == '4':
            break
        else:
            print("Invalid option, please try again.")
def billing_menu():
    while True:
        print("\n--- Billing Menu ---")
        print("1. Add Billing")
        print("2. Back to Main Menu")
        choice = input("Choose an option: ").strip()
        if choice == '1':
            add_billing()
        elif choice == '2':
            break
        else:
            print("Invalid option, please try again.")
def main_menu():
    while True:
        print("\n=== Main Menu ===")
        print("1. Customer Management")
        print("2. Seating Management")
        print("3. Billing")
        print("4. Exit")
        choice = input("Choose an option: ").strip()

        if choice == '1':
            customer_management_menu()
        elif choice == '2':
            seating_management_menu()
        elif choice == '3':
            billing_menu()
        elif choice == '4':
            print("Exiting...")
            break
        else:
            print("Invalid option, please try again.")
def display_all_seats():
    try:
        with open(SEATING_FILE, 'r') as file:
            reader = csv.DictReader(file)
            seats = list(reader)

        print("\n--- Seating Chart ---")
        for row in range(1, 31):
            seat_row = [f"{row}{seat['Seat']}: {seat['Status']}" for seat in seats if int(seat['Row']) == row]
            print(f"Row {row:02}: {' | '.join(seat_row)}")

    except FileNotFoundError:
        print("Error: Seating file not found.")
def book_seat():
    try:
        # Check if customer exists in customer_data.dat
        customer_number = input("Enter your customer number (e.g., ESA1234): ").strip()

        if not check_customer_exists(customer_number):
            print("Customer record not found. Returning to the main menu.")
            return

        # Display seat pricing
        print("\n--- Seat Pricing ---")
        print("1. Business Class    - 40,000")
        print("2. Premium Economy   - 15,000")
        print("3. Economy           - 7,000")

        row = input("Enter row number to book (1–30): ").strip()
        seat_letter = input("Enter seat letter to book (A–F): ").strip().upper()

        # Read seating data
        with open(SEATING_FILE, 'r') as file:
            reader = csv.DictReader(file)
            seats = list(reader)

        for seat in seats:
            if seat['Row'] == row and seat['Seat'] == seat_letter:
                if seat['Status'] == 'Available':
                    # Calculate seat price based on the class
                    seat_class = seat['Class']
                    price = SEAT_PRICES.get(seat_class, 0)
                    print(f"Seat {row}{seat_letter} is available in {seat_class} class. Price: {price}")

                    confirm = input("Do you want to book this seat? (yes/no): ").strip().lower()
                    if confirm == 'yes':
                        seat['Status'] = 'Booked'
                        seat['CustomerNumber'] = customer_number
                        print(f"Seat {row}{seat_letter} booked successfully!")
                    else:
                        print("Seat booking cancelled.")
                else:
                    print("Seat is already booked.")
                break
        else:
            print("Invalid seat selection.")

        with open(SEATING_FILE, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['Row', 'Seat', 'Class', 'Status', 'CustomerNumber'])
            writer.writeheader()
            writer.writerows(seats)

    except FileNotFoundError:
        print("Error: Required files not found.")
def check_customer_exists(customer_number):
    try:
        with open('customer_data.dat', 'rb') as file:
            while True:
                try:
                    customer = pickle.load(file)
                    if customer[0] == customer_number:
                        return True
                except EOFError:
                    break
    except FileNotFoundError:
        print("Error: Customer data file not found.")
    return False

def cancel_booking():
    try:
        with open(SEATING_FILE, 'r') as file:
            reader = csv.DictReader(file)
            seats = list(reader)

        print("\n--- Booked Seats ---")
        for seat in seats:
            if seat['Status'] == 'Booked':
                print(f"{seat['Row']}{seat['Seat']} - {seat['Class']}")

        row = input("Enter row number to cancel booking (1–30): ").strip()
        seat_letter = input("Enter seat letter to cancel booking (A–F): ").strip().upper()

        for seat in seats:
            if seat['Row'] == row and seat['Seat'] == seat_letter:
                if seat['Status'] == 'Booked':
                    seat['Status'] = 'Available'
                    seat.pop('CustomerNumber', None)  # Remove customer info if present
                    print(f"Booking for seat {row}{seat_letter} cancelled successfully!")
                else:
                    print("Seat is not booked.")
                break
        else:
            print("Invalid seat selection.")

        with open(SEATING_FILE, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['Row', 'Seat', 'Class', 'Status', 'CustomerNumber'])
            writer.writeheader()
            writer.writerows(seats)

    except FileNotFoundError:
        print("Error: Seating file not found.")

if __name__ == "__main__":
    main_menu()