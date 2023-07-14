import subprocess as sp
import pymysql
import pymysql.cursors
import datetime


def deleteTuple():
    try:
        table = input("Table to delete from: ")

        # ----------
        # primary key nikalo
        try:
            q0 = "SELECT K.COLUMN_NAME FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS T JOIN INFORMATION_SCHEMA.KEY_COLUMN_USAGE K ON K.CONSTRAINT_NAME = T.CONSTRAINT_NAME WHERE K.TABLE_NAME='%s' AND T.CONSTRAINT_TYPE = 'PRIMARY KEY' LIMIT 1;" % (
                table)
            cur.execute(q0)
            q0ans0 = cur.fetchall()    # q0ans is name of primary key
            # print(q0ans0)
            q0ans1 = q0ans0[0]["COLUMN_NAME"]
            # print(q0ans1)
            # print()
            # row is value of primary key
            row = input(q0ans1 + " to be deleted: ")
            # print(row)
            # print(table)
            q0typequery = "SELECT DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = '%s' AND COLUMN_NAME = '%s';" % (
                table, q0ans1)
            cur.execute(q0typequery)
            q0type0 = cur.fetchall()
            # q0type is datatype of primary key
            q0type = q0type0[0]["DATA_TYPE"]
            # print(q0type)

        except Exception as e:
            con.rollback()
            print()
            print("Failed to get primary key of given table!!")
            print()
            print(">>>>>>>>>>>>>>", e)
            print()
            return
        # -----------

        if (q0type == 'int'):
            rowint = int(row)
            query = "DELETE FROM %s WHERE %s = %d;" % (table, q0ans1, rowint)
            print()
            print(query)
            print()

        else:
            query = "DELETE FROM %s WHERE %s = '%s';" % (table, q0ans1, row)
            print()
            print(query)
            print()

        cur.execute(query)
        con.commit()

    except Exception as e:
        con.rollback()
        print()
        print("Failed to get required details")
        print()
        print(">>>>>>>>>>>>>>", e)

    return


def update():
    try:
        what = input("Do you want to update a number or a string?: ")
        table = input("Table to update: ")
        column = input("Column to update: ")

        # ----------
        # primary key nikalo
        try:
            q0 = "SELECT K.COLUMN_NAME FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS T JOIN INFORMATION_SCHEMA.KEY_COLUMN_USAGE K ON K.CONSTRAINT_NAME = T.CONSTRAINT_NAME WHERE K.TABLE_NAME='%s' AND T.CONSTRAINT_TYPE = 'PRIMARY KEY' LIMIT 1;" % (
                table)
            cur.execute(q0)
            q0ans0 = cur.fetchall()    # q0ans is name of primary key
            print(q0ans0)
            q0ans1 = q0ans0[0]["COLUMN_NAME"]
            print(q0ans1)
            # print()
            # row is value of primary key
            row = input(q0ans1 + " to be updated: ")
            print(row)
            print(table)
            q0typequery = "SELECT DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = '%s' AND COLUMN_NAME = '%s';" % (
                table, q0ans1)
            cur.execute(q0typequery)
            q0type0 = cur.fetchall()  # q0type is datatype of primary key
            q0type = q0type0[0]["DATA_TYPE"]
            print(q0type)

        except Exception as e:
            con.rollback()
            print()
            print("Failed to get primary key of given table!!")
            print()
            print(">>>>>>>>>>>>>>", e)
            print()
            return
        # -----------

        new_value = input("Updated value: ")
        if (what == 'number'):
            new_number = int(new_value)

        if (q0type == 'int'):
            rowint = int(row)
            # print(rowint)
            # print(type(rowint))
            if (what == 'number'):
                query = "UPDATE %s SET %s = '%d' WHERE %s = %d;" % (
                    table, column, new_number, q0ans1, rowint)
            else:
                query = "UPDATE %s SET %s = '%s' WHERE %s = %d;" % (
                    table, column, new_value, q0ans1, rowint)

            print(query)

        else:
            if (what == 'number'):
                query = "UPDATE %s SET %s = '%d' WHERE %s = '%s';" % (
                    table, column, new_number, q0ans1, row)
            else:
                query = "UPDATE %s SET %s = '%s' WHERE %s = '%s';" % (
                    table, column, new_value, q0ans1, row)

            print(query)

        cur.execute(query)
        con.commit()
    except Exception as e:
        con.rollback()
        print("Failed to get required details")
        print(">>>>>>>>>>>>>>", e)

    return


