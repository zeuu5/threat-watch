from flask import Flask, render_template, request
import datetime

app = Flask(__name__)

users = {
    "admin": "password123"
}

LOG_FILE = "logs.txt"

def log_attempt(username, password, result):

    with open(LOG_FILE, "a") as f:

        f.write(
            f"{datetime.datetime.now()} | "
            f"{username} | "
            f"{password} | "
            f"{result}\n"
        )

@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username in users and users[username] == password:

            log_attempt(username, password, "SUCCESS")

            return "✅ Login Successful"

        else:

            log_attempt(username, password, "FAIL")

            return "❌ Login Failed"

    return render_template("login.html")

@app.route("/logs")
def logs():

    try:
        with open(LOG_FILE, "r") as f:
            data = f.read()

    except:
        data = "No logs yet."

    return f"<pre>{data}</pre>"

if __name__ == "__main__":
    app.run(debug=True)