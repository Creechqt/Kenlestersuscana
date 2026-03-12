from flask import Flask, jsonify, request, render_template_string, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "supersecretkey"

# In-memory student list
students = [
    {"id": 1, "name": "Juan", "grade": 85, "section": "Zechariah"},
    {"id": 2, "name": "Maria", "grade": 90, "section": "Zechariah"},
    {"id": 3, "name": "Pedro", "grade": 70, "section": "Zion"}
]

# ---------- HOME / LIST STUDENTS ----------
@app.route('/')
@app.route('/students')
def list_students():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Student Dashboard</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css">
    </head>
    <body class="p-4">
        <div class="container">
            <h1 class="mb-4">Student Dashboard</h1>

            {% with messages = get_flashed_messages() %}
            {% if messages %}
            <div class="alert alert-success">
                {% for msg in messages %}
                    {{ msg }}<br>
                {% endfor %}
            </div>
            {% endif %}
            {% endwith %}

            <a href="{{ url_for('add_student_form') }}" class="btn btn-success mb-3">+ Add New Student</a>

            <table class="table table-bordered table-striped">
                <thead class="table-dark">
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Grade</th>
                        <th>Section</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                {% for s in students %}
                    <tr>
                        <td>{{ s.id }}</td>
                        <td>{{ s.name }}</td>
                        <td>{{ s.grade }}</td>
                        <td>{{ s.section }}</td>
                        <td>
                            <a href="{{ url_for('edit_student', id=s.id) }}" class="btn btn-primary btn-sm">Edit</a>
                            <a href="{{ url_for('delete_student', id=s.id) }}" class="btn btn-danger btn-sm" onclick="return confirm('Delete {{ s.name }}?');">Delete</a>
                        </td>
                    </tr>
                {% endfor %}
                </tbody>
            </table>
        </div>
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
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css">
    </head>
    <body class="p-4">
        <div class="container">
            <h2>Add New Student</h2>
            <form action="{{ url_for('add_student') }}" method="POST">
                <div class="mb-3">
                    <label>Name</label>
                    <input type="text" name="name" class="form-control" required autofocus>
                </div>
                <div class="mb-3">
                    <label>Grade</label>
                    <input type="number" name="grade" class="form-control" required>
                </div>
                <div class="mb-3">
                    <label>Section</label>
                    <input type="text" name="section" class="form-control" required>
                </div>
                <button type="submit" class="btn btn-success">Add Student</button>
                <a href="{{ url_for('list_students') }}" class="btn btn-secondary">Back</a>
            </form>
        </div>
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
    students.append({"id": new_id, "name": name, "grade": grade, "section": section})
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
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css">
    </head>
    <body class="p-4">
        <div class="container">
            <h2>Edit Student</h2>
            <form method="POST">
                <div class="mb-3">
                    <label>Name</label>
                    <input type="text" name="name" value="{{ student.name }}" class="form-control" required>
                </div>
                <div class="mb-3">
                    <label>Grade</label>
                    <input type="number" name="grade" value="{{ student.grade }}" class="form-control" required>
                </div>
                <div class="mb-3">
                    <label>Section</label>
                    <input type="text" name="section" value="{{ student.section }}" class="form-control" required>
                </div>
                <button type="submit" class="btn btn-primary">Update Student</button>
                <a href="{{ url_for('list_students') }}" class="btn btn-secondary">Back</a>
            </form>
        </div>
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
