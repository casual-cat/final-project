from flask import Flask
from flask_sslify import SSLify

app = Flask(__name__)
sslify = SSLify(app)

@app.route("/")
def home():
    return "Hello, HTTPS!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)  # Remove `ssl_context`

