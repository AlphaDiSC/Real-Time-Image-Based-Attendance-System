import mysql.connector as torsql

conn=torsql.connect(host='localhost',user='root',passwd='root')
if conn.is_connected():
    print('connected')
cursor=conn.cursor()

cursor.execute('drop database if exists minorproject')
cursor.execute('create database minorproject')
cursor.execute('use minorproject')

cursor.execute('create table Staff(S_id int primary key auto_increment,Fname varchar(20),Lname varchar(20),Sex char(1), S_Dept varchar(20), Contact_no char(10) unique, Address varchar(50))')
cursor.execute('ALTER TABLE Staff auto_increment=101')
sql = 'insert into Staff(Fname,Lname,Sex,S_Dept,Contact_no, Address) values(%s,%s,%s,%s,%s,%s)'
val = [('Elon','Musk','M','Admin','9455151545','129-B ABC st'),
        ('Poorab','Sharma','M','Technician','9552150149','23 Hatasha Residency'),
        ('Dharmaraj','Goswami','M','Pharmacist','9565142155','179 Ram Mandir road'),
        ('Harshali', 'Tamba','F','Nurse','9554745549','57 Mahabali Nagar'),
        ('Hriday','Singh','M','Receptionist','9784447747','B-8, Block 3, Aaliyah Residency'),
        ('Shubhrajyoti', 'Ghosh', 'M', 'Speech Pathologist', '9897854547', '123-B Hare Shyam Colony'),
        ('Mrinal','Chaudhary','M','Nurse','9576252235','D-22 Dharampath Colony'),
        ('Veera','Chaturvedi','F','Receptionist','9323325463','34-E, Lal Nagar'),
        ('Aayesha','Mooljani','F','Nurse','9715475486','45X Amrapali Nagar'),
        ('Brijpal','Meena','M','Janitor','9947632458','22-C Andheri Road'),
        ('Ashok','Sanchay','M','IT','9456745643','92-abc Shrinath Colony')]
cursor.executemany(sql, val)

cursor.execute('create table S_Users(User_id int , Password varchar(10), FOREIGN KEY(USER_ID) REFERENCES Staff(S_id))')
sql = 'insert into S_Users(User_id,Password) values(%s,%s)'
val = [(101,'user@101'),
        (102,'user@102'),
        (103,'user@103'),
        (104,'user@104'),
        (105,'user@105'),
        (106,'user@106'),
        (107,'user@107'),
        (108,'user@108'),
        (109,'user@109'),
        (110,'user@110'),
        (111,'user@111')]
cursor.executemany(sql, val)

cursor.execute('create table timetable(shift_id int primary key auto_increment, sid int, start time, end time, foreign key(sid) references Staff(s_id))')
cursor.execute('alter table timetable auto_increment = 1')
sql = 'insert into timetable(sid, start, end) values(%s, %s, %s)'
val = [(101, '22:36:00', '22:38:00'),
        (102, '12:00:00', '18:00:00'),
        (103, '09:00:00', '14:00:00'),
        (104, '08:00:00', '15:00:00'),
        (105, '17:00:00', '23:00:00'),
        (106, '19:56:00', '19:57:00'),
        (107, '11:00:00', '20:00:00'),
        (108, '09:49:00', '09:51:00'),
        (109, '09:00:00', '18:00:00'),
        (110, '10:00:00', '19:00:00'),
        (111, '09:00:00', '18:00:00')]
cursor.executemany(sql, val)

cursor.execute("create table Attendance(a_id int primary key auto_increment, s_id int, shift_id int, entry_time time, exit_time time, edate date, status char(1) default 'A', loiter_time int default '0', foreign key(s_id) references Staff(s_id))")
cursor.execute('alter table Attendance auto_increment = 1')
cursor.execute('create table loiter_time(l_id int primary key auto_increment, s_id int, start time, foreign key(s_id) references Staff(s_id))')
cursor.execute('alter table loiter_time auto_increment = 1')

conn.commit()