#!/usr/bin/python3.6
import hashlib
from random import uniform, randint, choice
import pymysql as mysql
from data.information import STATE, NITS, BRANCHES

PHONE = open('phone.txt')
ADDRESS = open('address.txt')
STUDENT = open('student.txt')
FATHER = open('father.txt')
MOTHER = open('mother.txt')

GENDER = ["male", "female"]
CATEGORY = ["general", "obc", "sc", "st"]

conn = mysql.connect("localhost", "root", "password", "jee")
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS credential")
cursor.execute("DROP TABLE IF EXISTS student")
cursor.execute("DROP TABLE IF EXISTS claims")
cursor.execute("DROP TABLE IF EXISTS college")
cursor.execute("DROP TABLE IF EXISTS branch")

print("Tables dropped...")
cursor.execute(
    "CREATE TABLE student ( id bigint, name varchar(50), father_name varchar(50), mother_name varchar(50), gender varchar(10), state_of_eligibility varchar(20), date_of_birth varchar(15), category varchar(20), pwd varchar(4), applying_for varchar(50), mode_of_exam varchar(20), paper_medium varchar(8), address varchar(80), email varchar(40), phone varchar(12), password varchar(50),photo varchar(60), signature varchar(60), marksheet varchar(60), step_1 int DEFAULT 0, step_2 int DEFAULT 0,step_3 int DEFAULT 0, physics BIGINT DEFAULT NULL, chemistry BIGINT DEFAULT NULL, maths BIGINT DEFAULT NULL, AIR int DEFAULT NULL, upload_verified int DEFAULT NULL, info_verified int DEFAULT NULL, obc_rank int DEFAULT NULL, sc_rank int DEFAULT NULL, st_rank int DEFAULT NULL)")

cursor.execute("CREATE TABLE credential (id varchar(10) ,name varchar(40), password varchar(50))")
cursor.execute("CREATE TABLE branch (id varchar(10) ,branch_name varchar(100))")

cursor.execute(
    "CREATE TABLE claims (id bigint, name varchar(50), subject varchar(15), message varchar(100), resolved int DEFAULT 0, seen_student int DEFAULT 0,seen_admin int DEFAULT 0)")

cursor.execute(
    "CREATE TABLE college (id bigint PRIMARY KEY AUTO_INCREMENT, name varchar(100), branch varchar(100), cutoff_general bigint DEFAULT NULL,cutoff_obc bigint DEFAULT NULL, cutoff_sc bigint DEFAULT NULL, cutoff_st bigint DEFAULT NULL)")

cursor.execute("INSERT INTO jee.credential VALUES('admin','admin','admin')")
conn.commit()
print("Again forming tables...")

for i in range(1, 71):
    ID = i
    name = STUDENT.readline().strip().upper()
    father = FATHER.readline().strip().upper()
    mother = MOTHER.readline().strip().upper()
    gender = choice(GENDER).upper()
    state = choice(STATE).upper()
    date = str(randint(1, 29)) + "-" + str(randint(1, 13)) + "-" + str(randint(1997, 2019))
    category = choice(CATEGORY).upper()
    pwd = choice(["YES", "NO"])
    applying = choice(["JEE(MAIN) PAPER-1 (B.E/B.TECH) ONLY"])
    mode = choice(["PEN PAPER TEST", "COMPUTER TEST"])
    medium = choice(["ENGLISH", "HINDI"])
    address = ADDRESS.readline().strip().upper()
    email = ''.join(name.lower().split()) + str(randint(1000, 10000)) + '@gmail.com'
    phone = PHONE.readline().strip().upper()
    password = "Ahtes8900@"

    upload_complete = randint(0, 1)
    payment_complete = 0

    if upload_complete == 1:
        payment_complete = randint(0, 1)

    photo = ""
    signature = ""
    marksheet = ""

    if upload_complete:
        photo = "/static/student/student.png"
        signature = "/static/student/signature.png"
        marksheet = "/static/student/marksheet.jpeg"

    maths = 0
    chemistry = 0
    physics = 0

    if upload_complete == 1 and payment_complete == 1:
        maths = uniform(-30, 120)
        chemistry = uniform(-30, 120)
        physics = uniform(-30, 120)
    cursor.execute('''INSERT INTO jee.credential VALUES('%s','%s','Ahtes8900@')''' % (str(ID), name))

    cursor.execute(
        "INSERT INTO jee.student VALUES(%d,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',1,%d,%d,%.1f,%.1f,%.1f,NULL,NULL,NULL,NULL,NULL,NULL)" % (
        ID, name, father,
        mother, gender, state, date, category, pwd, applying, mode, medium, address, email,
        phone, password, photo, signature, marksheet, upload_complete, payment_complete, maths, chemistry, physics))