def fmratio():
    try:
        query = "SELECT t1.girls/t2.boys AS gender_ratio FROM ( SELECT count(*) AS girls FROM students WHERE gender = 'F') as t1, (SELECT count(*) AS boys FROM students WHERE gender = 'M') AS t2 ;"
        cur.execute(query)
        answer = cur.fetchall()
        print(answer)
        con.commit()

        print("Query fetched!")

    except Exception as e:
        con.rollback()
        print("Failed to get required details")
        print(">>>>>>>>>>>>>>", e)

    return


def above_avg_cgpa():
    try:
        dept = input("Department Name: ")
        gender = input("Gender(Y/M): ")
        query = "SELECT count(*) FROM students AS S join stud_dept AS SD on S.roll_no = SD.stud_id WHERE cgpa > ALL (SELECT AVG(cgpa) FROM students) AND SD.dept_name = '%s' AND S.gender = '%c';" % (dept, gender)
        print(query)
        cur.execute(query)
        answer = cur.fetchall()
        print(answer)
        con.commit()

        print("Query fetched!")

    except Exception as e:
        con.rollback()
        print("Failed to get required details")
        print(">>>>>>>>>>>>>>", e)

    return


def std_more_than_avg():
    try:
        query = "SELECT * FROM subjects WHERE no_of_students > ALL (SELECT AVG(no_of_students) FROM subjects);"
        print(query)
        cur.execute(query)
        answer = cur.fetchall()
        print(answer)
        con.commit()

        print("Query fetched!")

    except Exception as e:
        con.rollback()
        print("Failed to get required details")
        print(">>>>>>>>>>>>>>", e)

    return


def searchDept():
    try:
        input_name = input("Name : ")
        query = "SELECT * FROM department WHERE dept_name = '%s';" % (
            input_name)
        print(query)
        cur.execute(query)
        answer = cur.fetchall()
        if (answer == 'NULL'):
            print("No Department Found")

        else:
            print(answer)
            print("Department Found!")

        con.commit()

        # print("Student Found!")

    except Exception as e:
        con.rollback()
        print("Failed to find department")
        print(">>>>>>>>>>>>>>", e)

    return


def searchProf():
    try:
        letter = input("First letter : ")
        # query = "SELECT * FROM professors WHERE prof_name LIKE \"'%c'%\";" % (
        # letter)
        query = f"SELECT * FROM professors WHERE prof_name LIKE '{letter}%'"
        print(query)
        cur.execute(query)
        answer = cur.fetchall()
        if (answer == 'NULL'):
            print("No Professor Found")

        else:
            print(answer)
            print("Professor Found!")

        con.commit()

        # print("Student Found!")

    except Exception as e:
        con.rollback()
        print("Failed to find professor")
        print(">>>>>>>>>>>>>>", e)

    return


def searchStd():
    try:
        letter = input("First letter : ")[0]
    #     listOfChars = list()
    # for character in letter:
    #     listOfChars.append(character)
    # letter2 = letter[0]
    # print(type(letter2))
        query = f"SELECT * FROM professors WHERE prof_name LIKE '{letter}%'"
        print(query)
        cur.execute(query)
        answer = cur.fetchall()
        if (answer == 'NULL'):
            print("No Student Found")

        else:
            print(answer)
            print("Student Found!")

        con.commit()

        # print("Student Found!")

    except Exception as e:
        con.rollback()
        print("Failed to find student")
        print(">>>>>>>>>>>>>>", e)

    return


def maxEquip():
    try:
        query = "SELECT sport_name FROM equipment WHERE quantity IN (SELECT MAX(quantity) FROM equipment);"
        print(query)
        cur.execute(query)
        answer = cur.fetchall()
        print(answer)
        con.commit()

        print("Sports with max equipment fetched!")

    except Exception as e:
        con.rollback()
        print("Failed to get required details")
        print(">>>>>>>>>>>>>>", e)

    return


def lhostel():
    try:
        query = "SELECT H.hostel_name FROM hostel AS H WHERE H.no_of_students IN (SELECT MIN(no_of_students) FROM hostel);"
        print(query)
        cur.execute(query)
        answer = cur.fetchall()
        print(answer)
        con.commit()

        print("Least populated hostel fetched!")

    except Exception as e:
        con.rollback()
        print("Failed to get required details")
        print(">>>>>>>>>>>>>>", e)

    return


def amount():
    try:
        query = "SELECT sum(salary) FROM professors;"
        print(query)
        cur.execute(query)
        answer = cur.fetchall()
        print(answer)
        con.commit()

        print("Total salary fetched!")

    except Exception as e:
        con.rollback()
        print("Failed to get required details")
        print(">>>>>>>>>>>>>>", e)

    return


