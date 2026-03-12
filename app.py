from flask import Flask, jsonify, request, render_template_string, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Needed for flash messages

# In-memory student list
students = [
    {"id": 1, "name": "Juan", "grade": 85, "section": "Zechariah"},
    {"id": 2, "name": "Maria", "grade": 90, "section": "Zechariah"},
    {"id": 3, "name": "Pedro", "grade": 70, "section": "Zion"}
]

# ---------- HOME ----------
@app.route('/')
def home():
    return redirect(url_for('list_students'))

# ---------- LIST STUDENTS ----------
@app.route('/students')
def list_students():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Student List</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            ul { list-style-type: none; padding: 0; }
            li { margin-bottom: 10px; }
            a { text-decoration: none; color: blue; margin-left: 10px; }
            .flash { color: green; }
        </style>
    </head>
    <body>
        <h1>Student List</h1>
        {% with messages = get_flashed_messages() %}
          {% if messages %}
            <ul class="flash">
            {% for msg in messages %}
              <li>{{ msg }}</li>
            {% endfor %}
            </ul>
          {% endif %}
        {% endwith %}
        <a href="{{ url_for('add_student_form') }}">Add New Student</a>
        <ul>
        {% for s in students %}
            <li>
            ID: {{ s.id }} - {{ s.name }} (Grade: {{ s.grade }}, Section: {{ s.section }})
            [<a href="{{ url_for('edit_student', id=s.id) }}">Edit</a>]
            [<a href="{{ url_for('delete_student', id=s.id) }}">Delete</a>]
            </li>
        {% endfor %}
        </ul>
    </body>
    </html>
    """
    return render_template_string(html, students=students)

# ---------- ADD STUDENT FORM ----------
@app.route('/add_student_form')
def add_student_form():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Add Student</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            input { margin-bottom: 10px; padding: 5px; }
            button { padding: 5px 10px; }
        </style>
    </head>
    <body>
        <h2>Add New Student</h2>
        <form action="{{ url_for('add_student') }}" method="POST">
            Name: <input type="text" name="name" required autofocus><br>
            Grade: <input type="number" name="grade" required><br>
            Section: <input type="text" name="section" required><br>
            <button type="submit">Add Student</button>
        </form>
        <br>
        <a href="{{ url_for('list_students') }}">Back to Student List</a>
    </body>
    </html>
    """
    return render_template_string(html)

# ---------- ADD STUDENT POST ----------
@app.route('/add_student', methods=['POST'])
def add_student():
    name = request.form.get("name")
    grade = int(request.form.get("grade"))
    section = request.form.get("section")
    new_id = max([s["id"] for s in students], default=0) + 1
    new_student = {"id": new_id, "name": name, "grade": grade, "section": section}
    students.append(new_student)
    flash(f"Student '{name}' added successfully!")
    return redirect(url_for('list_students'))

# ---------- EDIT STUDENT ----------
@app.route('/edit_student/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    student = next((s for s in students if s["id"] == id), None)
    if not student:
        return "Student not found", 404

    if request.method == 'POST':
        student["name"] = request.form["name"]
        student["grade"] = int(request.form["grade"])
        student["section"] = request.form["section"]
        flash(f"Student '{student['name']}' updated successfully!")
        return redirect(url_for('list_students'))

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Edit Student</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            input { margin-bottom: 10px; padding: 5px; }
            button { padding: 5px 10px; }
        </style>
    </head>
    <body>
        <h2>Edit Student</h2>
        <form method="POST">
            Name: <input type="text" name="name" value="{{ student.name }}" required><br>
            Grade: <input type="number" name="grade" value="{{ student.grade }}" required><br>
            Section: <input type="text" name="section" value="{{ student.section }}" required><br>
            <button type="submit">Update Student</button>
        </form>
        <br>
        <a href="{{ url_for('list_students') }}">Back to Student List</a>
    </body>
    </html>
    """
    return render_template_string(html, student=student)

# ---------- DELETE STUDENT ----------
@app.route('/delete_student/<int:id>')
def delete_student(id):
    global students
    student = next((s for s in students if s["id"] == id), None)
    if not student:
        return "Student not found", 404
    students = [s for s in students if s["id"] != id]
    flash(f"Student '{student['name']}' deleted successfully!")
    return redirect(url_for('list_students'))

# ---------- API: GET ALL STUDENTS ----------
@app.route('/api/students', methods=['GET'])
def get_students_api():
    return jsonify(students)

if __name__ == '__main__':
    app.run(debug=True)
