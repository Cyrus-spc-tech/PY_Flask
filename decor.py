from flask import Flask

app = Flask(__name__)

def simple_decorator(func):
    def wrapper():
        print("Do something before function call")
        func()
        print("Do something after function call")
    return wrapper

@app.route('/')

@simple_decorator
def say_hello():
    return "Hello, World!"