def avgStd():
    try:
        query = "SELECT avg(no_of_students) FROM subjects;"
        print(query)
        cur.execute(query)
        answer = cur.fetchall()
        print(answer)
        con.commit()

        print("Avg no. of fetched!")

    except Exception as e:
        con.rollback()
        print("Failed to get required details")
        print(">>>>>>>>>>>>>>", e)

    return


def labSub():
    try:
        query = "SELECT count(*) FROM subjects WHERE lab = 'y';"
        print(query)
        cur.execute(query)
        answer = cur.fetchall()
        print(answer)
        con.commit()

        print("Subjects having lab fetched!")

    except Exception as e:
        con.rollback()
        print("Failed to get required details")
        print(">>>>>>>>>>>>>>", e)

    return


def studgt30():
    try:
        query = "SELECT course_id, subject_name FROM subjects WHERE subjects.no_of_students > 30;"
        print(query)
        cur.execute(query)
        answer = cur.fetchall()
        print(answer)
        con.commit()

        print("Subjects having more than 30 students fetched!")

    except Exception as e:
        con.rollback()
        print("Failed to get required details")
        print(">>>>>>>>>>>>>>", e)

    return


def nonEquipSports():
    try:
        query = "SELECT S.sport_name FROM sports as S left join equipment as E on S.sport_name = E.sport_name WHERE E.quantity is not NULL and E.quantity > 0;"
        print(query)
        cur.execute(query)
        answer = cur.fetchall()
        print(answer)
        con.commit()

        print("Sports with no equipment fetched!")

    except Exception as e:
        con.rollback()
        print("Failed to fetch sport details")
        print(">>>>>>>>>>>>>>", e)

    return


def deptBuilding():
    try:
        building_no = int(input("Buildin No: "))
        query = "SELECT * FROM department WHERE building_no = '%d';" % (
            building_no)
        print(query)
        cur.execute(query)
        answer = cur.fetchall()
        print(answer)
        con.commit()

        print("Department Details fetched!")

    except Exception as e:
        con.rollback()
        print("Failed to fetch department details")
        print(">>>>>>>>>>>>>>", e)

    return


def profDetails():
    try:
        prof_id = int(input("Professor ID: "))
        query = "SELECT * FROM professors AS P WHERE P.prof_id = '%d';" % (
            prof_id)
        query1 = "SELECT * FROM prof_dept WHERE prof_id = '%d';" % (prof_id)
        print(query)
        print(query1)
        cur.execute(query)
        answer = cur.fetchall()
        print(answer)
        print()
        cur.execute(query1)
        answer = cur.fetchall()
        print(answer)
        print()
        con.commit()

        print("Professor Details fetched!")

    except Exception as e:
        con.rollback()
        print("Failed to fetch professor details")
        print(">>>>>>>>>>>>>>", e)

    return


def studentDetails():
    try:
        rollno = int(input("Roll No: "))
        query = "SELECT * FROM students WHERE roll_no = '%d';" % (rollno)
        query1 = "SELECT * FROM stud_dept WHERE stud_id = '%d';" % (rollno)
        print(query)
        print(query1)
        cur.execute(query)
        answer = cur.fetchall()
        print(answer)
        print()
        cur.execute(query1)
        answer = cur.fetchall()
        print(answer)
        print()
        con.commit()

        print("Student Details fetched!")

    except Exception as e:
        con.rollback()
        print("Failed to fetch student details")
        print(">>>>>>>>>>>>>>", e)

    return


def equipDetails():
    try:
        sport = input("Enter Sport Name: ")
        query = "SELECT * FROM equipment as E WHERE E.sport_name = '%s';" % (
            sport)
        print(query)
        cur.execute(query)
        answer = cur.fetchall()
        print(answer)
        con.commit()

        print("Equipment Details fetched!")

    except Exception as e:
        con.rollback()
        print("Failed to fetch equipment details")
        print(">>>>>>>>>>>>>>", e)

    return


def allEquip():
    try:
        query = "SELECT * FROM equipment;"
        print(query)
        cur.execute(query)
        answer = cur.fetchall()
        print(answer)
        con.commit()

        print("Equipment Details fetched!")

    except Exception as e:
        con.rollback()
        print("Failed to fetch equipment details")
        print(">>>>>>>>>>>>>>", e)

    return


