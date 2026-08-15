from flask import Flask, jsonify, render_template, request, redirect
app = Flask(__name__)
import secrets

url_store = {}

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/shorten", methods=["POST"])
def shorten():
    long_url = request.form.get("input")
    if not long_url.startswith(("http://", "https://")):
        long_url = "https://" + long_url
    short_token = secrets.token_urlsafe(8)
    url_store[short_token] = long_url
    return f"<h3>Long url: {long_url} shortened to small.{short_token}</h3>"
    
@app.route("/<short_token>", methods=["GET"])    
def redirect_to_url(short_token):
    if short_token in url_store:
        print(f"Redirecting to: {url_store[short_token]}")
        return redirect(url_store[short_token])
    else:
        return "URL not found", 404

if __name__ == '__main__':
    app.run(debug=True, port=5001)