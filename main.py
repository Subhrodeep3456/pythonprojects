import pickle
import csv


# Functions for customer management
def add_customer_cli():
    fn = input("Enter full name: ").strip()
    if not fn:  # Exit if input is empty
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

    if fn and age and sex and destination:
        customer = [fn, age, sex, destination]
        with open('customer_data.pkl', 'ab') as file:
            pickle.dump(customer, file)
        print("Customer data saved successfully.")
    else:
        print("Error: All fields must be filled.")


def search_customer_cli():
    name = input("Enter the name to search: ").strip()
    found = False
    if name:
        try:
            with open('customer_data.pkl', 'rb') as file:
                while True:
                    try:
                        customer = pickle.load(file)
                        if customer[0].lower() == name.lower():
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
    name = input("Enter the name to modify: ").strip()
    customers = []
    found = False

    if not name:
        print("Error: Name field is required.")
        return

    try:
        with open('customer_data.pkl', 'rb') as file:
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
        if customer[0].lower() == name.lower():
            new_name = input(f"Enter new full name ({customer[0]}): ") or customer[0]
            new_age = input(f"Enter new age ({customer[1]}): ") or customer[1]
            new_sex = input(f"Enter new sex (M/F) ({customer[2]}): ") or customer[2]
            new_destination = input(f"Enter new destination ({customer[3]}): ") or customer[3]
            customer[0], customer[1], customer[2], customer[3] = new_name, new_age, new_sex, new_destination
            found = True
            break

    if found:
        with open('customer_data.pkl', 'wb') as file:
            for customer in customers:
                pickle.dump(customer, file)
        print("Customer details updated successfully.")
    else:
        print("Customer not found.")


def delete_customer_cli():
    name = input("Enter the name to delete: ").strip()
    customers = []
    found = False

    if not name:
        print("Error: Name field is required.")
        return

    try:
        with open('customer_data.pkl', 'rb') as file:
            while True:
                try:
                    customer = pickle.load(file)
                    if customer[0].lower() != name.lower():
                        customers.append(customer)
                    else:
                        found = True
                except EOFError:
                    break
    except FileNotFoundError:
        print("Error: No customer data found.")
        return

    if found:
        with open('customer_data.pkl', 'wb') as file:
            for customer in customers:
                pickle.dump(customer, file)
        print("Customer record deleted successfully.")
    else:
        print("Customer not found.")


def read_customer_data_cli():
    try:
        with open('customer_data.pkl', 'rb') as file:
            customer_list = []
            while True:
                try:
                    customer = pickle.load(file)
                    customer_list.append(customer)
                except EOFError:
                    break

        if customer_list:
            for customer in customer_list:
                print(customer)
        else:
            print("No customer data available.")
    except FileNotFoundError:
        print("Error: No customer data found.")


def add_more_details_cli():
    name = input("Enter the name to add more details: ").strip()
    customers = []
    found = False

    if not name:
        print("Error: Name field is required.")
        return

    try:
        with open('customer_data.pkl', 'rb') as file:
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
        if customer[0].lower() == name.lower():
            additional_info = input("Enter additional details: ").strip()
            if additional_info:
                customer.append(additional_info)
                found = True
            break

    if found:
        with open('customer_data.pkl', 'wb') as file:
            for customer in customers:
                pickle.dump(customer, file)
        print("Additional details added successfully.")
    else:
        print("Customer not found.")


