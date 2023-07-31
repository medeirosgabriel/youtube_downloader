# flask imports
from downloader import *
from flask import Flask, request, jsonify, make_response, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import uuid # for public id
from  werkzeug.security import generate_password_hash, check_password_hash

# Imports For PyJWT Authentication
import jwt
from datetime import datetime, timedelta
from functools import wraps

from downloader import *

app = Flask(__name__)

# Configuration
# NEVER HARDCODE YOUR CONFIGURATION IN YOUR CODE
# INSTEAD CREATE A .env FILE AND STORE IN IT
app.config['SECRET_KEY'] = 'your secret key'

# Database Name
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# Creates SQLALCHEMY Object
db = SQLAlchemy(app)

@app.before_first_request
def create_tables():
     db.create_all()

if __name__ == "__main__":
    app.run(debug=True, port=5000)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # Jwt is Passed In The Request Header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        # Return 401 If Token Is Not Passed
        if not token:
            return jsonify({'message' : 'Token Is Missing!'}), 401
  
        try:
            # Decoding The Payload To Fetch The Stored Details
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(public_id = data['public_id']).first()
        except:
            return jsonify({
                'message' : 'Token is Invalid!'
            }), 401
        # Returns The Current Logged In Users Contex To The Routes
        return  f(current_user, *args, **kwargs)
  
    return decorated

# Database ORMs
class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    public_id = db.Column(db.String(50), unique = True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(70), unique = True)
    password = db.Column(db.String(80))

############################################################################
################################## ROUTES ##################################
############################################################################

@app.route('/signup', methods =['POST'])
def signup():
    # Creates A Dictionary Of The Form Data
    data = request.get_json()
  
    # Gets Name, Email And Password
    name, email = data.get('name'), data.get('email')
    password = data.get('password')
  
    # Checking For Existing User
    user = User.query.filter_by(email = email).first()

    if not user:
        # Database ORM Object
        user = User(
            public_id = str(uuid.uuid4()),
            name = name,
            email = email,
            password = generate_password_hash(password)
        )
        # Insert User
        db.session.add(user)
        db.session.commit()
  
        return make_response('Successfully registered.', 201)
    else:
        # Returns 202 If User Already Exists
        return make_response('User already exists. Please Log in.', 202)

@app.route('/login', methods =['POST'])
def login():
    # Creates Dictionary Of Form Data
    auth = request.get_json()
  
    if not auth or not auth.get('email') or not auth.get('password'):
        # Returns 401 If Any Email Or / And Password Is Missing
        return make_response(
            'Could not verify',
            401,
            {'WWW-Authenticate' : 'Basic realm ="Login required !!"'}
        )
  
    user = User.query.filter_by(email = auth.get('email')).first()
  
    if not user:
        # Returns 401 If User Does Not Exist
        return make_response(
            'Could not verify',
            401,
            {'WWW-Authenticate' : 'Basic realm ="User does not exist !!"'}
        )
  
    if check_password_hash(user.password, auth.get('password')):
        # Generates The JWT Token
        token = jwt.encode({
            'public_id': user.public_id,
            'exp' : datetime.utcnow() + timedelta(minutes = 30)
        }, app.config['SECRET_KEY'])
  
        return make_response(jsonify({'token' : token.decode('UTF-8')}), 201)
    # Returns 403 If Password Is Wrong
    return make_response(
        'Could not verify',
        403,
        {'WWW-Authenticate' : 'Basic realm ="Wrong Password !!"'}
    )

@app.route('/users', methods =['GET'])
@token_required
def get_all_users(current_user):
    # Querying The Database
    # For All The Entries In It
    users = User.query.all()
    # Converting The Query Objects
    # To List Of Jsons
    output = []
    for user in users:
        # Appending The User Data Json
        # To The Response List
        output.append({
            'public_id': user.public_id,
            'name' : user.name,
            'email' : user.email
        })
  
    return jsonify({'users': output})

#############################################################################
############################## DOWNLOAD ROUTES ##############################
#############################################################################

@app.route('/youtube/video', methods=['POST'])
@token_required
def getVideo():
    data = request.get_json()
    link = data['link']
    name = downloadVideo(link)
    return send_from_directory("./video", f"{name}.mp4", as_attachment=True)

@app.route('/youtube/music', methods=['POST'])
@token_required
def getMusic():
    data = request.get_json()
    link = data['link']
    name = data['name']
    downloadMusic(link, name)
    return send_from_directory("./music", f"{name}.mp3", as_attachment=True)

@app.route('/youtube/music/<id>/<name>', methods=['GET'])
@token_required
def getMusic2(id, name):
    link = 'https://www.youtube.com/watch?v=' + id
    downloadMusic(link, name)
    return send_from_directory("./music", f"{name}.mp3", as_attachment=True)

@app.route('/youtube/video/<id>', methods=['GET'])
@token_required
def getVideo2(id):
    link = 'https://www.youtube.com/watch?v=' + id
    name = downloadVideo(link)
    return send_from_directory("./video", f"{name}.mp4", as_attachment=True)

    