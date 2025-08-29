from flask import Flask, render_template, request, redirect, url_for, flash
from db import init_db, add_student, add_grade, get_student, list_students, calculate_student_average, subject_topper, class_average

app = Flask(__name__)
app.secret_key = "replace-this-with-a-random-secret"
init_db()

@app.route("/")
def index():
    students = list_students()
    return render_template("index.html", students=students)

@app.route("/students", methods=["POST"])
def create_student():
    name = request.form.get("name", "").strip()
    roll = request.form.get("roll", "").strip()
    if not name or not roll:
        flash("Name and Roll are required.", "error")
        return redirect(url_for("index"))
    if add_student(name, roll):
        flash("Student added.", "success")
    else:
        flash("Roll number already exists.", "error")
    return redirect(url_for("index"))

@app.route("/students/<roll>")
def student_detail(roll):
    stu = get_student(roll)
    if not stu:
        flash("Student not found.", "error")
        return redirect(url_for("index"))
    return render_template("student_detail.html", student=stu)

@app.route("/grades", methods=["POST"])
def create_grade():
    roll = request.form.get("roll", "").strip()
    subject = request.form.get("subject", "").strip()
    grade = request.form.get("grade", "").strip()
    try:
        grade_val = float(grade)
    except ValueError:
        flash("Grade must be a number.", "error")
        return redirect(url_for("student_detail", roll=roll) if roll else url_for("index"))
    ok, msg = add_grade(roll, subject, grade_val)
    flash(msg, "success" if ok else "error")
    return redirect(url_for("student_detail", roll=roll))

@app.route("/analytics/topper", methods=["GET"])
def analytics_topper():
    subject = request.args.get("subject", "").strip()
    top = subject_topper(subject) if subject else None
    return render_template("analytics.html", subject=subject, topper=top, class_avg=class_average(subject) if subject else None)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
