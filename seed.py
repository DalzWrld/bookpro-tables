from datetime import date, time

from app import app
from models import Appointment, Doctor, Hospital, Patient, Review, User, db

with app.app_context():
    Review.query.delete()
    Appointment.query.delete()
    Doctor.query.delete()
    Patient.query.delete()
    Hospital.query.delete()
    User.query.delete()
    db.session.commit()

    users = [
        User(first_name="John", last_name="Doe", role="Admin", email="john.doe@example.com", phone="0712345678"),
        User(first_name="Jane", last_name="Smith", role="Doctor", email="jane.smith@example.com", phone="0712345679"),
        User(first_name="Michael", last_name="Mwangi", role="Doctor", email="michael.mwangi@example.com", phone="0712345680"),
        User(first_name="Sarah", last_name="Akinyi", role="Doctor", email="sarah.akinyi@example.com", phone="0712345681"),
        User(first_name="Daniel", last_name="Otieno", role="Patient", email="daniel.otieno@example.com", phone="0712345682"),
        User(first_name="Grace", last_name="Wanjiku", role="Patient", email="grace.wanjiku@example.com", phone="0712345683"),
        User(first_name="Lilian", last_name="Kariuki", role="Patient", email="lilian.kariuki@example.com", phone="0712345684"),
        User(first_name="Kevin", last_name="Njoroge", role="Patient", email="kevin.njoroge@example.com", phone="0712345685"),
    ]
    db.session.add_all(users)
    db.session.commit()
    user_ids = [user.id for user in users]
    print(f"Seeded {len(users)} users")

    doctors = [
        Doctor(user_id=user_ids[1], first_name="Jane", last_name="Smith", specialty="Cardiology", bio="Cardiology specialist with 10 years of experience.", available=True, rating=4.7, phone="0734567890"),
        Doctor(user_id=user_ids[2], first_name="Michael", last_name="Mwangi", specialty="Neurology", bio="Skilled neurologist focused on preventive care.", available=True, rating=4.8, phone="0734567891"),
        Doctor(user_id=user_ids[3], first_name="Sarah", last_name="Akinyi", specialty="Pediatrics", bio="Compassionate pediatrician with a calm bedside manner.", available=False, rating=4.6, phone="0734567892"),
    ]
    db.session.add_all(doctors)
    db.session.commit()
    doctor_ids = [doctor.id for doctor in doctors]
    print(f"Seeded {len(doctors)} doctors")

    patients = [
        Patient(user_id=user_ids[4], first_name="Daniel", last_name="Otieno", dob=date(2003, 4, 20), gender="Male", address="123 Main Street", phone="0745678900"),
        Patient(user_id=user_ids[5], first_name="Grace", last_name="Wanjiku", dob=date(2004, 5, 15), gender="Female", address="456 Second Street", phone="0745678901"),
        Patient(user_id=user_ids[6], first_name="Lilian", last_name="Kariuki", dob=date(2001, 7, 10), gender="Female", address="789 Third Street", phone="0745678902"),
        Patient(user_id=user_ids[7], first_name="Kevin", last_name="Njoroge", dob=date(1998, 11, 3), gender="Male", address="321 Fourth Street", phone="0745678903"),
    ]
    db.session.add_all(patients)
    db.session.commit()
    patient_ids = [patient.id for patient in patients]
    print(f"Seeded {len(patients)} patients")

    hospitals = [
        Hospital(name="City Hospital", address="789 Third Street", phone="0756789012", email="city.hospital@example.com", website="cityhospital.com"),
        Hospital(name="Green Clinic", address="321 Fourth Street", phone="0756789013", email="green.clinic@example.com", website="greenclinic.com"),
        Hospital(name="Sunrise Medical Center", address="654 River Road", phone="0756789014", email="sunrise.med@example.com", website="sunrisemedical.co.ke"),
    ]
    db.session.add_all(hospitals)
    db.session.commit()
    hospital_ids = [hospital.id for hospital in hospitals]
    print(f"Seeded {len(hospitals)} hospitals")

    appointments = [
        Appointment(patient_id=patient_ids[0], doctor_id=doctor_ids[0], hospital_id=hospital_ids[0], appointment_date=date(2026, 1, 15), appointment_time=time(10, 0), status="Scheduled", notes="Regular check-up"),
        Appointment(patient_id=patient_ids[1], doctor_id=doctor_ids[1], hospital_id=hospital_ids[0], appointment_date=date(2026, 1, 16), appointment_time=time(11, 30), status="Completed", notes="Follow-up visit"),
        Appointment(patient_id=patient_ids[2], doctor_id=doctor_ids[0], hospital_id=hospital_ids[1], appointment_date=date(2026, 2, 5), appointment_time=time(9, 15), status="Scheduled", notes="Pediatric consultation"),
        Appointment(patient_id=patient_ids[3], doctor_id=doctor_ids[2], hospital_id=hospital_ids[2], appointment_date=date(2026, 2, 12), appointment_time=time(13, 0), status="Cancelled", notes="Rescheduled due to travel"),
        Appointment(patient_id=patient_ids[0], doctor_id=doctor_ids[1], hospital_id=hospital_ids[2], appointment_date=date(2026, 3, 2), appointment_time=time(15, 45), status="Scheduled", notes="Neurology review"),
        Appointment(patient_id=patient_ids[2], doctor_id=doctor_ids[2], hospital_id=hospital_ids[1], appointment_date=date(2026, 3, 10), appointment_time=time(8, 30), status="Completed", notes="Routine wellness visit"),
    ]
    db.session.add_all(appointments)
    db.session.commit()
    appointment_ids = [appointment.id for appointment in appointments]
    print(f"Seeded {len(appointments)} appointments")

    reviews = [
        Review(appointment_id=appointment_ids[0], patient_id=patient_ids[0], doctor_id=doctor_ids[0], rating=5.0, comment="Excellent care and attention to detail."),
        Review(appointment_id=appointment_ids[1], patient_id=patient_ids[1], doctor_id=doctor_ids[1], rating=4.5, comment="Very professional and helpful."),
        Review(appointment_id=appointment_ids[2], patient_id=patient_ids[2], doctor_id=doctor_ids[0], rating=4.8, comment="Friendly staff and clear instructions."),
        Review(appointment_id=appointment_ids[5], patient_id=patient_ids[2], doctor_id=doctor_ids[2], rating=5.0, comment="Great bedside manner and quick follow-up."),
    ]
    db.session.add_all(reviews)
    db.session.commit()
    print(f"Seeded {len(reviews)} reviews")