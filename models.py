from datetime import datetime

from flask_bcrypt import check_password_hash, generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=naming_convention)

db = SQLAlchemy(metadata=metadata)

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now)

    doctor = db.relationship('Doctor', uselist=False, back_populates='user')
    patient = db.relationship('Patient', uselist=False, back_populates='user')

    def set_password(self, user_pass):
        self.password = generate_password_hash(password=user_pass).decode("utf-8")

    def check_password(self, user_pass):
        return check_password_hash(self.password, user_pass)

    def __repr__(self):
        return f'<User {self.id}, {self.first_name} {self.last_name}, {self.email}, {self.phone}>'

class Doctor(db.Model):
    __tablename__ = "doctors"
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    specialty = db.Column(db.String(50), nullable=False)
    bio = db.Column(db.String(250), nullable=True)
    available = db.Column(db.Boolean, default=True, nullable=False)
    rating = db.Column(db.Float, nullable=True)
    phone = db.Column(db.String(10), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now)

    user = db.relationship('User', back_populates='doctor')
    appointments = db.relationship('Appointment', back_populates='doctor')
    reviews = db.relationship('Review', back_populates='doctor')

    def __repr__(self):
        return f'<Doctor {self.id}, {self.first_name} {self.last_name}, {self.specialty}, {self.bio}, {self.available}, {self.rating}, {self.phone}>'


class Patient(db.Model):
    __tablename__ = "patients"
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String, nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now)

    user = db.relationship('User', back_populates='patient')
    appointments = db.relationship('Appointment', back_populates='patient')
    reviews = db.relationship('Review', back_populates='patient')

    def __repr__(self):
        return f'<Patient {self.id}, {self.first_name} {self.last_name}, {self.dob}, {self.gender}, {self.address}, {self.phone}>'


class Hospital(db.Model):
    __tablename__ = "hospitals"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    website = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now)

    appointments = db.relationship('Appointment', back_populates='hospital')

    def __repr__(self):
        return f'<Hospital {self.id}, {self.name}, {self.address}, {self.phone}, {self.email}, {self.website}>'


class Appointment(db.Model):
    __tablename__ = "appointments"

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospitals.id'), nullable=False)
    appointment_date = db.Column(db.DateTime, nullable=False)
    appointment_time = db.Column(db.Time, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='scheduled')
    notes = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now)

    patient = db.relationship('Patient', back_populates='appointments')
    doctor = db.relationship('Doctor', back_populates='appointments')
    hospital = db.relationship('Hospital', back_populates='appointments')
    reviews = db.relationship('Review', back_populates='appointment')

    def __repr__(self):
        return f'<Appointment {self.id}, {self.patient_id}, {self.doctor_id}, {self.hospital_id}, {self.appointment_date}, {self.status}, {self.notes}>'


class Review(db.Model):
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    comment = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now)

    patient = db.relationship('Patient', back_populates='reviews')
    doctor = db.relationship('Doctor', back_populates='reviews')
    appointment = db.relationship('Appointment', back_populates='reviews')

    def __repr__(self):
        return f'<Review {self.id}, {self.patient_id}, {self.doctor_id}, {self.appointment_id}, {self.rating}, {self.comment}>'