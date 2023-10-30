from flask import Flask, render_template, request
app = Flask(__name__)


@app.route("/")
def hello():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():
    input_name = request.form.get("name")
    input_age = request.form.get("age")
    return render_template("hello.html", name=input_name, age=input_age)


@app.route("/query", methods=["GET"])
def get_query():
    query = request.args.get('q')
    return process_query(query)


def process_query(query):
    if query == "dinosaurs":
        result = "Dinosaurs ruled the Earth 200 million years ago"
    elif query == "asteroids":
        result = "Unknown"
    elif query == "What is your name?":
        result == "SY"
    else:
        result == "input again"
    return result
