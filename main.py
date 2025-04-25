from flask import Flask
app=Flask(__name__)
@app.route("/")
def hel():
    return "Hello World!"

if __name__=="__main__":
    app.run(debug=True,host="")