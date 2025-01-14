import secrets
from flask import Flask, make_response, request
from database import users
import bcrypt
import pyotp

app = Flask(__name__)

@app.route('/')
def home():
    return '<p>Secret Sauces</p>'

@app.route('/login', methods = ["POST"])
def login():
    # parse data from request
    username, password, otp = request.form['username'], request.form['password'], request.form['otp']

    user = users.find_one({'name': username})

    # if user doesn't exist or password incorrect
    if user == None or not bcrypt.checkpw(password.encode('utf8'), user['password']):
        return "login error", 403

    # check for 2fa
    if "otp" in user and not pyotp.TOTP(user["otp"]).verify(otp):
        return "login error", 403

    token = str(secrets.token_bytes(20))
    users.update_one({'name': username}, { "$push": { "token": token } })
    resp = make_response("success")
    resp.set_cookie("token", token)
    return resp
    

    

@app.route('/signup', methods = ["POST"])
def signup():
    # parse data from request
    username, password = request.form['username'], request.form['password']

    # check if user already exists
    if users.count_documents({'name': username}) != 0:
        return "user exists", 409

    # insert new user
    hashed = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
    users.insert_one({'name': username, 'password': hashed })
    return "success", 200

@app.route('/setup_auth')
def setup_auth():
    token = request.cookies.get("token")

    if token == None:
        return "not logged in", 403

    if users.count_documents({'token': token}) == 0:
        return "invalid auth token", 403
    
    key = pyotp.random_base32()

    users.update_one({'token': token}, { "$set": { "otp": key } })
    user = users.find_one({'token': token})
    setup_string = pyotp.totp.TOTP(key).provisioning_uri(name=user["name"], issuer_name='Hide My Secret Sauce')

    return setup_string

    


