import os
import re
import datetime
from flask import Flask, jsonify, request
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from models import (
    db,
    User,
    Event,
    favorite,
    attendance,
    Auth,
    Calendar,
    Category,
    Facebook,
)
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import (
    JWTManager,
    jwt_required,
    create_access_token,
    get_jwt_identity,
    create_refresh_token,
    jwt_refresh_token_required,
    get_raw_jwt,
)
from sqlalchemy.exc import IntegrityError


BASEDIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret-key"
app.config["JWT_SECRET_KEY"] = "encrypt"
app.config["DEBUG"] = True
app.config["ENV"] = "development"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(BASEDIR, "test.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']
db.init_app(app)
jwt = JWTManager(app)
blacklist = set()
bcrypt = Bcrypt(app)
Migrate = Migrate(app, db)
CORS(app)


Manager = Manager(app)
Manager.add_command("db", MigrateCommand)


@app.route("/login", methods=["POST"])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    if not email:
        return jsonify({"msg": "Missing email parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    user = User.query.filter_by(email=email).first()

    if user is None:
        return jsonify({"msg": "Email not found"}), 404

    if bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=email)
        data = {
            "access_token": access_token,
            "msg": "success",
        }
        auth = Auth()
        auth.token = access_token
        auth.is_valid = True
        auth.created_at = datetime.datetime.now()
        auth.login_user_id = user.user_id

        db.session.add(auth)
        db.session.commit()

        return jsonify(data), 200


@app.route('/protected', methods=['GET'])
@jwt_required
def protected():
    # Access the identity of the current user with get_jwt_identity
    user = get_jwt_identity()
    return jsonify(logged_in_as=user), 200


@jwt.expired_token_loader
def my_expired_token_callback(expired_token):
    token_type = expired_token['type']
    return jsonify({
        'status': 401,
        'sub_status': 42,
        'msg': 'La sesión del token {} ha expirado'.format(token_type)
    }), 
    
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in blacklist


@app.route("/signup", methods=["POST"])
def signup():
    # Regular expression that checks a valid email
    ereg = "^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$"
    # Regular expression that checks a valid password
    preg = "^.*(?=.{8,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).*$"
    # Instancing the a new user
    user = User()
    # Checking email
    if re.search(ereg, request.json.get("email")):
        user.email = request.json.get("email")
    else:
        return "Invalid email format", 400
    # Checking password
    if re.search(preg, request.json.get("password")):
        pw_hash = bcrypt.generate_password_hash(request.json.get("password"))
        user.password = pw_hash
    else:
        return "Invalid password format", 400
    # Ask for everything else
    user.name = request.json.get("name")
    user.last_name = request.json.get("last_name")
    user.birthday_date = request.json.get("birthday_date")

    db.session.add(user)

    db.session.commit()

    return jsonify({"success": True}), 201


@app.route("/user/<int:user_id>", methods=["DELETE", "GET", "PUT"])
@app.route("/users", methods=["GET"])
@jwt_required
def user(user_id=None):
    if request.method == "GET":
        if user_id is not None:
            user = User.query.get(user_id)
            return jsonify(user.serialize()), 200
        else:
            users = User.query.all()
            users_list = [user.serialize() for user in users]
            return jsonify(users_list), 200

    if request.method == "DELETE":
        user = User.query.get(user_id)
        db.session.delete(user)
        db.session.commit()
        return "User has been deleted", 200

    if request.method == "PUT":
        if user_id is not None:
            user = User.query.get(user_id)
            user.name = request.json.get("name")
            user.last_name = request.json.get("last_name")
            user.email = request.json.get("email")
            user.birthday_date = request.json.get("birthday_date")
            db.session.commit()
            return jsonify(user.serialize()), 201


@app.route("/categories", methods=["GET", "POST"])
@app.route("/categories/<int:category_id>", methods=["DELETE"])
def category_handler(category_id=None):
    if request.method == "GET":
        categories = Category.query.all()
        categories_list = [category.serialize() for category in categories]
        return jsonify(categories_list), 200

    if request.method == "POST":
        category = Category()
        category.category_name = request.json.get("category_name")

        db.session.add(category)
        db.session.commit()
        return jsonify(category.serialize()), 201

    if request.method == "DELETE":
        if category_id is not None:
            category = Category.query.get(category_id)
            db.session.delete(category)
            db.session.commit()
            return jsonify({"msg": "Field has been deleted"}), 201


@app.route("/event", methods=["POST", "GET"])
@app.route("/event/<int:event_id>", methods=["DELETE", "GET"])
def event(event_id=None):
    if request.method == "GET":
        if event_id is None:
            events = Event.query.all()
            events_list = [event.serialize() for event in events]
            return jsonify(events_list), 200
        if event_id is not None:
            event = Event.query.get(event_id)
            return jsonify(event.serialize()), 200

    if request.method == "DELETE":
        if event_id is not None:
            event = Event.query.get(event_id)
            db.session.delete(event)
            db.session.commit()
            return jsonify({"msg": "Field has been deleted"}), 201

    if request.method == "POST":
        event = Event()
        event.event_name = request.json.get("event_name")
        event.description = request.json.get("description")
        event.start_time = request.json.get("start_time")
        event.end_time = request.json.get("end_time")
        event.city = request.json.get("city")
        event.street = request.json.get("street")
        event.lat = request.json.get("lat")
        event.longi = request.json.get("longi")
        event.ticket_url = request.json.get("ticket_url")
        event.is_canceled = request.json.get("is_canceled")


        db.session.add(event)

        db.session.commit()
        return "Success", 200


@app.route("/calendars", methods=["POST", "GET"])
@app.route("/calendars/<int:calendar_id>", methods=["GET", "PUT", "DELETE"])
def calendar_handler(calendar_id=None):
    if request.method == "GET":
        if calendar_id is None:
            calendars = Calendar.query.all()
            calendars_list = [calendar.serialize() for calendar in calendars]
            return jsonify(calendars_list), 200
        if calendar_id is not None:
            calendar = Calendar.query.get(calendar_id)
            return jsonify(calendar.serialize()), 200

    if request.method == "POST":
        calendar = Calendar()
        calendar.name = request.json.get("name_calendar")
        calendar.description = request.json.get("description")
        calendar.calendar_id_owner = request.json.get("calendar_id_owner")

        db.session.add(calendar)
        db.session.commit()
        return jsonify(calendar.serialize()), 201

    if calendar_id is not None:
        if request.method == "PUT":
            calendar = Calendar.query.get(calendar_id)
            calendar.name = request.json.get("name_calendar")
            calendar.description = request.json.get("description")
            db.session.commit()
            return jsonfify(calendar.serialize()), 201

        if request.method == "DELETE":
            calendar = Calendar.query.get(calendar_id)
            db.session.delete(calendar)
            db.session.commit()
            return jsonify({"msg": "Calendar has been deleted"}), 201


@app.route("/user/<int:user_id>/category/<int:category_id>", methods=["GET", "PUT", "DELETE"])
def favcategories(user_id, category_id):
    user_query = User.query.get(user_id)
    category_query = Category.query.get(category_id)
    if request.method == "PUT":
        user_query.favs.append(category_query)
        db.session.commit()
        return jsonify({"msg": "Category added"}), 201

    if request.method == "DELETE":
        user_query.favs.remove(category_query)
        db.session.commit()
        return jsonify({"msg": "category deleted"}), 201


@app.route("/calendar/<int:calendar_id>/event/<int:event_id>", methods=["PUT", "DELETE"])
def attendance(calendar_id, event_id):
    calendar_query = Calendar.query.get(calendar_id)
    event_query = Event.query.get(event_id)
    if request.method == "PUT":
        calendar_query.events_assistance.append(event_query)
        db.session.commit()
        return jsonify({"msg": "Event saved"}), 201

    if request.method == "DELETE":
        calendar_query.events_assistance.remove(event_query)
        db.session.commit()
        return jsonify({"msg": "Event deleted from calendar"}), 201


@app.route("/facebookusers", methods=["GET", "POST", "DELETE"])
def facebookusers():
    if request.method == "GET":
        facebook_users = Facebook.query.all()
        fbusers_list = [users.serialize() for users in facebook_users]
        return jsonify(fbusers_list), 200

    if request.method == "POST":
        facebook = Facebook()
        facebook.user_id = request.json.get("user_id")
        facebook.name = request.json.get("name")
        facebook.last_name = request.json.get("last_name")
        facebook.email = request.json.get("email")

        db.session.add(facebook)
        db.session.commit()
        return jsonify(facebook.serialize()), 201


@app.route('/logout', methods=['DELETE'])
@jwt_required
def logout():
    jti = get_raw_jwt()['jti']
    blacklist.add(jti)
    return jsonify({"msg": "Te has deslogueado exitosamente"}), 200


if __name__ == "__main__":
    Manager.run()