print("Inserted student data...")

for branch in BRANCHES:
    cursor.execute('''INSERT INTO jee.branch(branch_name) VALUES('%s')''' % branch)

for nit in NITS:
    for branch in BRANCHES:
        cursor.execute(
            '''INSERT INTO jee.college(name,branch,cutoff_general,cutoff_obc,cutoff_sc,cutoff_st) VALUES('%s','%s',%d,%d,%d,%d)''' % (
            nit, branch, uniform(80, 250), uniform(70, 150), uniform(0, 60), uniform(-20, 30)))

print("Inserted college data...")
cursor.execute('''SET SQL_SAFE_UPDATES = 0;''')
print("END")
conn.commit()
conn.close()

# all data verified

# for i in range(1,101):
# 	ID = i
# 	name = STUDENT.readline().strip().upper()
# 	father = FATHER.readline().strip().upper()
# 	mother = MOTHER.readline().strip().upper()
# 	gender = choice(GENDER).upper()
# 	state =  choice(STATE).upper()
# 	date = str(randint(1,29))+"-"+str(randint(1,13))+"-"+str(randint(1997,2019))
# 	category = choice(CATEGORY).upper()
# 	pwd = choice(["YES","NO"])
# 	applying = choice(["JEE(MAIN) PAPER-1 (B.E/B.TECH) ONLY"])
# 	mode = choice(["PEN PAPER TEST","COMPUTER TEST"])
# 	medium = choice(["ENGLISH","HINDI"])
# 	address = ADDRESS.readline().strip().upper()
# 	email = ''.join(name.lower().split())+str(randint(1000,10000))+choice(['@gmail.com','@yahoo.com','@hotmail.com'])
# 	phone = PHONE.readline().strip().upper()
# 	password = hashlib.md5(b"Ahtes8900@").hexdigest()
#
# 	photo = "/static/student/student.png"
# 	signature = "/static/student/signature.png"
# 	marksheet = "/static/student/marksheet.jpeg"
#
# 	maths = uniform(-30,120)
# 	chemistry = uniform(-30,120)
# 	physics = uniform(-30,120)
#
# 	cursor.execute('''INSERT INTO jee.credential VALUES('%s','%s','Ahtes8900@')'''%(str(ID),name))
#
# 	cursor.execute("INSERT INTO jee.student VALUES(%d,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',1,%d,%d,%.1f,%.1f,%.1f,NULL,1,1,NULL,NULL,NULL)"%(ID,name,father,
# 			mother,gender,state,date,category,pwd,applying, mode,medium,address,email,
# 			phone,password,photo,signature,marksheet,1,1,maths,chemistry,physics))
#
# print("Inserted student data...")
#
# for nit in NITS:
# 	for branch in BRANCHES:
# 		cursor.execute('''INSERT INTO jee.college(name,branch,cutoff_general,cutoff_obc,cutoff_sc,cutoff_st) VALUES('%s','%s',%d,%d,%d,%d)'''%(nit,branch,uniform(80,250),uniform(70,150),uniform(0,60),uniform(-20,30)))
#
# print("Inserted college data...")
# print("END")
# conn.commit()
# conn.close()
