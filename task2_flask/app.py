"""
Task 2: Flask-based Student Management Web Application with Jinja2 Templates
Course: CSR210 - Advanced Programming & Databases

Pages:
1. Home Page (/) - Welcome message & nav links
2. Student List (/students) - HTML table, ID, Name, Email, Course, Marks + Search Bonus
3. Add Student (/students/add) - Form with POST method
4. Student Details (/students/<id>) - Complete student details
5. Jinja2 Features: Variables, For loops, If conditions, Template Inheritance (base.html)
"""

from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "csr210_secret_key_student_mgmt"

# In-memory storage for students
students = [
    {"id": 1, "name": "Aarav Sharma", "email": "aarav.sharma@example.com", "course": "B.Tech CSE", "marks": 89.5},
    {"id": 2, "name": "Diya Patel", "email": "diya.patel@example.com", "course": "B.Tech IT", "marks": 92.0},
    {"id": 3, "name": "Rohan Verma", "email": "rohan.verma@example.com", "course": "MCA", "marks": 78.5},
    {"id": 4, "name": "Sneha Reddy", "email": "sneha.reddy@example.com", "course": "BCA", "marks": 85.0},
    {"id": 5, "name": "Vikram Singh", "email": "vikram.singh@example.com", "course": "B.Tech AI", "marks": 95.0},
]


@app.route("/")
def home():
    """1. Home Page: Welcome message and quick statistics"""
    total_students = len(students)
    avg_marks = round(sum(s["marks"] for s in students) / total_students, 2) if total_students > 0 else 0
    return render_template("index.html", total_students=total_students, avg_marks=avg_marks)


@app.route("/students")
def student_list():
    """2. Student List Page: Displays students in an HTML table with bonus search functionality"""
    search_query = request.args.get("search", "").strip()
    if search_query:
        # Bonus requirement: search students by name (case-insensitive)
        filtered_students = [
            s for s in students if search_query.lower() in s["name"].lower()
        ]
    else:
        filtered_students = students

    return render_template("students.html", students=filtered_students, search_query=search_query)


@app.route("/students/add", methods=["GET", "POST"])
def add_student():
    """3. Add Student Page: HTML Form with POST method"""
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        course = request.form.get("course", "").strip()
        marks_raw = request.form.get("marks", "").strip()

        # Simple validation
        if not name or not email or not course or not marks_raw:
            flash("All fields are required!", "danger")
            return render_template("add_student.html")

        try:
            marks = float(marks_raw)
            if not (0 <= marks <= 100):
                flash("Marks must be between 0 and 100!", "danger")
                return render_template("add_student.html")
        except ValueError:
            flash("Marks must be a valid numeric value!", "danger")
            return render_template("add_student.html")

        new_id = max([s["id"] for s in students], default=0) + 1
        new_student = {
            "id": new_id,
            "name": name,
            "email": email,
            "course": course,
            "marks": marks
        }
        students.append(new_student)
        flash(f"Student '{name}' added successfully with ID #{new_id}!", "success")
        return redirect(url_for("student_list"))

    return render_template("add_student.html")


@app.route("/students/<int:student_id>")
def student_details(student_id):
    """4. Student Details Page: Complete details of selected student"""
    student = next((s for s in students if s["id"] == student_id), None)
    if not student:
        flash(f"Student with ID #{student_id} not found!", "danger")
        return redirect(url_for("student_list"))

    # Determine grade/performance for jinja demo
    if student["marks"] >= 90:
        grade = "A+ (Outstanding)"
        status_color = "success"
    elif student["marks"] >= 75:
        grade = "A (First Class)"
        status_color = "primary"
    elif student["marks"] >= 60:
        grade = "B (Second Class)"
        status_color = "info"
    elif student["marks"] >= 40:
        grade = "C (Pass)"
        status_color = "warning"
    else:
        grade = "F (Fail)"
        status_color = "danger"

    return render_template("student_detail.html", student=student, grade=grade, status_color=status_color)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
