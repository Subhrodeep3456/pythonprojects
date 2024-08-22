#CSV Files, Binary Files and MYSQL
#Airline company
import csv
import pickle 
# import mysql.connector


print("Trans Oceanic Airlines")
print("Welcome")
print("Menu")
ans = 'yes'
while ans == 'yes':
    print("1. Customers")
    print("2. Seating")
    print("3. Billing")
    print("4. Report")
    print('5. Exit')
    p = int(input("Enter your choice (1-5): "))
    if p == 1:
        f = open('customer.dat','wb')
        a = {}
        an = 'y'
        while an == 'y':
            cn = input("Full name  : ")
            age = int(input("Enter age : "))
            sex = input("Gender : ")
            cl = input("Enter class (Business/Economy/First/Premium Economy): ")
            d = input("Enter destination: ")
            a['Customer Name'] = cn
            a['Age'] = age
            a['Gender'] = sex
            a['Class'] = cl
            pickle.dump(a,f)
            an = input('Continue ? (y/n): ')
        f.close()

        #Function to read the file
        def redreport():
            import pickle
            a = {}
            f = open('customer.dat','rb+')
            try:
                while True:
                    a = pickle.load(f)
                    print(a)
            except EOFError:
                f.close()
            
        #Add records
        def add():
            import pickle
            f = open('customer.dat','wb')
        a = {}
        an = 'y'
        while an == 'y':
            cn = input("Full name  : ")
            age = int(input("Enter age : "))
            sex = input("Gender : ")
            cl = input("Enter class (Business/Economy/First/Premium Economy): ")
            d = input("Enter destination: ")
            a['Customer Name'] = cn
            a['Age'] = age
            a['Gender'] = sex
            a['Class'] = cl
            pickle.dump(a,f)
            an = input('Continue ? (y/n): ')
        f.close()


        def search():
            import pickle 
            p = {}
            found = False
            f = open('customer.dat','rb')
            s = input("Enter customer name : ")
            try:
                print("Searching...")
                while True:
                    s = pickle.load(f)
                    if p['Customer Name'] == s:
                        print(s)
                        found = True
            except EOFError:
                if found == False:
                    print("No records found")
                else:
                    print("Found")
                f.close()
        def modify():
            import pickle
            found = False
            f = open('customer.dat','rb')
            g = open('customer1.dat','wb')
            s = input("Enter customer name : ")
            try:
                while True:
                    p = pickle.load(f)
                    if p['Customer Name'] == s:
                        print("Customer found")
                        p['Age'] = int(input("Enter new age : "))
                        p['Gender'] = input("Enter new gender : ")
                        p['Class'] = input("Enter new class : ")
                        pickle.dump(p,g)
                        found = True
            except EOFError:
                if found == False:
                    print("No records found")
                else:
                    print("Modified")
                f.close()
                g.close()


        def delete():
            import pickle
            found = False
            f = open('customer.dat','rb')
            g = open('customer1.dat','wb')
            s = input("Enter customer name : ")
            try:
                while True:
                    p = pickle.load(f)
                    if p['Customer Name'] == s:
                        print("Customer found")
                        found = True
                    else:
                        pickle.dump(p,g)
            except EOFError:
                if found == False:
                    print("No records found")
                else:
                    print("Deleted")
                f.close()
                g.close()

        answer = 'y'
        while answer == 'y':
            print("1 to view customer details")
            print("2 to add customer details")
            print("3 to search customer details")
            print("4 to modify customer details")
            print("5 to delete customer details")
            print("6 to exit")
            answer = input("Enter your choice : ")
            if answer == '1':
                redreport()
            elif answer == '2':
                add()
            elif answer == '3':
                search()
            elif answer == '4':
                modify()
            elif answer == '5':
                delete()
            elif answer == '6':
                break

    # elif p == 2:
    #     print("Seating")
    #     import csv
    #     with open('seating.csv') as cf:





