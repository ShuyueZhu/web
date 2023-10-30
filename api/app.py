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


def process_query(q):
    if q == "dinosaurs":
        return "Dinosaurs ruled the Earth 200 million years ago"
    elif q == "asteroids":
        return "Unknown"
    elif q == "What is your name?":
        return "SY"
    else:
        return "Unrecognized input!!!"


@app.route('/query', methods=['GET'])
def query_route():
    query = request.args.get('q')
    result = process_query(query)
    return result
