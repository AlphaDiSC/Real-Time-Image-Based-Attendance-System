import datetime as dt
import mysql.connector as torsql
import matplotlib.pyplot as plt

conn=torsql.connect(host='localhost',user='root',passwd='root',database='minorproject', autocommit = True)
cursor=conn.cursor(buffered = True)
if conn.is_connected():
    print('connected')
else:
    print('Connection problem. Try again later.')

def markAttendance(enr):
    today = dt.date.today()
    now = dt.datetime.now()
    time = now.strftime('%H:%M:%S')
    cursor.execute('select shift_id from timetable where sid = {} and start <= "{}" and end > "{}"'.format(enr, time, time))
    shift = cursor.fetchone()
    if shift is None:
        return "Shift Not Started"
    cursor.execute('select entry_time, EDate from attendance where S_id = {} and EDate = "{}" and shift_id = {}'.format(enr, today, int(shift[0])))
    check = cursor.fetchone()
    if(check is None):
        cursor.execute('insert into attendance(S_id, shift_id, entry_time, EDate) values({}, {}, "{}", "{}")'.format(enr,int(shift[0]), time, today))
        conn.commit()
        return "Attendance Marked! ("+str(now)+" )"
    else:
        cursor.execute('select l_id from loiter_time where s_id = {}'.format(enr))
        check_loiter = cursor.fetchone()
        if check_loiter is None :
            add_loiter_time(enr, time)
        else :
            update_loiter_time(enr, time)
        #else:
        return "Attendance Already Marked! ("+str(check[0])+" "+str(check[1])+" )"
        
def IAToday(enr):
    today = dt.date.today()
    cursor.execute("select * from attendance where S_id = {} and edate = '{}'".format(enr, today))
    present = cursor.fetchone()
    if(present is not None):
        return "Marked Present"
    else:
        return "Marked Absent"

def IATotal(enr):
    cursor.execute("select count(distinct edate) from attendance")
    dtotal = cursor.fetchone()
    cursor.execute("Select count(*) from attendance group by S_id having S_id = {}".format(enr))
    denr = cursor.fetchone()
    if denr is None:
        return "Present : 0    Absent : " + str(dtotal[0])+"     Total : "+str(dtotal[0])
    return "Present : "+str(denr[0])+"    Absent : "+str(dtotal[0] - denr[0])+"     Total : "+str(dtotal[0])

def totalpresenttoday():
    today = dt.date.today()
    cursor.execute('select count(*) from attendance where edate = "{}"'.format(today))
    data = cursor.fetchone()
    return "Total Present : "+str(data[0])

def insert_staff():
    a1=input('Enter Fname:       ')
    a2=input('Enter Lname:       ')
    a3=input('Enter Sex:         ')
    a4=input('Enter Department:  ')
    a5=input('Enter Contact_no:  ')
    a6=input('Enter Address:     ')
    cursor.execute('insert into Staff(Fname,Lname,Sex,S_Dept,Contact_no,Address) values("{}","{}","{}","{}","{}","{}")'.format(a1,a2,a3,a4,a5,a6))
    a7=input('Set Password:      ')
    cursor.execute('select MAX(S_id) from Staff')
    staffid=cursor.fetchone()
    cursor.execute("insert into S_Users(User_id, Password) values({},'{}')".format(staffid[0],a7))
    print('\nStaff added successful!\n')
    conn.commit()

def delete_staff():
    a1=int(input('Enter Staff Id:    '))
    cursor.execute('select * from staff where S_id={}'.format(a1))
    data = cursor.fetchone()
    if data==None:
        print('\nInvalid Staff ID\n')
    else:
        cursor.execute('delete from attendance where S_id={}'.format(a1))
        cursor.execute('delete from S_Users where User_id={}'.format(a1))
        cursor.execute('delete from Staff where S_id={}'.format(a1))
        print('\nStaff deleted successfully!\n')
    conn.commit()

def barchart():
    Staff_id = []
    Attendance = []
    cursor.execute('select S_id, count(*) from attendance group by S_id')
    for i in cursor:
        Staff_id.append(i[0])
        Attendance.append(i[1])
    plt.xlabel('Staff ID')
    plt.ylabel('Total Attendance')
    plt.title('Report')
    plt.bar(Staff_id, Attendance, color = 'blue')
    plt.xticks(Staff_id)
    plt.yticks(Attendance)
    plt.show()

def add_loiter_time(enr, start_time):
    cursor.execute('insert into loiter_time(s_id, start) values({}, "{}")'.format(enr, start_time))
    conn.commit()

def update_loiter_time(enr, et):
    cursor.execute('select start from loiter_time where s_id = {}'.format(enr))
    data = cursor.fetchone()
    start_time = data[0]
    et1 = dt.datetime.strptime(et, '%H:%M:%S')
    end_time = dt.timedelta(hours = et1.hour, minutes = et1.minute, seconds = et1.second)
    print(start_time)
    print(end_time)
    lt = end_time - start_time
    lt1 = lt.seconds
    cursor.execute('select loiter_time from attendance where s_id = {}'.format(enr))
    lt_prev = cursor.fetchone()
    lt1 = lt1 + int(lt_prev[0])
    cursor.execute('update attendance set loiter_time = {} where s_id = {}'.format(lt1, enr))
    cursor.execute('delete from loiter_time where s_id = {}'.format(enr))
    conn.commit()

def update_attendance():
    now = dt.datetime.now()
    time = now.strftime('%H:%M:%S')
    cursor.execute('select shift_id from timetable where end = "{}"'.format(time))
    data = cursor.fetchall()
    if data is None:
        print('no shift ended')
        return 
    else:
        for shift in data:
            cursor.execute('select start, end from timetable where shift_id = {}'.format(int(shift[0])))
            dur = cursor.fetchone()
            st = dur[0]
            et = dur[1]
            duration = et.seconds - st.seconds
            today = dt.date.today()
            cursor.execute('select a_id, s_id, entry_time, exit_time, loiter_time from attendance where shift_id = {} and Edate = "{}"'.format(int(shift[0]), today))
            att = cursor.fetchall()
            if att is None:
                return
            for id, s_id, in_time, out_time, l_time in att:
                cursor.execute('select start from loiter_time where s_id = {}'.format(int(s_id)))
                dat = cursor.fetchone()
                if dat is None:
                    cursor.execute('update attendance set exit_time = "{}" where a_id = {}'.format(str(et), int(id)))
                    out_time = et
                else:
                    cursor.execute('update attendance set exit_time = "{}" where a_id = {}'.format(str(dat[0]), int(id)))
                    out_time = dat[0]
                time_attended = out_time.seconds - in_time.seconds - l_time
                if time_attended > duration/2:
                    cursor.execute('update attendance set status = "P" where a_id = {}'.format(int(id)))
            conn.commit()