def subDetails():
    try:
        sub = int(input("Course_id : "))
        query = "SELECT * FROM subjects WHERE course_id = '%d';" % (sub)
        print(query)
        cur.execute(query)
        answer = cur.fetchall()
        print(answer)
        con.commit()

        print("Details fetched!")

    except Exception as e:
        con.rollback()
        print("Failed to fetch subject details")
        print(">>>>>>>>>>>>>>", e)

    return


def newClub():
    # what if no of members < no of cords and if cords > 3 entered
    try:
        row = {}
        print("Enter Club details: ")
        row["name"] = input("Name: ")
        row["no_of_members"] = int(input("No. of members: "))
        no_of_coords = int(input("No. of Coordinators (max 3): "))
        row["coord1"] = input("Coord 1 : ")
        if (no_of_coords > 1):
            row["coord2"] = input("Coord 2 : ")
        else:
            row["coord2"] = "NULL"
        if (no_of_coords > 2):
            row["coord3"] = input("Coord 3 : ")
        else:
            row["coord3"] = "NULL"

        query = " INSERT INTO clubs values ('%s', '%d', '%s','%s','%s')" % (
            row["name"], row["no_of_members"], row["coord1"], row["coord2"], row["coord3"])
        print(query)
        cur.execute(query)
        con.commit()

        print("Added new club!")

    except Exception as e:
        con.rollback()
        print("Failed to add new club")
        print(">>>>>>>>>>>>>>", e)

    return


def recruitProf():
    try:
        row = {}
        print("Enter new proff's details: ")
        # name = (input("Name (Fname Minit Lname): ")).split(' ')
        name = (input("Name (Fname Minit Lname): "))
        # row["Fname"] = name[0]
        # row["Minit"] = name[1]
        # row["Lname"] = name[2]
        row["Prof_id"] = int(input("Prof_id: "))
        row["Sex"] = input("Sex(F/M): ")
        row["Salary"] = int(input("Salary: "))
        row["Bdate"] = input("Birth Date (YYYY-MM-DD): ")
        row["Dept"] = (input("Department: "))
        row["course_id"] = int(input("course_id: "))
        row["super_prof_id"] = input("super_prof_id: ")
        # derive age
        bdate = row["Bdate"]
        blist = bdate.split('-')
        dob = datetime.date(int(blist[0]), int(blist[1]), int(blist[2]))
        today = datetime.date.today()
        age = today.year - dob.year - \
            ((today.month, today.day) < (dob.month, dob.day))
        query = " INSERT INTO professors values ('%d','%s','%c','%d','%s','%d',NULL)" % (
            row["Prof_id"], name, row["Sex"], row["Salary"], row["Bdate"], int(age))
        query1 = " INSERT INTO prof_dept values ('%d','%s')" % (
            row["Prof_id"], row["Dept"])
        query2 = " INSERT INTO subject_prof_id values ('%d','%s')" % (
            row["course_id"], row["Prof_id"])
        print()
        print(query)
        print(query1)
        print(query2)
        cur.execute(query)
        cur.execute(query1)
        cur.execute(query2)
        con.commit()

        print("Added Proff to the Database!")

    except Exception as e:
        con.rollback()
        print("Failed to insert into database")
        print(">>>>>>>>>>>>>", e)

    return


def admitAStudent():

    try:
        row = {}
        print("Enter new student's details: ")
        name = (input("Name (Fname Minit Lname): ")).split(' ')
        # name = (input("Name (Fname Minit Lname): "))
        row["Fname"] = name[0]
        try:
            row["Minit"] = name[1]

        except:
            row["Minit"] = 'NULL'

        try:
            row["Lname"] = name[2]

        except:
            row["Lname"] = 'NULL'    
        row["Roll_No"] = int(input("Roll No: "))
        # row["CGPA"] = input("CGPA: ")
        row["Sex"] = input("Sex(F/M): ")
        row["Batch"] = input("Batch: ")
        row["Bdate"] = input("Birth Date (YYYY-MM-DD): ")
        row["Email"] = (input("Email: "))
        row["Dept"] = (input("Department: "))
        row["Hostel"] = input("Hostel: ")
        row["Password"] = (input("Password: "))

        # derive age
        bdate = row["Bdate"]
        blist = bdate.split('-')
        dob = datetime.date(int(blist[0]), int(blist[1]), int(blist[2]))
        today = datetime.date.today()
        age = today.year - dob.year - \
            ((today.month, today.day) < (dob.month, dob.day))
        query = " INSERT INTO students values ('%d', NULL,'%c','%s',%d,'%s','%s','%s','%s','%s','%s','%s')" % (
            row["Roll_No"], row["Sex"], row["Batch"], age, row["Email"], row["Bdate"], row["Fname"], row["Minit"], row["Lname"], row["Password"], row["Hostel"])
        # query = " INSERT INTO students values ('%d', NULL, '%s', '%s','%d', '%s', '%s', '%s','%s','%s')" % (
        #     row["Roll_No"], row["Sex"], row["Batch"], int(age), row["Email"], row["Bdate"], name, row["Password"], row["Hostel"])
        query1 = " INSERT INTO stud_dept values ('%d','%s')" % (
            row["Roll_No"], row["Dept"])
        print()
        print(query)
        print(query1)
        cur.execute(query)
        cur.execute(query1)
        con.commit()

        print()
        print("Added Student to the Database!")
        print()

    except Exception as e:
        con.rollback()
        print()
        print("Failed to insert into database")
        print()
        print(">>>>>>>>>>>>>", e)

    return


