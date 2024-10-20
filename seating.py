import mysql.connector
from prettytable import PrettyTable  # To display seats neatly

# Connect to database
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="subhro",
  database="ES"
)

# Create a cursor object to execute SQL queries
mycursor = mydb.cursor()

# Create table if it doesn't exist
mycursor.execute(
    "CREATE TABLE IF NOT EXISTS seating (id INT AUTO_INCREMENT PRIMARY KEY, section VARCHAR(255), seat_number VARCHAR(255), status VARCHAR(255))"
)

# Function to display random available seats
def display_random_available_seats(limit=10):
    print("\nAvailable Seats (Random Selection):\n")
    table = PrettyTable(["Section", "Seat Number", "Status"])
    
    # Fetch random available seats, limit the result to 10-15
    mycursor.execute(f"SELECT * FROM seating WHERE status = 'Available' ORDER BY RAND() LIMIT {limit}")
    seats = mycursor.fetchall()
    
    for row in seats:
        table.add_row([row[1], row[2], row[3]])

    print(table)
    
    return seats  # Return available seats for selection


# Function to allow customer to select a seat
def select_seat():
    available_seats = display_random_available_seats(limit=15)

    if not available_seats:
        print("No available seats.")
        return

    # Prompt customer to choose a seat
    while True:
        section = input("\nEnter section (Business/Premium Economy/Economy): ").strip()
        seat_number = input("Enter seat number: ").strip()

        # Check if the selected seat is available
        for seat in available_seats:
            if seat[1].lower() == section.lower() and seat[2] == seat_number:
                # Update the seat to 'Booked'
                mycursor.execute(
                    "UPDATE seating SET status = 'Booked' WHERE id = %s", (seat[0],)
                )
                mydb.commit()
                print(f"Seat {seat_number} in {section} successfully booked!")
                return
        print("Invalid selection. Please choose a seat from the available options.")

# Main Program Execution
if __name__ == "__main__":
    print("\n=== Welcome to East Sky Airlines ===\n")
    select_seat()
