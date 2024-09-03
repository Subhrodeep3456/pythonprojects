import csv
import pickle
import random

def display_menu():
    print("\nWelcome to the Aircraft Management System")
    print("East Sky Airlines")
    print("1. Customers")
    print("2. Seating")
    print("3. Billing")
    print("4. Report")
    print("5. Exit")

def display_customer_menu():
    print("\nCustomer Management")
    print("1. Add Customer")
    print("2. Search Customer")
    print("3. Modify Customer")
    print("4. Delete Customer")
    print("5. Read Customer Data")
    print("6. Add More Details")
    print("7. Back to Main Menu")

def add_customer():
    full_name = input("Enter full name: ")
    age = input("Enter age: ")
    sex = input("Enter sex (M/F): ")
    destination = input("Enter destination: ")

    with open('customer_data.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([full_name, age, sex, destination])

    print("Customer data saved in CSV format.")

def search_customer():
    name = input("Enter the name to search: ")
    found = False

    with open('customer_data.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == name:
                print("Customer found:", row)
                found = True
                break
    
    if not found:
        print("Customer not found.")

def modify_customer():
    name = input("Enter the name to modify: ")
    customers = []
    found = False

    with open('customer_data.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == name:
                print("Current details:", row)
                row[0] = input("Enter new full name: ")
                row[1] = input("Enter new age: ")
                row[2] = input("Enter new sex (M/F): ")
                row[3] = input("Enter new destination: ")
                found = True
            customers.append(row)

    if found:
        with open('customer_data.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(customers)
        print("Customer details updated.")
    else:
        print("Customer not found.")

def delete_customer():
    name = input("Enter the name to delete: ")
    customers = []
    found = False

    with open('customer_data.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] != name:
                customers.append(row)
            else:
                found = True

    if found:
        with open('customer_data.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(customers)
        print("Customer record deleted.")
    else:
        print("Customer not found.")

def read_customer_data():
    with open('customer_data.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            print(row)

def add_more_details():
    name = input("Enter the name to add more details: ")
    customers = []
    found = False

    with open('customer_data.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == name:
                print("Current details:", row)
                additional_info = input("Enter additional details: ")
                row.append(additional_info)
                found = True
            customers.append(row)

    if found:
        with open('customer_data.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(customers)
        print("Additional details added.")
    else:
        print("Customer not found.")

# Seating functions
def initialize_seats():
    seats = {
        'Business': [f'{row}{seat}' for row in range(1, 9) for seat in 'ABCDEF'],
        'Premium Economy': [f'{row}{seat}' for row in range(9, 19) for seat in 'ABCDEF'],
        'Economy': [f'{row}{seat}' for row in range(19, 30) for seat in 'ABCDEF']
    }
    with open('seating_data.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        for section, seat_list in seats.items():
            for seat in seat_list:
                writer.writerow([section, seat, 'Available'])

    print("Seating data initialized.")

def display_seating():
    seats = {'Business': [], 'Premium Economy': [], 'Economy': []}
    with open('seating_data.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[2] == 'Available':
                seats[row[0]].append(row[1])

    for section, seat_list in seats.items():
        print(f"\n{section}:")
        random_seats = random.sample(seat_list, min(len(seat_list), 5))  # Display up to 5 random seats
        for seat in random_seats:
            print(seat, end=' ')
        print()

def book_seat():
    section = input("Enter section (Business/Premium Economy/Economy): ")
    seat = input("Enter seat number: ")
    updated_seats = []
    found = False

    with open('seating_data.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == section and row[1] == seat:
                if row[2] == 'Available':
                    row[2] = 'Booked'
                    found = True
                else:
                    print("Seat already booked.")
            updated_seats.append(row)

    if found:
        with open('seating_data.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(updated_seats)
        print("Seat booked successfully.")
    else:
        print("Seat not found or already booked.")

def cancel_seat():
    section = input("Enter section (Business/Premium Economy/Economy): ")
    seat = input("Enter seat number: ")
    updated_seats = []
    found = False

    with open('seating_data.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == section and row[1] == seat:
                if row[2] == 'Booked':
                    row[2] = 'Available'
                    found = True
                else:
                    print("Seat is not booked.")
            updated_seats.append(row)

    if found:
        with open('seating_data.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(updated_seats)
        print("Seat booking cancelled.")
    else:
        print("Seat not found or not booked.")

def main():
    initialize_seats()
    while True:
        display_menu()
        choice = input("Enter your choice: ")
        if choice == '1':
            while True:
                display_customer_menu()
                customer_choice = input("Enter your choice: ")
                if customer_choice == '1':
                    add_customer()
                elif customer_choice == '2':
                    search_customer()
                elif customer_choice == '3':
                    modify_customer()
                elif customer_choice == '4':
                    delete_customer()
                elif customer_choice == '5':
                    read_customer_data()
                elif customer_choice == '6':
                    add_more_details()
                elif customer_choice == '7':
                    break
                else:
                    print("Invalid choice. Please try again.")
        elif choice == '2':
            while True:
                print("\nSeating Management")
                print("1. Display Seating")
                print("2. Book Seat")
                print("3. Cancel Seat")
                print("4. Back to Main Menu")
                seating_choice = input("Enter your choice: ")
                if seating_choice == '1':
                    display_seating()
                elif seating_choice == '2':
                    book_seat()
                elif seating_choice == '3':
                    cancel_seat()
                elif seating_choice == '4':
                    break
                else:
                    print("Invalid choice. Please try again.")
        elif choice == '3':
            print("Billing functionality not implemented yet.")
        elif choice == '4':
            print("Report functionality not implemented yet.")
        elif choice == '5':
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
