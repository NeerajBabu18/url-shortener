from flask import Flask, jsonify, render_template, request, redirect
app = Flask(__name__)
import secrets
import psycopg2

create_table_query = """
CREATE TABLE IF NOT EXISTS urls(
    short_code varchar(255) PRIMARY KEY,
    long_url TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
)
"""

try:
    # Establish connection
    connection = psycopg2.connect(
        host="localhost",
        database="urlshortener",
        user="postgres",
        password="postgres",
        port="5432"
    )
    
    # Create a cursor object to execute queries
    cursor = connection.cursor()
    
    # Execute the table creation query
    cursor.execute(create_table_query)
    connection.commit()
    print("Table 'urls' created successfully!")

except (Exception, psycopg2.Error) as error:
    connection.rollback()
    print(f"Error while connecting to PostgreSQL: {error}")


url_store = {}

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/shorten", methods=["POST"])
def shorten():
    long_url = request.form.get("input")
    cursor = connection.cursor()
    
    if not long_url.startswith(("http://", "https://")):
        long_url = "https://" + long_url
    short_token = secrets.token_urlsafe(8)
    cursor.execute(
        "INSERT INTO urls (short_code, long_url) VALUES (%s, %s)", (short_token, long_url)
    )
    connection.commit()
    return f"<h3>Long url: {long_url} shortened to small.{short_token}</h3>"
    
@app.route("/<short_token>", methods=["GET"])    
def redirect_to_url(short_token):
    cursor = connection.cursor()
    cursor.execute("SELECT long_url FROM urls WHERE short_code = %s", (short_token,))
    result = cursor.fetchone()
    if result:
        print(f"Redirecting to: {result[0]}")
        return redirect(result[0])
    else:
        return "URL not found", 404

if __name__ == '__main__':
    app.run(debug=True, port=5001)