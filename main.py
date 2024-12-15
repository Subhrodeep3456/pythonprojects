import pickle
import csv
import random
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import os

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
            password='subhro'
        )
        if connection.is_connected():
            cursor = connection.cursor()
            # Ensure the database exists
            cursor.execute("CREATE DATABASE IF NOT EXISTS ESA")
            cursor.execute("USE ESA")

            # Create user table
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

            # Create billing table
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

# Functions for customer management
def add_customer_cli(dat_file, db_config):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

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

    customer = [customer_number, fn, age, sex, destination, start_place]

    # Write to .dat file
    with open(dat_file, 'ab') as file:
        pickle.dump(customer, file)

    # Write to USER table
    cursor.execute('''
        INSERT IGNORE INTO USER (customer_number, full_name, age, sex)
        VALUES (%s, %s, %s, %s)
    ''', (customer_number, fn, age, sex))

    # Write to BILLING table
    cursor.execute('''
        INSERT IGNORE INTO BILLING (customer_number, destination, start_place)
        VALUES (%s, %s, %s)
    ''', (customer_number, destination, start_place))

    conn.commit()
    conn.close()
    print("Customer data added successfully.")

def delete_customer(dat_file, db_config, customer_number_to_delete):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Delete from the database
    cursor.execute("DELETE FROM BILLING WHERE customer_number = %s", (customer_number_to_delete,))
    cursor.execute("DELETE FROM USER WHERE customer_number = %s", (customer_number_to_delete,))
    conn.commit()

    # Update the .dat file
    customers = []
    if os.path.exists(dat_file):
        with open(dat_file, 'rb') as file:
            try:
                while True:
                    customer = pickle.load(file)
                    if customer[0] != customer_number_to_delete:
                        customers.append(customer)
            except EOFError:
                pass

    # Rewrite the updated data back to the .dat file
    with open(dat_file, 'wb') as file:
        for customer in customers:
            pickle.dump(customer, file)

    conn.close()
    print(f"Customer {customer_number_to_delete} deleted successfully.")



def search_customer_cli():
    customer_number = input("Enter customer number to search (e.g., ESA1234): ").strip()
    
    # Try to fetch from database first
    customer = fetch_customer_data(customer_number)
    
    if customer:
        print("\n--- Customer Details (from database) ---")
        print(f"Customer ID    : {customer['customer_number']}")
        print(f"Full Name      : {customer['full_name']}")
        print(f"Age            : {customer['age']}")
        print(f"Sex            : {customer['sex']}")
        print(f"Destination    : {customer['destination']}")
        print(f"Start Place    : {customer['start_place']}")
    else:
        # Fallback to file search
        customer = search_customer_in_file(customer_number)
        
        if customer:
            print("\n--- Customer Details (from file) ---")
            print(f"Customer ID    : {customer[0]}")
            print(f"Full Name      : {customer[1]}")
            print(f"Age            : {customer[2]}")
            print(f"Sex            : {customer[3]}")
            print(f"Destination    : {customer[4]}")
            print(f"Start Place    : {customer[5]}")
        else:
            print("Error: Customer not found in database or file.")



def search_customer_in_file(customer_number):
    try:
        with open('customer_data.dat', 'rb') as file:
            while True:
                try:
                    customer = pickle.load(file)
                    print(f"Checking customer: {customer[0]}")  # Debug statement
                    if customer[0] == customer_number:
                        return customer
                except EOFError:
                    break
    except FileNotFoundError:
        print("Error: Customer data file not found.")
    return None


def debug_print_customer_data():
    print("\n--- Debug: Customer Data File Contents ---")
    try:
        with open('customer_data.dat', 'rb') as file:
            while True:
                try:
                    customer = pickle.load(file)
                    print(customer)
                except EOFError:
                    break
    except FileNotFoundError:
        print("Error: Customer data file not found.")


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

    # Load existing customers from the .dat file
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

    # If customer was found in the .dat file, delete from database as well
    if found:
        # Delete from MySQL database
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            try:
                # Delete from billing table first due to foreign key constraint
                cursor.execute("DELETE FROM billing WHERE customer_number = %s", (customer_number,))
                cursor.execute("DELETE FROM user WHERE customer_number = %s", (customer_number,))
                connection.commit()
                print("Customer record deleted from database successfully.")
            except Error as e:
                print(f"Error deleting from database: {e}")
                connection.rollback()
            finally:
                cursor.close()
                connection.close()

        # Now write back the remaining customers to the .dat file
        with open('customer_data.dat', 'wb') as file:
            for customer in customers:
                pickle.dump(customer, file)

        print("Customer record deleted successfully from .dat file.")
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
        try:
            cursor = connection.cursor(dictionary=True)
            query = "SELECT * FROM user WHERE customer_number = %s"
            cursor.execute(query, (customer_number,))
            customer = cursor.fetchone()
            cursor.close()
            return customer
        except mysql.connector.Error as e:
            print(f"Database error: {e}")
        finally:
            connection.close()
    return None



