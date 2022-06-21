import Functions as fn
import mysql.connector as torsql
conn=torsql.connect(host='localhost',user='root',passwd='root',database='minorproject')
cursor=conn.cursor()
print(''' 

░█████╗░████████╗████████╗███████╗███╗░░██╗██████╗░░█████╗░███╗░░██╗░█████╗░███████╗
██╔══██╗╚══██╔══╝╚══██╔══╝██╔════╝████╗░██║██╔══██╗██╔══██╗████╗░██║██╔══██╗██╔════╝
███████║░░░██║░░░░░░██║░░░█████╗░░██╔██╗██║██║░░██║███████║██╔██╗██║██║░░╚═╝█████╗░░
██╔══██║░░░██║░░░░░░██║░░░██╔══╝░░██║╚████║██║░░██║██╔══██║██║╚████║██║░░██╗██╔══╝░░
██║░░██║░░░██║░░░░░░██║░░░███████╗██║░╚███║██████╔╝██║░░██║██║░╚███║╚█████╔╝███████╗
╚═╝░░╚═╝░░░╚═╝░░░░░░╚═╝░░░╚══════╝╚═╝░░╚══╝╚═════╝░╚═╝░░╚═╝╚═╝░░╚══╝░╚════╝░╚══════╝

███╗░░░███╗░█████╗░███╗░░██╗░█████╗░░██████╗░███████╗███╗░░░███╗███████╗███╗░░██╗████████╗
████╗░████║██╔══██╗████╗░██║██╔══██╗██╔════╝░██╔════╝████╗░████║██╔════╝████╗░██║╚══██╔══╝
██╔████╔██║███████║██╔██╗██║███████║██║░░██╗░█████╗░░██╔████╔██║█████╗░░██╔██╗██║░░░██║░░░
██║╚██╔╝██║██╔══██║██║╚████║██╔══██║██║░░╚██╗██╔══╝░░██║╚██╔╝██║██╔══╝░░██║╚████║░░░██║░░░
██║░╚═╝░██║██║░░██║██║░╚███║██║░░██║╚██████╔╝███████╗██║░╚═╝░██║███████╗██║░╚███║░░░██║░░░
╚═╝░░░░░╚═╝╚═╝░░╚═╝╚═╝░░╚══╝╚═╝░░╚═╝░╚═════╝░╚══════╝╚═╝░░░░░╚═╝╚══════╝╚═╝░░╚══╝░░░╚═╝░░░

░██████╗██╗░░░██╗░██████╗████████╗███████╗███╗░░░███╗
██╔════╝╚██╗░██╔╝██╔════╝╚══██╔══╝██╔════╝████╗░████║
╚█████╗░░╚████╔╝░╚█████╗░░░░██║░░░█████╗░░██╔████╔██║
░╚═══██╗░░╚██╔╝░░░╚═══██╗░░░██║░░░██╔══╝░░██║╚██╔╝██║
██████╔╝░░░██║░░░██████╔╝░░░██║░░░███████╗██║░╚═╝░██║
╚═════╝░░░░╚═╝░░░╚═════╝░░░░╚═╝░░░╚══════╝╚═╝░░░░░╚═╝                   
    ''')

t = 1
while (t != 0):
    while (True):
        a = int(input('User id:     '))
        b = input('Password:    ')
        cursor.execute("Select * from S_Users where User_id={} and Password='{}'".format(a, b))
        data = cursor.fetchone()
        if data is None:
            print('\nIncorrect User id or password. Try again.\n')
            continue
        else:
            print('\nLogin successful\n')
        cursor.execute('Select Fname,S_Dept from Staff where S_id={}'.format(a))
        st = cursor.fetchone()
        if st[1] == "Admin":
            print("Welcome " + st[0] + "!")
            while True:
                print('''
                                                ************MENU************

                                                1 : Insert new Staff
                              		            2 : Delete existing Staff
                              		            3 : Attendance Chart 
                              		            4 : Total Present Today
                              		            5 : Exit
                              		              
                                                *****************************
                    ''')
                choice = int(input('\nEnter choice: '))

                if choice == 1:
                    fn.insert_staff()
                elif choice == 2:
                    fn.delete_staff()
                elif choice == 3:
                    fn.barchart()
                elif choice == 4:
                    print(fn.totalpresenttoday())
                elif choice == 5:
                    print('Bye')
                    break
                else:
                    print('Invalid Choice')

        else:
            print("Welcome " + st[0] + "!")
            while True:
                print('''
                                                ************MENU************

                                                  1 : Check Today's Attendance
                              		              2 : Check Total Attendance
                              		              3 : Exit

                                                *****************************
                    ''')
                choice = int(input('\nEnter choice: '))

                if choice == 1:
                    print(fn.IAToday(a))
                elif choice == 2:
                    s = fn.IATotal(a)
                    print(s)
                elif choice == 3:
                    print('Bye')
                    break
                else:
                    print('Invalid Choice')