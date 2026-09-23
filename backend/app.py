from flask import Flask, render_template, request, redirect
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


@app.route("/semester-leave", methods=["GET", "POST"])
def semester_leave():

    if request.method == "POST":

        student_id = request.form.get("student_id")
        from_date = request.form.get("from_date")
        to_date = request.form.get("to_date")
        reason = request.form.get("reason")

        full_date = (
            "From: "
            + from_date
            + " | To: "
            + to_date
        )

        connection = get_database_connection()

        connection.execute(
            """
            INSERT INTO leave_requests
            (student_id, leave_type, leave_date, reason)
            VALUES (?, ?, ?, ?)
            """,
            (student_id, "Semester Leave", full_date, reason)
        )

        connection.commit()
        connection.close()

        return "Semester leave application submitted successfully!"

    return render_template("semester_leave.html")


@app.route("/hometown-leave", methods=["GET", "POST"])
def hometown_leave():

    if request.method == "POST":

        student_id = request.form.get("student_id")
        from_date = request.form.get("from_date")
        to_date = request.form.get("to_date")
        hometown = request.form.get("hometown")
        reason = request.form.get("reason")

        full_date = (
            "From: "
            + from_date
            + " | To: "
            + to_date
        )

        full_reason = (
            "Hometown: "
            + hometown
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
            (student_id, "Hometown Leave", full_date, full_reason)
        )

        connection.commit()
        connection.close()

        return "Hometown leave application submitted successfully!"

    return render_template("hometown_leave.html")


@app.route("/warden-login", methods=["GET", "POST"])
def warden_login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        if username == "warden" and password == "1234":
            return redirect("/warden-dashboard")

        return "Invalid Warden Username or Password!"

    return render_template("warden_login.html")


@app.route("/warden-dashboard")
def warden_dashboard():

    connection = get_database_connection()

    requests = connection.execute(
        """
        SELECT * FROM leave_requests
        ORDER BY id DESC
        """
    ).fetchall()

    total_requests = connection.execute(
        "SELECT COUNT(*) FROM leave_requests"
    ).fetchone()[0]

    pending_requests = connection.execute(
        "SELECT COUNT(*) FROM leave_requests WHERE status = 'Pending'"
    ).fetchone()[0]

    approved_requests = connection.execute(
        "SELECT COUNT(*) FROM leave_requests WHERE status = 'Approved'"
    ).fetchone()[0]

    rejected_requests = connection.execute(
        "SELECT COUNT(*) FROM leave_requests WHERE status = 'Rejected'"
    ).fetchone()[0]

    connection.close()

    return render_template(
        "warden_dashboard.html",
        requests=requests,
        total_requests=total_requests,
        pending_requests=pending_requests,
        approved_requests=approved_requests,
        rejected_requests=rejected_requests
    )


@app.route("/update-request/<int:request_id>", methods=["POST"])
def update_request(request_id):

    status = request.form.get("status")

    connection = get_database_connection()

    connection.execute(
        """
        UPDATE leave_requests
        SET status = ?
        WHERE id = ?
        """,
        (status, request_id)
    )

    connection.commit()
    connection.close()

    return redirect("/warden-dashboard")


if __name__ == "__main__":
    app.run(debug=True)