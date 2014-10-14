import sqlite3

DB = None
CONN = None

def add_project(title, description, max_grade):
    query = """INSERT into Projects (title, description, max_grade) values (?,?,?)"""
    DB.execute(query, (title, description, max_grade))
    CONN.commit()
    print "Successfully added project: %s description: %s max_grade: %s" % (title, description, max_grade)

def make_new_student(first_name, last_name, github):
    query = """INSERT into Students values (?,?,?)"""
    DB.execute(query, (first_name, last_name, github))
    CONN.commit()
    print "Successfully added student: %s %s" % (first_name, last_name)

def get_student_by_project(project):
    query = """SELECT first_name, last_name, title, description FROM Projects JOIN Grades on 
    Projects.title=Grades.project_title JOIN Students on Grades.student_github=Students.github WHERE title = ? """
    DB.execute(query, (project,))
    row = DB.fetchone()
    print """\
Student %s %s
Project info: %s
Description: %s"""%(row[0], row[1], row[2], row[3]) 

def get_grade_by_project(github, project_title):
    query = """SELECT first_name, last_name, project_title, grade from Students JOIN 
    Grades on Students.github=Grades.student_github WHERE github = ? and project_title = ?"""
    DB.execute(query,(github, project_title))
    row = DB.fetchone()
    print """\
Student %s %s 
Project %s
Grade %s """ % (row[0], row[1], row[2], row[3])

def get_all_project_grades(project_title):
    query = """SELECT first_name, last_name, project_title, grade from Students JOIN 
    Grades on Students.github=Grades.student_github WHERE project_title = ?"""
    DB.execute(query,(project_title,))
    row = DB.fetchall()
    print row

#     print """\
# Student %s %s 
# Project %s
# Grade %s """ % (row[0], row[1], row[2], row[3])

def get_student_by_github(github):
    query = """SELECT first_name, last_name, github FROM Students WHERE github = ?"""
    DB.execute(query, (github,))
    row = DB.fetchone()
    return row
# Student: %s %s
# Github account: %s"""%(row[0], row[1], row[2])


def grade_student(student_github, project_title, grade):
    query = """INSERT INTO Grades values (?,?,?)"""
    DB.execute(query,(student_github, project_title, grade))
    CONN.commit()
    print "Successfully added grade %s for student %s for project %s" % (grade, project_title, student_github)

def show_all_grades(student_github):
    query = """SELECT first_name, last_name, project_title, grade FROM Students
    LEFT JOIN Grades ON github = student_github WHERE github = ?"""
    DB.execute(query,(student_github,))
    row = DB.fetchall()
    return row 
  
    # for i in range(len(row)):
    #     print """\
    # Student: %s %s
    # Project: %s
    # Grade: %s""" % (row[i][0], row[i][1], row[i][2], row[i][3])
    #     i+=1

def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect("hackbright.db")
    DB = CONN.cursor()

def main():
    connect_to_db()
    command = None
    while command != "quit":
        input_string = raw_input("HBA Database> ")
        tokens = input_string.split()
        command = tokens[0]
        args = tokens[1:]

        if command == "student":
            print get_student_by_github(*args) 
        elif command == "new_student":
            make_new_student(*args)
        elif command == "project_details":
            get_student_by_project(*args)
        elif command == "new_project":
            add_project(*args)
        elif command == "gimme_grade":
            get_grade_by_project(*args)
        elif command == "give_grade":
            grade_student(*args)
        elif command == "all_grades":
            show_all_grades(*args)
        elif command == "all_project_grades":
            get_all_project_grades(*args)


    CONN.close()

if __name__ == "__main__":
    main()
