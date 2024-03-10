from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    # host '0,0,0,0' so we can open the app on other devices on the same network
    app.run(debug=True, host="0.0.0.0")
