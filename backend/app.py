from flask import Flask, render_template, request
import sqlite3
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, "hostel.db")


def get_database_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        student_id = request.form.get("student_id")
        password = request.form.get("password")

        connection = get_database_connection()

        requests = connection.execute(
            """
            SELECT * FROM leave_requests
            WHERE student_id = ?
            ORDER BY id DESC
            """,
            (student_id,)
        ).fetchall()

        connection.close()

        return render_template(
            "dashboard.html",
            student_id=student_id,
            requests=requests
        )

    return render_template("login.html")


@app.route("/sick-leave", methods=["GET", "POST"])
def sick_leave():

    if request.method == "POST":

        student_id = request.form.get("student_id")
        leave_date = request.form.get("leave_date")
        reason = request.form.get("reason")

        connection = get_database_connection()

        connection.execute(
            """
            INSERT INTO leave_requests
            (student_id, leave_type, leave_date, reason)
            VALUES (?, ?, ?, ?)
            """,
            (student_id, "Sick Leave", leave_date, reason)
        )

        connection.commit()
        connection.close()

        return "Sick leave application submitted successfully!"

    return render_template("sick_leave.html")


@app.route("/outing", methods=["GET", "POST"])
def outing():

    if request.method == "POST":

        student_id = request.form.get("student_id")
        outing_date = request.form.get("outing_date")
        outing_time = request.form.get("outing_time")
        return_time = request.form.get("return_time")
        reason = request.form.get("reason")

        full_date = (
            outing_date
            + " | Out: "
            + outing_time
            + " | Return: "
            + return_time
        )

        connection = get_database_connection()

        connection.execute(
            """
            INSERT INTO leave_requests
            (student_id, leave_type, leave_date, reason)
            VALUES (?, ?, ?, ?)
            """,
            (student_id, "Outing", full_date, reason)
        )

        connection.commit()
        connection.close()

        return "Outing request submitted successfully!"

    return render_template("outing.html")


@app.route("/home-visit", methods=["GET", "POST"])
def home_visit():

    if request.method == "POST":

        student_id = request.form.get("student_id")
        visit_date = request.form.get("visit_date")
        guardian_name = request.form.get("guardian_name")
        guardian_phone = request.form.get("guardian_phone")
        address = request.form.get("address")
        reason = request.form.get("reason")

        full_reason = (
            "Guardian: "
            + guardian_name
            + " | Phone: "
            + guardian_phone
            + " | Address: "
            + address
            + " | Reason: "
            + reason
        )

        connection = get_database_connection()

        connection.execute(
            """
            INSERT INTO leave_requests
            (student_id, leave_type, leave_date, reason)
            VALUES (?, ?, ?, ?)
            """,
            (student_id, "Home Visit", visit_date, full_reason)
        )

        connection.commit()
        connection.close()

        return "Home visit request submitted successfully!"

    return render_template("home_visit.html")


if __name__ == "__main__":
    app.run(debug=True)