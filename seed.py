from app import app
from models import db, User, Doctor, Patient, Hospital, Appointment, Review
from datetime import date, time

with app.app_context():
    db.session.query(User).delete()
    db.session.query(Doctor).delete()
    db.session.query(Patient).delete()
    db.session.query(Hospital).delete()
    db.session.query(Appointment).delete()
    db.session.query(Review).delete()

    # Users
    users = [
        User(first_name="John", last_name="Doe", role="Admin", email="john.doe@gmail.com", phone="0712345678"),
        User(first_name="Jane", last_name="Smith", role="Patient", email="jane.smith@gmail.com", phone="0723456789")
    ]
    db.session.add_all(users)
    db.session.commit()
    print(f"Seeded {len(users)} users")

    # Doctors
    doctors = [
        Doctor(user_id=1, first_name="Alice", last_name="Smith", specialty="Cardiology", bio="Cardiology specialist with 10 years of experience.", available=True, rating=4.5, phone="0734567890"),
        Doctor(user_id=1, first_name="Bob", last_name="Brown", specialty="Neurology", bio=None, available=True, rating=4.8, phone="0745678901")
    ]
    db.session.add_all(doctors)
    db.session.commit()
    print(f"Seeded {len(doctors)} doctors")

    # Patients
    patients = [
        Patient(user_id=1, first_name="Alice", last_name="Smith", dob=date(2003, 4, 20), gender="Female", address="123 Main Street", phone="0734567890"),
        Patient(user_id=2, first_name="Bob", last_name="Brown", dob=date(2004, 5, 15), gender="Male", address="456 Second Street", phone="0745678901")
    ]
    db.session.add_all(patients)
    db.session.commit()
    print(f"Seeded {len(patients)} patients")

    # Hospitals
    hospitals = [
        Hospital(name="City Hospital", address="789 Third Street", phone="0756789012", email="city.hospital@gmail.com", website="cityhospital.com"),
        Hospital(name="Green Clinic", address="321 Fourth Street", phone="0767890123", email="green.clinic@gmail.com", website="greenclinic.com")
    ]
    db.session.add_all(hospitals)
    db.session.commit()
    print(f"Seeded {len(hospitals)} hospitals")

    # Appointments
    appointments = [
        Appointment(patient_id=1, doctor_id=2, hospital_id=1, appointment_date=date(2024, 8, 15), appointment_time=time(10, 0), status="Scheduled", notes="Regular check-up"),
        Appointment(patient_id=2, doctor_id=2, hospital_id=1, appointment_date=date(2024, 8, 16), appointment_time=time(11, 30), status="Completed", notes="Follow-up visit")
    ]
    db.session.add_all(appointments)
    db.session.commit()
    print(f"Seeded {len(appointments)} appointments")

    # Reviews
    reviews = [
        Review(appointment_id=1, patient_id=2, doctor_id=2, rating=5.0, comment="Excellent care and attention to detail."),
        Review(appointment_id=2, patient_id=1, doctor_id=1, rating=4.5, comment="Very professional and helpful.")
    ]
    db.session.add_all(reviews)
    db.session.commit()
    print(f"Seeded {len(reviews)} reviews")