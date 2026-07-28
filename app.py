import os

from dotenv import load_dotenv
from flask import Flask, make_response, request, session
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api

from extensions import log
from models import db
from resources.appointments import AppointmentByID, Appointments
from resources.doctors import DoctorByID, Doctors
from resources.hospitals import HospitalByID, Hospitals
from resources.patients import PatientByID, Patients
from resources.reviews import ReviewByID, Reviews
from resources.users import UserByID, Users

load_dotenv()

app = Flask(__name__)

bcrypt = Bcrypt(app=app)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

app.config["SESSION_COOKIE_SAMESITE"] = os.environ.get("SESSION_COOKIE_SAMESITE")
app.config["SESSION_COOKIE_SECURE"] = os.environ.get("SESSION_COOKIE_SECURE")
app.config["SESSION_COOKIE_HTTPONLY"] = os.environ.get("SESSION_COOKIE_HTTPONLY")

migrate = Migrate(app=app, db=db)

CORS_ORIGINS = os.environ.get("ALLOWED_ORIGINS", "").split(",")
CORS(app, supports_credentials=True, origins=[origin.strip() for origin in CORS_ORIGINS if origin.strip()])

db.init_app(app=app)

api = Api(app=app)

@app.before_request
def log_request():
    log.info(
        "request",
        method=request.method,
        content_type=request.headers.get("Content-Type"),
    )

PUBLIC_ENDPOINTS = ["login", "register"]
@app.before_request
def check_if_authenticated():
    if not session.get("user_id") and request.endpoint not in PUBLIC_ENDPOINTS:
        response = {
            "status": 401,
            "message": "Not authenticated. Login to access resource."
        }
        return make_response(response, 401)

    

api.add_resource(Users, '/users')
api.add_resource(UserByID, '/users/<int:id>')

api.add_resource(Doctors, '/doctors')
api.add_resource(DoctorByID, '/doctors/<int:id>')

api.add_resource(Patients, '/patients')
api.add_resource(PatientByID, '/patients/<int:id>')

api.add_resource(Hospitals, '/hospitals')
api.add_resource(HospitalByID, '/hospitals/<int:id>')

api.add_resource(Appointments, '/appointments')
api.add_resource(AppointmentByID, '/appointments/<int:id>')

api.add_resource(Reviews, '/reviews')
api.add_resource(ReviewByID, '/reviews/<int:id>')

if __name__ == '__main__':
    app.run(debug=True)
