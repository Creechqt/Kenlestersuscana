from flask import Flask, jsonify, request, render_template_string, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "supersecret"  # Needed for flash messages

# Sample in-memory data
students = [
    {"id": 1, "name": "Juan", "grade": 85, "section": "Zechariah"},
    {"id": 2, "name": "Maria", "grade": 90, "section": "Zechariah"},
    {"id": 3, "name": "Pedro", "grade": 70, "section": "Zion"}
]

@app.route('/')
def home():
    return redirect(url_for('list_students'))

# Show all students
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
            a { text-decoration: none; color: blue; }
        </style>
    </head>
    <body>
        <h2>Student List</h2>
        {% with messages = get_flashed_messages() %}
          {% if messages %}
            <ul style="color: green;">
            {% for msg in messages %}
              <li>{{ msg }}</li>
            {% endfor %}
            </ul>
          {% endif %}
        {% endwith %}
        <ul>
        {% for s in students %}
            <li>
                ID: {{s.id}} - {{s.name}} (Grade: {{s.grade}}, Section: {{s.section}})
                [<a href="{{ url_for('edit_student', id=s.id) }}">Edit</a>]
            </li>
        {% endfor %}
        </ul>
    </body>
    </html>
    """
    return render_template_string(html, students=students)

# Edit student
@app.route('/edit_student/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    student = next((s for s in students if s["id"] == id), None)
    if not student:
        return "Student not found", 404

    if request.method == 'POST':
        # Get form data safely
        student["name"] = request.form.get("name", student["name"])
        try:
            student["grade"] = int(request.form.get("grade", student["grade"]))
        except ValueError:
            flash("Invalid grade input. Keeping previous value.")
        student["section"] = request.form.get("section", student["section"])

        flash(f"Student '{student['name']}' updated successfully!")
        return redirect(url_for('list_students'))

    # Show form
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Edit Student</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            input { margin-bottom: 10px; }
            button { padding: 5px 10px; }
        </style>
    </head>
    <body>
        <h2>Edit Student</h2>
        <form method="POST">
            Name: <input type="text" name="name" value="{{student.name}}" required><br>
            Grade: <input type="number" name="grade" value="{{student.grade}}" required><br>
            Section: <input type="text" name="section" value="{{student.section}}" required><br>
            <button type="submit">Update</button>
        </form>
        <br>
        <a href="{{ url_for('list_students') }}">Back to List</a>
    </body>
    </html>
    """
    return render_template_string(html, student=student)

if __name__ == '__main__':
    app.run(debug=True)
