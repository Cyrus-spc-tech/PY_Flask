from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/hello', methods=['POST'])
def hello():
    name = request.form.get('name')
    return f"<h2>Hello {name}, you are learning Flask!</h2>"

if __name__ == '__main__':
    app.run(debug=True)