# Billing Section
def add_billing_cli():
    connection = create_connection()
    if connection is None:
        print("Error: Could not connect to database.")
        return

    # Get customer data
    customer_number = input("Enter customer number (e.g., ESA1234): ").strip()
    card_number = input("Enter your credit card number: ").strip()
    cvv = input("Enter your CVV: ").strip()
    exp_date = input("Enter credit card expiry date (MM/YY): ").strip()

    if not all([customer_number, card_number, cvv, exp_date]):
        print("Error: All fields are required.")
        return

    # Determine the amount paid
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

    # Insert billing information into the billing table (without full_name)
    cursor = connection.cursor()
    try:
        query = """
            INSERT INTO billing (customer_number, card_number, cvv, exp_date, amount_paid)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (customer_number, card_number, cvv, exp_date, amount_paid))
        connection.commit()
        print("Billing information stored successfully.")
    except Error as e:
        print(f"Error inserting billing data: {e}")
        connection.rollback()
    finally:
        cursor.close()
        connection.close()

def sync_data_to_db(dat_file, db_config):
    # Connect to MySQL database
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Create tables if they don't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS USER (
            customer_number VARCHAR(20) PRIMARY KEY,
            full_name VARCHAR(100),
            age INT,
            sex VARCHAR(10)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS BILLING (
            customer_number VARCHAR(20) PRIMARY KEY,
            destination VARCHAR(100),
            start_place VARCHAR(100),
            FOREIGN KEY(customer_number) REFERENCES USER(customer_number)
        )
    ''')

    # Check if the .dat file exists
    if not os.path.exists(dat_file):
        print("No data file found. Sync skipped.")
        return

    # Load data from .dat file
    with open(dat_file, 'rb') as file:
        try:
            while True:
                customer = pickle.load(file)
                customer_number, full_name, age, sex, destination, start_place = customer

                # Insert data into USER table
                cursor.execute('''
                    INSERT IGNORE INTO USER (customer_number, full_name, age, sex)
                    VALUES (%s, %s, %s, %s)
                ''', (customer_number, full_name, age, sex))

                # Insert data into BILLING table
                cursor.execute('''
                    INSERT IGNORE INTO BILLING (customer_number, destination, start_place)
                    VALUES (%s, %s, %s)
                ''', (customer_number, destination, start_place))
        except EOFError:
            pass  # End of file reached

    # Commit and close
    conn.commit()
    conn.close()
    print("Data synced successfully to the database.")



def get_seating_price(seat_class):
    return SEAT_PRICES.get(seat_class, 0)


def generate_invoice(customer_number):
    connection = create_connection()
    if connection is None:
        print("Error: Could not connect to database.")
        return

    cursor = connection.cursor(dictionary=True)
    try:
        query = """
            SELECT u.full_name, b.card_number, b.cvv, b.exp_date, b.amount_paid
            FROM user u
            JOIN billing b ON u.customer_number = b.customer_number
            WHERE u.customer_number = %s
        """
        cursor.execute(query, (customer_number,))
        invoice = cursor.fetchone()
        
        if invoice:
            # Mask sensitive information
            masked_card_number = "*" * (len(invoice['card_number']) - 4) + invoice['card_number'][-4:]
            masked_cvv = "*" * len(invoice['cvv'])

            print("\n--- Invoice ---")
            print(f"Customer Number: {customer_number}")
            print(f"Full Name      : {invoice['full_name']}")
            print(f"Card Number    : {masked_card_number}")
            print(f"CVV            : {masked_cvv}")
            print(f"Exp. Date      : {invoice['exp_date']}")
            print(f"Amount Paid    : {invoice['amount_paid']}")
            print("------------------------")
        else:
            print(f"No billing information found for customer {customer_number}.")
    except Error as e:
        print(f"Error fetching invoice: {e}")
    finally:
        cursor.close()
        connection.close()




# Seating Management Functions
def display_seating_cli():
    # Define seating sections and total seats per section
    seating_sections = {
        'Business': 5,           # 10 seats in Business
        'Premium Economy': 3,    # 10 seats in Premium Economy
        'Economy': 22             # 10 seats in Economy
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
        print("2. Modify Customer")
        print("3. Delete Customer")
        print("4. Read Customer Data")
        print("5. Search Customer")
        print("6. Exit to Main Menu")

        choice = input("Select an option: ").strip()

        if choice == '1':
            add_customer_cli()
        elif choice == '2':
            modify_customer_cli()
        elif choice == '3':
            delete_customer_cli()
        elif choice == '4':
            read_customer_data_cli()
        elif choice == '5':
            search_customer_cli()
        elif choice == '6':
            break  # Exit to the main menu
        else:
            print("Invalid option, please try again.")


def billing_section():
    print("\n--- Billing ---")
    customer_number = input("Enter your customer number (e.g., ESA1234): ").strip()

    # Fetch customer data from the binary file
    customer = search_customer_in_file(customer_number)
    if not customer:
        print(f"Error: Customer {customer_number} not found in the system.")
        return

    full_name = customer[1]
    print(f"\nCustomer found: {full_name}")

    # Retrieve seat information
    seat_class, seat_number = check_booked_seat(customer_number)

    if not seat_class or not seat_number:
        print("No seat booked for this customer. Please book a seat first.")
        return

    # Calculate amount due
    amount_due = SEAT_PRICES.get(seat_class, 0)
    print(f"Seat Class: {seat_class}")
    print(f"Seat Number: {seat_number}")
    print(f"Total Amount Due: {amount_due}")

    # Collect payment information
    card_number = input("Enter your credit card number: ").strip()
    cvv = input("Enter your CVV: ").strip()
    exp_date_str = input("Enter credit card expiry date (MM/YY): ").strip()

    # Validate expiry date
    try:
        exp_month, exp_year = map(int, exp_date_str.split('/'))
        exp_date = datetime(year=2000 + exp_year, month=exp_month, day=1)
        current_date = datetime.now()

        if exp_date < current_date:
            print("Error: Expiry date has already passed.")
            return
    except ValueError:
        print("Error: Invalid expiry date format. Please enter in MM/YY format.")
        return

    # Mask sensitive information
    masked_card_number = "*" * (len(card_number) - 4) + card_number[-4:]
    masked_cvv = "*" * len(cvv)

    # Confirm payment
    confirm_payment = input("\nConfirm payment? (y/n): ").strip().lower()

    if confirm_payment == 'y':
        print("\nPayment processed successfully!")

        # Store billing information in the database
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            try:
                query = """
                    INSERT INTO billing (customer_number, card_number, cvv, exp_date, amount_paid)
                    VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(query, (customer_number, card_number, cvv, exp_date_str, amount_due))
                connection.commit()
                print("Billing information stored in the database.")
            except Error as e:
                print(f"Error inserting billing data: {e}")
                connection.rollback()
            finally:
                cursor.close()
                connection.close()

        # Generate and display invoice
        generate_invoice(customer_number, full_name, masked_card_number, masked_cvv, exp_date_str, seat_class, seat_number, amount_due)
    else:
        print("Payment canceled.")

