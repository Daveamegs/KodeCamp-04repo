from flask import Flask


app = Flask(__name__)

# Route Traffic to Index


@app.route("/")
def index():
    return "Hello, Welcome to KodeCamp DevOps Bookcamp! New"


# Run App
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
