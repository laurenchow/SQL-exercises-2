from flask import Flask, render_template, request
import hackbright_app


app = Flask(__name__)

@app.route("/")
def get_github():
    return render_template("get_github.html")


@app.route("/student")
def get_student():
    hackbright_app.connect_to_db()
    student_github = request.args.get("github") #fancy dictionary 
    row = hackbright_app.get_student_by_github(student_github)
    grades = hackbright_app.show_all_grades(student_github)
    html = render_template("student_info.html", first_name=row[0], 
       last_name=row[1], github=row[2], grades=grades)
    return html

@app.route("/<project>")
def get_all_grades(project):
    hackbright_app.connect_to_db()
    #grades_for_all_students=request.args.get("project")
    #print grades_for_all_students
    actual_grades = hackbright_app.get_all_project_grades(project)
    print actual_grades
    html = render_template("project_grades.html", project=project, 
        grades=actual_grades)
    return html



if __name__=="__main__":
    app.run(debug=True)