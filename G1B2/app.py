from flask import Flask, render_template    # redirect ,url_for

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')
# @app.route('/')
# def redirect_example():
#     return redirect(url_for('index'))


@app.route('/about')
def about():
    return render_template('about.html')





if __name__ == '__main__':
    app.run(debug=True)