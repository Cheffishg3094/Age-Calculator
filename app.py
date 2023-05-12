from calendar import calendar
from flask import Flask, render_template, request, redirect, url_for
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

app = Flask(__name__)


class Person:
    def __init__(self, name, birthdate):
        self.name = name
        self.birthdate = birthdate

    def age(self):
        today = datetime.now().date()
        delta = relativedelta(today, self.birthdate)
        return delta.years, delta.months, delta.days


people = []


@app.route("/")
def index():
    now = datetime.now().date()
    return render_template("index.html", now=now, people=people)


from datetime import datetime, date


@app.route("/", methods=["POST"])
def calculate_age():
    name = request.form.get("name")
    year = int(request.form.get("year")) # type: ignore
    month = int(request.form.get("month")) # type: ignore
    day = int(request.form.get("day")) # type: ignore
    try:
        birthdate = datetime(year, month, day).date()
    except ValueError:
        answer = "Invalid date entered!"
        now = datetime.now().date()
        return render_template("index.html", answer=answer, now=now)
    today = date.today()
    if birthdate > today:
        answer = "You cannot enter a future date!"
    else:
        person = Person(name, birthdate)
        people.append(person)
        age_years, age_months, age_days = person.age()
        answer = f"Hey {name}! You are {age_years} years, {age_months} months, and {age_days} days old!"
    now = datetime.now().date()
    return render_template("index.html", answer=answer, now=now, people=people)


@app.route("/clear", methods=["POST"])
def clear_data():
    people.clear()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