def load_customers_from_file(filename):
    # Check if the file exists before opening it
    if not os.path.exists(filename):
        # Return an empty list if the file does not exist
        print(f"Note: '{filename}' does not exist. Creating a new file.")
        with open(filename, 'wb') as file:  # Creates an empty file
            pass
        return []  # Return an empty list of customers
    
    # If the file exists, load the data
    customers = []
    try:
        with open(filename, 'rb') as file:
            while True:
                try:
                    customers.append(pickle.load(file))
                except EOFError:
                    break  # Reached end of file
    except Exception as e:
        print(f"Error loading customers: {e}")
    return customers

def insert_customer_into_db(customer):
    connection = create_connection()
    cursor = connection.cursor()

    customer_number, full_name, age, sex, destination, start_place = customer

    try:
        cursor.execute("""
            INSERT INTO user (customer_number, full_name, age, sex, destination, start_place)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE 
                full_name = VALUES(full_name), 
                age = VALUES(age), 
                sex = VALUES(sex), 
                destination = VALUES(destination), 
                start_place = VALUES(start_place)
        """, (customer_number, full_name, age, sex, destination, start_place))

        connection.commit()
        print(f"Customer {customer_number} inserted/updated successfully.")

    except mysql.connector.Error as e:
        print(f"Error inserting customer: {e}")
        connection.rollback()

    finally:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    customers = load_customers_from_file('customer_data.dat')
    for customer in customers:
        insert_customer_into_db(customer)

def display_available_seats():
    seating_sections = {
        'Business': 10,
        'Premium Economy': 10,
        'Economy': 10
    }
    seats = {'Business': [], 'Premium Economy': [], 'Economy': []}

    for section, total_seats in seating_sections.items():
        for seat_number in range(1, total_seats + 1):
            status = 'Available' if random.choice([True, False]) else 'Booked'
            seats[section].append({'seat': f"{seat_number}", 'status': status})

    print("\n--- Available Seats ---")
    for section, seat_list in seats.items():
        available_seats = [seat['seat'] for seat in seat_list if seat['status'] == 'Available']
        print(f"{section}: {', '.join(available_seats) if available_seats else 'No available seats'}")

def select_seat():
    display_available_seats()
    
    seat_class = input("\nEnter seat class (Business/Premium Economy/Economy): ").strip()
    seat_number = input("Enter seat number: ").strip()
    
    return seat_class, seat_number

def process_billing():
    customer_number = input("Enter your customer number (e.g., ESA1234): ").strip()

    # Fetch customer data from the database
    customer = fetch_customer_data(customer_number)

    if not customer:
        print(f"Error: Customer {customer_number} not found in the database.")
        return

    full_name = customer['full_name']
    print(f"\nCustomer found: {full_name}")

    # Check if customer has a booked seat
    seat_class, seat_number = check_booked_seat(customer_number)

    if not seat_class or not seat_number:
        print("No seat booked for this customer. Please book a seat first.")
        return

    # Calculate amount due
    amount_due = SEAT_PRICES.get(seat_class, 0)
    print(f"Seat Class: {seat_class}")
    print(f"Seat Number: {seat_number}")
    print(f"Total Amount Due: {amount_due}")

    # Collect payment information
    card_number = input("Enter your credit card number: ").strip()
    cvv = input("Enter your CVV: ").strip()
    exp_date = input("Enter credit card expiry date (MM/YY): ").strip()

    # Mask sensitive information
    masked_card_number = "*" * (len(card_number) - 4) + card_number[-4:]
    masked_cvv = "*" * len(cvv)

    # Confirm payment
    confirm_payment = input("\nConfirm payment? (y/n): ").strip().lower()

    if confirm_payment == 'y':
        print("\nPayment processed successfully!")

        # Generate and display invoice
        generate_invoice(customer_number, full_name, masked_card_number, masked_cvv, exp_date, seat_class, seat_number, amount_due)

    else:
        print("Payment canceled.")


def generate_invoice(customer_number, full_name, masked_card_number, masked_cvv, exp_date, seat_class, seat_number, amount_due):
    print("\n--- Invoice ---")
    print(f"Customer Number: {customer_number}")
    print(f"Full Name: {full_name}")
    print(f"Card Number: {masked_card_number}")
    print(f"CVV: {masked_cvv}")
    print(f"Expiration Date: {exp_date}")
    print(f"Seat Class: {seat_class}")
    print(f"Seat Number: {seat_number}")
    print(f"Amount Paid: {amount_due}")
    print("------------------------")

def check_booked_seat(customer_number):
    try:
        with open('seating_data.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) > 3 and row[3] == customer_number and row[2] == 'Booked':
                    return row[0], row[1]  # Return seat_class, seat_number
    except FileNotFoundError:
        print("Error: Seating data file not found.")

    return None, None #return 2 values from a function not having a specific value

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


def create_seating_data(filename):
    if os.path.exists(filename):
        print(f"{filename} already exists. Skipping creation.")
        return
    
    sections = ['Business'] * 5 + ['Premium Economy'] * 6 + ['Economy'] * 19
    seat_labels = [f"{row}{col}" for row in range(1, 31) for col in 'ABCDEF']  # 30 rows with seats A-F

    # Create seating data with random availability
    seating_data = [['Section', 'Seat Number', 'Status', 'Customer Number']]
    for section, seat_number in zip(sections, seat_labels):
        status = random.choice(['Available', 'Booked'])  # Randomly assign status
        seating_data.append([section, seat_number, status, ''])  # Customer Number is empty initially

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

if __name__ == "__main__":
    DATA_FILE = 'customer_data.dat'
    DB_CONFIG = {
        'host': 'localhost',        # Change to your MySQL server address
        'user': 'root',             # Your MySQL username
        'password': 'subhro',     # Your MySQL password
        'database': 'esa'           # Your MySQL database name
    }

    # Sync existing data into the database
    sync_data_to_db(DATA_FILE, DB_CONFIG)

    while True:
        print("\n1. Add Customer")
        print("2. Delete Customer")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            add_customer_cli(DATA_FILE, DB_CONFIG)
        elif choice == '2':
            cust_id = input("Enter customer number to delete: ").strip()
            delete_customer(DATA_FILE, DB_CONFIG, cust_id)
        elif choice == '3':
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Try again.")
