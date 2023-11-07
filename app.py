from cs50 import SQL
from flask import Flask, redirect, render_template, request

app = Flask(__name__)

db = SQL("sqlite:///project.db")


@app.route("/", methods=["GET"])
def index():
    mastery_list = db.execute("SELECT * FROM mastery_list ORDER BY (ease+importance) DESC")
    return render_template("index.html", mastery_list=mastery_list)


@app.route("/add", methods=["POST"])
def add():
    task = request.form.get("task")
    ease = request.form.get("ease")
    importance = request.form.get("importance")
    if int(ease) > 10 or int(importance) > 10 or int(ease) < 1 or int(importance) < 1:
        return apology("Ease and importance must be 1-10.")
    db.execute("INSERT INTO mastery_list (task, ease, importance) VALUES (?, ?, ?)", task, ease, importance)
    return redirect("/")


@app.route("/delete", methods=["POST"])
def delete():
    task = request.form.get("delete")
    if task:
        db.execute("DELETE FROM mastery_list WHERE task = ?", task)
    return redirect("/")


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code