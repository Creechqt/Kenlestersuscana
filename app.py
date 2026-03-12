from flask import Flask, jsonify, request, render_template_string, redirect, url_for

app = Flask(_name_)

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
    <h1>Student List</h1>
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
    """
    return render_template_string(html, students=students)

# ---------- ADD STUDENT FORM ----------
@app.route('/add_student_form')
def add_student_form():
    html = """
    <h2>Add New Student</h2>
    <form action="{{ url_for('add_student') }}" method="POST">
        Name: <input type="text" name="name" required autofocus><br><br>
        Grade: <input type="number" name="grade" required><br><br>
        Section: <input type="text" name="section" required><br><br>
        <button type="submit">Add Student</button>
    </form>
    <br><a href="{{ url_for('list_students') }}">Back to Student List</a>
    """
    return render_template_string(html)

# ---------- ADD STUDENT POST ----------
@app.route('/add_student', methods=['POST'])
def add_student():
    name = request.form.get("name")
    grade = int(request.form.get("grade"))
    section = request.form.get("section")
    new_id = max([s["id"] for s in students]) + 1 if students else 1
    new_student = {"id": new_id, "name": name, "grade": grade, "section": section}
    students.append(new_student)
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
        return redirect(url_for('list_students'))

    html = """
    <h2>Edit Student</h2>
    <form method="POST">
        Name: <input type="text" name="name" value="{{ student.name }}" required><br><br>
        Grade: <input type="number" name="grade" value="{{ student.grade }}" required><br><br>
        Section: <input type="text" name="section" value="{{ student.section }}" required><br><br>
        <button type="submit">Update Student</button>
    </form>
    <br><a href="{{ url_for('list_students') }}">Back to Student List</a>
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
    return redirect(url_for('list_students'))

# ---------- API: GET ALL STUDENTS ----------
@app.route('/api/students', methods=['GET'])
def get_students_api():
    return jsonify(students)

if _name_ == '_main_':
    app.run(debug=True)
    app.run(debug=True)
