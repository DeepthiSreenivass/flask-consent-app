from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import csv
import os
from datetime import datetime

app = Flask(__name__)
DATABASE = "participants.db"
CSV_FILE = "participants.csv"

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS participants (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT,
                email TEXT,
                phone_number TEXT,
                consent_date TEXT
            )
        ''')
        conn.commit()

def save_to_csv(data):
    file_exists = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Full Name", "Email", "Phone Number", "Date"])
        
        # Ensure the date is formatted correctly
        try:
            formatted_date = datetime.strptime(data[3], "%Y-%m-%d").strftime("%d-%m-%Y")  # Change format if needed
        except ValueError:
            formatted_date = data[3]  # Use original if it fails
        
        writer.writerow([data[0], data[1], data[2], f"'{formatted_date}"])

@app.route("/", methods=["GET", "POST"])
def consent_form():
    if request.method == "POST":
        full_name = request.form.get("name")
        email = request.form.get("email")
        phone_number = request.form.get("phone")
        consent_date = request.form.get("date")
        agreement = request.form.get("agreement")
        
        if agreement:
            with sqlite3.connect(DATABASE) as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO participants (full_name, email, phone_number, consent_date) VALUES (?, ?, ?, ?)", (full_name, email, phone_number, consent_date))
                conn.commit()
            
            save_to_csv([full_name, email, phone_number, consent_date])
            return redirect(url_for("thank_you"))
        
    return render_template("index.html")

@app.route("/thank-you")
def thank_you():
    return "Thank you for your participation! Your consent has been recorded."

@app.route("/init-db")
def initialize_database():
    init_db()
    return "Database initialized successfully!"

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
