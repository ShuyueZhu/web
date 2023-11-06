from flask import Flask, render_template, request
import re
import math


app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():
    input_name = request.form.get("name")
    input_age = request.form.get("age")
    return render_template("hello.html", name=input_name, age=input_age)


@app.route("/submit2", methods=["POST"])
def submit2():
    input_name = request.form.get("github_name")
    return render_template("hello_github.html", name=input_name)


@app.route("/query", methods=["GET"])
def get_query_parameter():
    query_parameter = request.args.get("q")
    return process_query(query_parameter)


def is_prime(i):
    if i <= 1 or i % 2 == 0 or i % 3 == 0:
        return False
    elif i <= 3:
        return True
    else:
        k = 5
        while k * k <= i:
            if i % k == 0 or i % (k + 2) == 0:
                return False
            k += 6
        return True


def process_query(query_parameter):
    pattern_multiplied = r'What is \d+ multiplied by \d+\?$'
    large = r'Which of the following numbers is the largest: (\d+)(, \d+)*\?$'
    pattern_plus = r'What is \d+ plus \d+\?$'
    cubes = r'[A-Za-z\s]+ is both a square and a cube: (\d+)(, \d+)*\?$'
    prime = r'Which of the following numbers are primes: (\d+)(, \d+)*\?$'
    pattern_minus = r'What is \d+ minus \d+\?$'
    pattern_num = r'\d+'

    if re.match(pattern_multiplied, query_parameter):
        matches = re.findall(pattern_num, query_parameter)
        res = 1
        for i in matches:
            res = res * int(i)
        return str(res)

    elif re.match(large, query_parameter):
        matches = re.findall(pattern_num, query_parameter)
        int_ls = [int(i) for i in matches]
        return str(max(int_ls))

    elif re.match(pattern_plus, query_parameter):
        matches = re.findall(pattern_num, query_parameter)
        res = 0
        for i in matches:
            res = res + int(i)
        return str(res)

    elif re.match(cubes, query_parameter):
        matches = re.findall(pattern_num, query_parameter)
        res = ""
        for i in matches:
            i = int(i)
            square_root = round(math.sqrt(i), 5)
            cube_root = round(i ** (1/3), 5)
            if square_root.is_integer() and cube_root.is_integer():
                res = res + str(i) + ", "
        return res[0:-2]

    elif re.match(pattern_minus, query_parameter):
        matches = re.findall(pattern_num, query_parameter)
        return str(int(matches[0])-int(matches[1]))

    elif re.match(prime, query_parameter):
        matches = re.findall(pattern_num, query_parameter)
        res = ""
        for i in matches:
            i = int(i)
            if is_prime(i):
                res = res + str(i) + ", "
        return res[0:-2]

    elif query_parameter == "What is your name?":
        return "ZSY"

    elif query_parameter == "dinosaurs":
        return "Dinosaurs ruled the Earth 200 million years ago"

    else:
        return "Unknown"
