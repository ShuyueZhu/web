from flask import Flask, render_template, redirect, url_for, flash,  request
import re
import math
import requests


app = Flask(__name__)


@app.route("/submit3", methods=['POST'])
def submit3():
    username = "ShuyueZhu"
    # get respiratory information
    repo_response = requests.get(f"https://api.github.com/users/{username}/repos")
    if repo_response.status_code == 200:
        repos = repo_response.json()
    else:
        repos = []

    # get lastest information
    commit_info = {}
    for repo in repos:
        commits_response = requests.get(f"https://api.github.com/repos/{username}/{repo['name']}/commits")
        if commits_response.status_code == 200:
            commits = commits_response.json()
            if commits:
                latest_commit = commits[0]
                commit_info[repo['name']] = {
                    "latest_commit_hash": latest_commit['sha'],
                    "latest_commit_author": latest_commit['commit']['author']['name'],
                    "latest_commit_date": latest_commit['commit']['author']['date'],
                    "latest_commit_message": latest_commit['commit']['message']
                }

    return render_template("name.html", repos=repos, commit_info=commit_info)


@app.route("/submit4", methods=['POST'])
def submit4():
    username = "ShuyueZhu"
     # Accessing the GitHub API to obtain followers and user data for followers
    followers_url = f"https://api.github.com/users/{username}/followers"
    following_url = f"https://api.github.com/users/{username}/following"
    try:
        followers_response = requests.get(followers_url)
        following_response = requests.get(following_url)
        followers_data = followers_response.json()
        following_data = following_response.json()
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

    return render_template("github_users.html", followers=followers_data, following=following_data)


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
