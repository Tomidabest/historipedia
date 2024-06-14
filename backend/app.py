from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from keycloak import KeycloakOpenID, KeycloakGetError
from functools import wraps
import os

# App Configuration
app = Flask(__name__)
CORS(app)
app.config['DB_USER'] = os.getenv('DB_USER', 'mariadb_user')
app.config['DB_PASSWORD'] = os.getenv('DB_PASSWORD', 'secure_pass123')
app.config['DB_HOST'] = os.getenv('DB_HOST', 'localhost')
app.config['DB_PORT'] = os.getenv('DB_PORT', '4006')
app.config['DB_NAME'] = os.getenv('DB_NAME', 'historipedia')
app.config['KEYCLOAK_SERVER_URL'] = os.getenv('KEYCLOAK_SERVER_URL', "http://localhost:8080/")
app.config['KEYCLOAK_CLIENT_ID'] = os.getenv('KEYCLOAK_CLIENT_ID', "historipedia-client")
app.config['KEYCLOAK_REALM_NAME'] = os.getenv('KEYCLOAK_REALM_NAME', "historipedia-realm")

keycloak_openid = KeycloakOpenID(
    server_url=app.config['KEYCLOAK_SERVER_URL'],
    client_id=app.config['KEYCLOAK_CLIENT_ID'],
    realm_name=app.config['KEYCLOAK_REALM_NAME'],
)

def get_db_connection():
    return mysql.connector.connect(
        user=app.config['DB_USER'],
        password=app.config['DB_PASSWORD'],
        host=app.config['DB_HOST'],
        port=app.config['DB_PORT'],
        database=app.config['DB_NAME']
    )

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization', '').split(' ')[1] if 'Authorization' in request.headers else None
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            keycloak_openid.userinfo(token)
        except KeycloakGetError as e:
            if e.response_code == 401:
                refresh_token = request.headers.get('refresh_token')
                if refresh_token:
                    try:
                        new_token = keycloak_openid.refresh_token(refresh_token)
                        token = new_token['access_token']
                        request.headers['Authorization'] = f'Bearer {token}'
                        request.headers['refresh_token'] = new_token['refresh_token']
                        keycloak_openid.userinfo(token)
                    except Exception as refresh_e:
                        return jsonify({'message': 'Token refresh failed!'}), 401
                return jsonify({'message': 'Refresh token is missing!'}), 401
            return jsonify({'message': 'Token is invalid!'}), 401
        return f(*args, **kwargs)
    return decorated

@app.route('/historical_entries', methods=['GET'])
@token_required
def get_historical_entries():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM historical_entries')
    entries = cursor.fetchall()
    connection.close()
    return jsonify(entries), 200

@app.route('/historical_entries', methods=['POST'])
@token_required
def add_historical_entry():
    new_entry = request.json
    title = new_entry['title']
    description = new_entry['description']
    year = new_entry['year']

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        'INSERT INTO historical_entries (title, description, year) VALUES (%s, %s, %s)',
        (title, description, year))
    connection.commit()
    connection.close()

    return jsonify({'message': 'Historical entry added successfully!'}), 201

@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'Welcome to HistoriPedia!'}), 200

if __name__ == '__main__':
    app.run(debug=os.getenv('FLASK_ENV') == 'development')