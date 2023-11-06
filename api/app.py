from flask import Flask, render_template, request
import re
app = Flask(__name__)


@app.route("/")
def hello():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():
    input_name = request.form.get("name")
    input_age = request.form.get("age")
    input_name_github = request.form.get("gitname")
    button_clicked = request.form['submit_button']
    if button_clicked == 'Submit1':
        return render_template("hello.html", name=input_name, age=input_age)
    elif button_clicked == 'Submit2':
        return render_template("hello_github.html", name=input_name_github)


def process_query(q):
    # addition_pattern = r'What is (\d+) plus (\d+)?'
    # multiplication_pattern = r'What is (\d+) multiplied by (\d+)?'
    # largest_pattern = r'Which of the following numbers is the largest:' + \
    #     r'(\d+), (\d+), (\d+)?'
    # square_cube_pattern = r'Which of the following numbers is both ' + \
    #     r'a square and a cube' + \
    #     r': (\d+), (\d+), (\d+), (\d+), (\d+), (\d+), (\d+)?'
    # minus_pattern = r'What is (\d+) minus (\d+)?'
    # prime_pattern = r'Which of the following numbers are primes: ' + \
    #     r'(\d+), (\d+), (\d+), (\d+), (\d+)?'
    op = re.search(r'(plus|minus|multiplied|largest|primes|square)', q)
    if op:
        op = op.group()
        nums = list(map(int, re.findall(r'\d+', q)))

        # match_addition = re.search(addition_pattern, q)
        if op == 'plus':
            return str(sum(nums))

        # match_multiplication = re.search(multiplication_pattern, q)
        if op == 'multiplied':
            return str(nums[0] * nums[1])

        # match_largest = re.search(largest_pattern, q)
        if op == 'largest':
            return str(max(nums))

        # match_square_cube = re.search(square_cube_pattern, q)
        if op == 'square':

            def is_square_and_cube(n):
                root = round(n**(1/6))
                return root**6 == n
            result_numbers = [num for num in nums if is_square_and_cube(num)]
            return ', '.join(map(str, result_numbers))

        # match_minus = re.search(minus_pattern, q)
        if op == 'minus':
            return str(nums[0] - nums[1])

        # match_prime = re.search(prime_pattern, q)
        if op == 'primes':

            def is_prime(n):
                if n <= 1:
                    return False
                for i in range(2, int(n**0.5) + 1):
                    if n % i == 0:
                        return False
                return True
            primes = [str(num) for num in nums if is_prime(num)]
            return ', '.join(primes)

    elif q == "dinosaurs":
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
