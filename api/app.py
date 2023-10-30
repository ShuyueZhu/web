from flask import Flask, render_template, request
import re
import math
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
    addition_pattern = r'What is (\d+) plus (\d+)?'
    multiplication_pattern = r'What is (\d+) multiplied by (\d+)?'
    largest_pattern = r'Which of the following numbers is both a square and a cube: (\d+), (\d+), (\d+)?'
    square_cube_pattern = r'Which of the following numbers is the largest: (\d+), (\d+), (\d+)?'
    minus_pattern = r'What is (\d+) minus (\d+)?'
    match_addition = re.search(addition_pattern, q)
    if match_addition:
        num1, num2 = map(int, match_addition.groups())
        return str(num1 + num2)

    match_multiplication = re.search(multiplication_pattern, q)
    if match_multiplication:
        nums = map(int, match_multiplication.groups())
        return str(max(nums))

    match_largest = re.search(largest_pattern, q)
    if match_largest:
        num1, num2 = map(int, match_largest.groups())
        return str(num1 * num2)

    match_square_cube = re.search(square_cube_pattern, q)
    if match_square_cube:
        nums = map(int, match_square_cube.groups())
        result = []
        for num in nums:
            if math.isqrt(num)**2 == num and round(num**(1/3))**3 == num:
                result.append(num)
        if len(result) == 1:
            return result[0]
        else:
            return result

    match_minus = re.search(minus_pattern, q)
    if match_minus:
        num1, num2 = map(int, match_minus.groups())
        return str(num1 - num2)

    if q == "dinosaurs":
        return "Dinosaurs ruled the Earth 200 million years ago"
    elif q == "asteroids":
        return "Unknown"
    elif q == "What is your name?":
        return "ZSY"
    else:
        return "Unrecognized input!!!"


@app.route('/query', methods=['GET'])
def query_route():
    query = request.args.get('q')
    result = process_query(query)
    return result
