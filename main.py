#CSV Files, Binary Files and MYSQL
#Airline company
import csv
import pickle 


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
            
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    ans = input("Continue (yes/no) : ")


        