# Seating Management
def delete_seat_cli():
    section = input("Enter section (Business/Premium Economy/Economy): ").strip()
    seat = input("Enter seat number: ").strip()

    if not section or not seat:
        print("Error: All fields are required.")
        return

    updated_seats = []
    found = False

    try:
        with open('seating_data.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == section and row[1] == seat:
                    if row[2] == 'Booked':
                        row[2] = 'Available'
                        found = True
                    else:
                        print("Seat is already available.")
                updated_seats.append(row)
    except FileNotFoundError:
        print("Error: Seating data not found.")
        return

    if found:
        with open('seating_data.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(updated_seats)
        print("Seat booking canceled successfully.")
    else:
        print("Seat not found or not booked.")


def display_seating_cli():
    seats = {'Business': [], 'Premium Economy': [], 'Economy': []}

    try:
        with open('seating_data.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[2] == 'Available':
                    seats[row[0]].append(row[1])

        for section, seat_list in seats.items():
            print(f"{section}: {', '.join(seat_list[:5])}")  # Display up to 5 available seats
    except FileNotFoundError:
        print("Error: Seating data not found.")


def book_seat_cli():
    section = input("Enter section (Business/Premium Economy/Economy): ").strip()
    seat = input("Enter seat number: ").strip()

    if not section or not seat:
        print("Error: Section and seat number are required.")
        return

    updated_seats = []
    found = False

    try:
        with open('seating_data.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == section and row[1] == seat:
                    if row[2] == 'Available':
                        row[2] = 'Booked'
                        found = True
                    else:
                        print("Error: Seat already booked.")
                updated_seats.append(row)
    except FileNotFoundError:
        print("Error: Seating data not found.")
        return

    if found:
        with open('seating_data.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(updated_seats)
        print("Seat booked successfully.")
    else:
        print("Seat not found or already booked.")


# Main menu for CLI management
def main_menu():
    while True:
        print("\n=== East Sky Airlines Management ===")
        print("1. Customer Management")
        print("2. Seating Management")
        print("3. Exit")
        ch = input("Select an option: ").strip()

        if ch == '1':
            customer_management_menu()
        elif ch == '2':
            seating_management_menu()
        elif ch == '3':
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
        print("6. Add More Details")
        print("7. Back to Main Menu")
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
            add_more_details_cli()
        elif ch == '7':
            break
        else:
            print("Invalid option, please try again.")


# Seating management menu for CLI
def seating_management_menu():
    while True:
        print("\n--- Seating Management ---")
        print("1. Display Seating")
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

import mysql.connector
from mysql.connector import Error

# Connect to MySQL
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',  # Change if needed
            user='root',       # MySQL username
            password='yourpassword',  # MySQL password
            database='airline_management'
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error: {e}")
    return None


# Functions for customer management
def add_customer_mysql():
    connection = create_connection()
    if not connection:
        return

    full_name = input("Enter full name: ").strip()
    if not full_name:
        print("Operation canceled.")
        return

    age = input("Enter age: ").strip()
    if not age.isdigit():
        print("Error: Age must be a number.")
        return

    sex = input("Enter sex (M/F): ").strip().upper()
    if sex not in ['M', 'F']:
        print("Error: Invalid sex entered.")
        return

    destination = input("Enter destination: ").strip()
    if not destination:
        print("Operation canceled.")
        return

    query = "INSERT INTO customers (full_name, age, sex, destination) VALUES (%s, %s, %s, %s)"
    values = (full_name, int(age), sex, destination)

    cursor = connection.cursor()
    try:
        cursor.execute(query, values)
        connection.commit()
        print("Customer data saved successfully.")
    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        connection.close()


def search_customer_mysql():
    connection = create_connection()
    if not connection:
        return

    name = input("Enter the name to search: ").strip()
    if not name:
        print("Operation canceled.")
        return

    query = "SELECT * FROM customers WHERE full_name LIKE %s"
    cursor = connection.cursor()
    try:
        cursor.execute(query, (f"%{name}%",))
        results = cursor.fetchall()
        if results:
            for row in results:
                print(f"Customer: {row}")
        else:
            print("Customer not found.")
    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        connection.close()


def modify_customer_mysql():
    connection = create_connection()
    if not connection:
        return

    name = input("Enter the name to modify: ").strip()
    if not name:
        print("Operation canceled.")
        return

    cursor = connection.cursor()
    query = "SELECT * FROM customers WHERE full_name LIKE %s"
    try:
        cursor.execute(query, (f"%{name}%",))
        customer = cursor.fetchone()
        if customer:
            new_name = input(f"Enter new full name ({customer[1]}): ") or customer[1]
            new_age = input(f"Enter new age ({customer[2]}): ") or str(customer[2])
            if not new_age.isdigit():
                print("Error: Age must be a number.")
                return
            new_sex = input(f"Enter new sex (M/F) ({customer[3]}): ") or customer[3]
            new_destination = input(f"Enter new destination ({customer[4]}): ") or customer[4]

            update_query = "UPDATE customers SET full_name = %s, age = %s, sex = %s, destination = %s WHERE id = %s"
            cursor.execute(update_query, (new_name, int(new_age), new_sex, new_destination, customer[0]))
            connection.commit()
            print("Customer details updated successfully.")
        else:
            print("Customer not found.")
    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        connection.close()


def delete_customer_mysql():
    connection = create_connection()
    if not connection:
        return

    name = input("Enter the name to delete: ").strip()
    if not name:
        print("Operation canceled.")
        return

    query = "DELETE FROM customers WHERE full_name = %s"
    cursor = connection.cursor()
    try:
        cursor.execute(query, (name,))
        if cursor.rowcount > 0:
            connection.commit()
            print("Customer deleted successfully.")
        else:
            print("Customer not found.")
    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        connection.close()


def read_customer_data_mysql():
    connection = create_connection()
    if not connection:
        return

    query = "SELECT * FROM customers"
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        if results:
            for customer in results:
                print(f"Customer: {customer}")
        else:
            print("No customer data available.")
    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        connection.close()


# Seating Management
def display_seating_mysql():
    connection = create_connection()
    if not connection:
        return

    query = "SELECT section, seat_number FROM seating WHERE status = 'Available'"
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        seats = cursor.fetchall()
        if seats:
            for seat in seats:
                print(f"Section: {seat[0]}, Seat: {seat[1]}")
        else:
            print("No available seats.")
    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        connection.close()


def book_seat_mysql():
    connection = create_connection()
    if not connection:
        return

    section = input("Enter section (Business/Premium Economy/Economy): ").strip()
    seat_number = input("Enter seat number: ").strip()

    cursor = connection.cursor()
    query = "SELECT * FROM seating WHERE section = %s AND seat_number = %s AND status = 'Available'"
    try:
        cursor.execute(query, (section, seat_number))
        seat = cursor.fetchone()
        if seat:
            update_query = "UPDATE seating SET status = 'Booked' WHERE id = %s"
            cursor.execute(update_query, (seat[0],))
            connection.commit()
            print("Seat booked successfully.")
        else:
            print("Seat is either already booked or doesn't exist.")
    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        connection.close()


def cancel_seat_booking_mysql():
    connection = create_connection()
    if not connection:
        return

    section = input("Enter section (Business/Premium Economy/Economy): ").strip()
    seat_number = input("Enter seat number: ").strip()

    cursor = connection.cursor()
    query = "SELECT * FROM seating WHERE section = %s AND seat_number = %s AND status = 'Booked'"
    try:
        cursor.execute(query, (section, seat_number))
        seat = cursor.fetchone()
        if seat:
            update_query = "UPDATE seating SET status = 'Available' WHERE id = %s"
            cursor.execute(update_query, (seat[0],))
            connection.commit()
            print("Seat booking canceled successfully.")
        else:
            print("Seat is not booked or doesn't exist.")
    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        connection.close()


# Main menu for CLI management
def main_menu():
    while True:
        print("\n=== East Sky Airlines Management ===")
        print("1. Customer Management")
        print("2. Seating Management")
        print("3. Exit")
        ch = input("Select an option: ").strip()

        if ch == '1':
            customer_management_menu()
        elif ch == '2':
            seating_management_menu()
        elif ch == '3':
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
            add_customer_mysql()
        elif ch == '2':
            search_customer_mysql()
        elif ch == '3':
            modify_customer_mysql()
        elif ch == '4':
            delete_customer_mysql()
        elif ch == '5':
            read_customer_data_mysql()
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
            display_seating_mysql()
        elif ch == '2':
            book_seat_mysql()
        elif ch == '3':
            cancel_seat_booking_mysql()
        elif ch == '4':
            break
        else:
            print("Invalid option, please try again.")


if __name__ == "__main__":
    main_menu()
