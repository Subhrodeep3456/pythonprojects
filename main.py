import pickle
import os

def display_menu():
    print("\nWelcome to the Aircraft Management System")
    print("1. Customers")
    print("2. Seating")
    print("3. Billing")
    print("4. Report")
    print("5. Back to menu")
    print("6. Exit")

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

    customer_data = {
        'full_name': full_name,
        'age': age,
        'sex': sex,
        'destination': destination
    }

    with open('customer_data.bin', 'ab') as file:
        pickle.dump(customer_data, file)

    print("Customer data saved in binary format.")

def search_customer():
    name = input("Enter the name to search: ")
    found = False
    with open('customer_data.bin', 'rb') as file:
        try:
            while True:
                customer = pickle.load(file)
                if customer['full_name'] == name:
                    print("Customer found:", customer)
                    found = True
                    break
        except EOFError:
            if not found:
                print("Customer not found.")

def modify_customer():
    name = input("Enter the name to modify: ")
    customers = []
    found = False
    with open('customer_data.bin', 'rb') as file:
        try:
            while True:
                customer = pickle.load(file)
                if customer['full_name'] == name:
                    print("Current details:", customer)
                    customer['full_name'] = input("Enter new full name: ")
                    customer['age'] = input("Enter new age: ")
                    customer['sex'] = input("Enter new sex (M/F): ")
                    customer['destination'] = input("Enter new destination: ")
                    found = True
                customers.append(customer)
        except EOFError:
            pass

    if found:
        with open('customer_data.bin', 'wb') as file:
            for customer in customers:
                pickle.dump(customer, file)
        print("Customer details updated.")
    else:
        print("Customer not found.")

def delete_customer():
    name = input("Enter the name to delete: ")
    customers = []
    found = False
    with open('customer_data.bin', 'rb') as file:
        try:
            while True:
                customer = pickle.load(file)
                if customer['full_name'] != name:
                    customers.append(customer)
                else:
                    found = True
        except EOFError:
            pass

    if found:
        with open('customer_data.bin', 'wb') as file:
            for customer in customers:
                pickle.dump(customer, file)
        print("Customer record deleted.")
    else:
        print("Customer not found.")

def read_customer_data():
    with open('customer_data.bin', 'rb') as file:
        try:
            while True:
                customer = pickle.load(file)
                print(customer)
        except EOFError:
            pass

def add_more_details():
    name = input("Enter the name to add more details: ")
    customers = []
    found = False
    with open('customer_data.bin', 'rb') as file:
        try:
            while True:
                customer = pickle.load(file)
                if customer['full_name'] == name:
                    print("Current details:", customer)
                    additional_info = input("Enter additional details: ")
                    customer['additional_info'] = additional_info
                    found = True
                customers.append(customer)
        except EOFError:
            pass

    if found:
        with open('customer_data.bin', 'wb') as file:
            for customer in customers:
                pickle.dump(customer, file)
        print("Additional details added.")
    else:
        print("Customer not found.")

def initialize_seats():
    seats = {
        'Business': ['1A', '1B', '1C', '1D', '2A', '2B', '2C', '2D'],
        'Premium Economy': ['3A', '3B', '3C', '3D', '4A', '4B', '4C', '4D'],
        'Economy': ['5A', '5B', '5C', '5D', '6A', '6B', '6C', '6D',
                    '7A', '7B', '7C', '7D', '8A', '8B', '8C', '8D']
    }
    with open('seating_data.bin', 'wb') as file:
        pickle.dump(seats, file)
    print("Seating initialized.")

# Function to display available seats and let user choose one
def handle_seating():
    try:
        with open('seating_data.bin', 'rb') as file:
            seats = pickle.load(file)
    except FileNotFoundError:
        initialize_seats()
        with open('seating_data.bin', 'rb') as file:
            seats = pickle.load(file)

    print("\nAvailable Seats:")
    for class_type, seat_list in seats.items():
        print(f"{class_type} Class: {', '.join(seat_list)}")
    
    selected_class = input("\nChoose class (Business, Premium Economy, Economy): ").strip()
    if selected_class not in seats:
        print("Invalid class selected.")
        return

    selected_seat = input(f"Choose a seat from {selected_class} Class: ").strip().upper()
    if selected_seat in seats[selected_class]:
        seats[selected_class].remove(selected_seat)
        with open('seating_data.bin', 'wb') as file:
            pickle.dump(seats, file)
        print(f"Seat {selected_seat} successfully booked in {selected_class} Class.")
    else:
        print("Seat not available or invalid seat number.")

def main():
    while True:
        display_menu()
        choice = input("Please select an option (1-6): ")
        
        if choice == '1':
            while True:
                display_customer_menu()
                customer_choice = input("Please select an option (1-7): ")
                
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
                    print("Invalid choice. Please select a valid option.")
        elif choice == '2':
            handle_seating()
        elif choice == '3':
            handle_billing()
        elif choice == '4':
            handle_report()
        elif choice == '5':
            print("Returning to menu...")
        elif choice == '6':
            print("Exiting the program. Have a nice day!")
            break
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()
