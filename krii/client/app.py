from flask import Flask, render_template
app = Flask(__name__)

import requests

response = requests.get(f"http://localhost:4000/blocks")
blocks = response.json()["blocks"]

@app.route("/")
def hello():
    return render_template("home.html", blocks=blocks)

if __name__ == "__main__":
    app.run()