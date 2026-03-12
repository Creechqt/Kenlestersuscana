from flask import Flask, jsonify, request

app = Flask(__name__)

# sample student data
student = {
    "name": "Your Name",
    "grade": 10,
    "section": "Zechariah"
}

@app.route('/')
def home():
    return "Welcome to my Flask API!"

# GET student info
@app.route('/student', methods=['GET'])
def get_student():
    return jsonify(student)

# UPDATE student info
@app.route('/student/update', methods=['POST'])
def update_student():
    data = request.get_json()

    if "name" in data:
        student["name"] = data["name"]

    if "grade" in data:
        student["grade"] = data["grade"]

    if "section" in data:
        student["section"] = data["section"]

    return jsonify({
        "message": "Student updated successfully",
        "student": student
    })

if __name__ == '__main__':
    app.run(debug=True)
