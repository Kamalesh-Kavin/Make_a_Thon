from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
CORS(app)

# configure MySQL
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'personal_expense'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# initialize MySQL
mysql = MySQL(app)

# registration endpoint
@app.route('/register', methods=['POST'])
def register():
    # parse request data
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    # hash the password for storage
    hashed_password = generate_password_hash(password, method='sha256')

    # insert user into database
    cur = mysql.connection.cursor()
    cur.execute('INSERT INTO users (name, email, password) VALUES (%s, %s, %s)', (name, email, hashed_password))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message': 'User created successfully!'}), 201

# login endpoint
@app.route('/login', methods=['POST'])
def login():
    # parse request data
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # retrieve user from database
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM users WHERE email = %s', (email,))
    user = cur.fetchone()
    cur.close()

    # check if user exists and password is correct
    if user and check_password_hash(user['password'], password):
        return jsonify({'message': 'Login successful!', 'user_id': user['id']}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

if __name__ == '__main__':
    app.run(debug=True)
