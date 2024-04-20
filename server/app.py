from flask import Flask , request, abort, jsonify, session
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_session import Session
from config import ApplicationConfig
from models import db, User
from create_schedule import create_schedule_dataframe,save_schedule_as_image
from create_vertex import create_graph_and_apply_coloring

app = Flask(__name__)
app.config.from_object(ApplicationConfig)

bcrypt = Bcrypt(app)
CORS(app, supports_credentials=True)
server_session = Session(app)
db.init_app(app)
with app.app_context():
    db.create_all()


@app.route("/register", methods=["POST"])
def register_user():
    email = request.json["email"]
    password = request.json["password"]

    user_exists = User.query.filter_by(email=email).first() is not None

    if user_exists:
        return jsonify({"error": "User already exists"}), 409

    hashed_password = bcrypt.generate_password_hash(password)
    new_user = User(email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    session["user_id"] = new_user.id

    return jsonify({
        "id": new_user.id,
        "email": new_user.email
    })


@app.route("/login", methods=["POST"])
def login_user():
    email = request.json["email"]
    password = request.json["password"]

    user = User.query.filter_by(email=email).first()

    if user is None:
        return jsonify({"error": "Unauthorized"}), 401

    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Unauthorized"}), 401

    session["user_id"] = user.id

    return jsonify({
        "id": user.id,
        "email": user.email
    })



def create_the_schedule():
    G, colors = create_graph_and_apply_coloring(get_current_user_id())
    df = create_schedule_dataframe(G, colors)
    save_schedule_as_image(df, 'weekly_schedule.png')

def get_current_user_id():
    user_id = session.get('user_id', None)
    if user_id is None:
        # Handle the case where there is no user logged in
        return None
    return user_id

if __name__ == "__main__":
    app.run()
    create_the_schedule()