def dispatch(ch):
    """
    Function that maps helper functions to option entered
    """

    if (ch == 1):
        admitAStudent()
    elif (ch == 2):
        recruitProf()
    elif (ch == 3):
        subDetails()
    elif (ch == 4):
        newClub()
    elif (ch == 5):
        allEquip()
    elif (ch == 6):
        equipDetails()
    elif (ch == 7):
        studentDetails()
    elif (ch == 8):
        profDetails()
    elif (ch == 9):
        deptBuilding()
    elif (ch == 10):
        nonEquipSports()
    elif (ch == 11):
        studgt30()
    elif (ch == 12):
        labSub()
    elif (ch == 13):
        avgStd()
    elif (ch == 14):
        amount()
    elif (ch == 15):
        lhostel()
    elif (ch == 16):
        maxEquip()
    elif (ch == 17):
        searchStd()
    elif (ch == 18):
        searchProf()
    elif (ch == 19):
        searchDept()
    elif (ch == 20):
        std_more_than_avg()
    elif (ch == 21):
        above_avg_cgpa()
    elif (ch == 22):
        fmratio()
    elif (ch == 23):
        update()
    elif (ch == 24):
        deleteTuple()
    else:
        print("Error: Invalid Option")


# Global
while (1):
    tmp = sp.call('clear', shell=True)

    # Can be skipped if you want to hardcode username and password
    username = input("Username: ")
    password = input("Password: ")

    try:
        # Set db name accordingly which have been create by you
        # Set host to the server's address if you don't want to use local SQL server
        con = pymysql.connect(host='localhost',
                              port=3306,
                              user=username,
                              password=password,
                              db='pro',
                              cursorclass=pymysql.cursors.DictCursor)
        tmp = sp.call('clear', shell=True)

        if (con.open):
            print("Connected")
        else:
            print("Failed to connect")

        tmp = input("Enter any key to CONTINUE>")

        with con.cursor() as cur:
            while (1):
                tmp = sp.call('clear', shell=True)
                # Here taking example of Employee Mini-world
                print("1. new student")  # Hire an Employee
                print("2. new proff")  # Fire an Employee
                print("3. get details of a subject")  # Promote Employee
                print("4. insert new club")  # Employee Statistics
                print("5. get equipment details for all sports")
                print("6. get equipment details for a sport")
                print("7. get a student details")
                print("8. get a proff details")
                print("9. Get details about all the departments in a building")
                print("10. Name of all sports having non-zero equipment")
                print("11. subjects having more than 30 students enrolled")
                print("12. Number of subjects having labs")
                print("13. Average number of students per subject")
                print("14. Total amount spent by university on professors’ salary")
                print("15. Least populated hostel")
                print("16. Sport with maximum equipment")
                print("17. Search for students using first letter of their name")
                print("18. Search for professors using first letter of their name")
                print("19. Search for departments by their name")
                print(
                    "20. Number of students enrolled for the subjects having more than average number of students.")
                print(
                    "21. Number of girls and boys having above average CGPA in mechanical department")
                print("22. Student female is to male ratio")
                print("23. update")
                print("24. delete tuple")
                # print("6. Logout")
                ch = int(input("Enter choice> "))
                tmp = sp.call('clear', shell=True)
                # if ch == 6:
                #     exit()
                # else:
                dispatch(ch)
                tmp = input("Enter any key to CONTINUE>")

    except Exception as e:
        tmp = sp.call('clear', shell=True)
        print(e)
        print("Connection Refused: Either username or password is incorrect or user doesn't have access to database")
        tmp = input("Enter any key to CONTINUE>")
