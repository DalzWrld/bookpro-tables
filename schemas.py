from marshmallow import Schema, ValidationError, fields, validates_schema


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    email = fields.Email(required=True, unique=True)
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

    doctor = fields.Nested("DoctorSchema", excludes=("user",))
    patient = fields.Nested("PatientSchema", excludes=("user",))

class DoctorSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    specialty = fields.Str()
    dob = fields.Date()
    gender = fields.Str()
    bio = fields.Str()
    phone = fields.Str(unique=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    appointments = fields.Nested("AppointmentSchema", many=True, exclude=("doctor",))
    reviews = fields.Nested("ReviewSchema", many=True, exclude=("doctor",))

class PatientSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    dob = fields.Date()
    gender = fields.Str()
    address = fields.Str()
    phone = fields.Str(unique=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

class HospitalSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    address = fields.Str()
    phone = fields.Str(unique=True)
    email = fields.Email(required=True, unique=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

class AppointmentSchema(Schema):
    id = fields.Int(dump_only=True)
    patient_id = fields.Int(required=True)
    doctor_id = fields.Int(required=True)
    hospital_id = fields.Int(required=True)
    appointment_date = fields.DateTime(required=True)
    status = fields.Str()
    notes = fields.Str()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

class ReviewSchema(Schema):
    id = fields.Int(dump_only=True)
    appointment_id = fields.Int(required=True)
    patient_id = fields.Int(required=True)
    doctor_id = fields.Int(required=True)
    rating = fields.Float(required=True)
    comment = fields.Str()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)