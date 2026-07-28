from dotenv import load_dotenv
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_restful import Api

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

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///demo.db"

migrate = Migrate(app=app, db=db)

db.init_app(app=app)

api = Api(app=app)

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
