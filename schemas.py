from marshmallow import Schema, ValidationError, fields, validate, validates_schema


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    email = fields.Email(required=True)
    phone = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    doctor = fields.Nested("DoctorSchema", exclude=("user",), dump_only=True)
    patient = fields.Nested("PatientSchema", exclude=("user",), dump_only=True)

user_schema = UserSchema()
users_schema = UserSchema(many=True)

class UserListSchema(Schema):
    id = fields.Int(dump_only=True)
    first_name = fields.Str(dump_only=True)
    last_name = fields.Str(dump_only=True)
    email = fields.Email(dump_only=True)
    phone = fields.Str(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

users_list_schema = UserListSchema(many=True)

class DoctorSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    specialty = fields.Str(required=True, validate=validate.Length(min=1))
    bio = fields.Str(validate=validate.Length(max=250))
    available = fields.Bool()
    phone = fields.Str(required=True)
    years_practice = fields.Int(validate=validate.Range(min=0, max=100))
    rating = fields.Float(validate=validate.Range(min=0, max=5))
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    appointments = fields.Nested("AppointmentSchema", many=True, exclude=("doctor",), dump_only=True)
    reviews = fields.Nested("ReviewSchema", many=True, exclude=("doctor",), dump_only=True)

doctor_schema = DoctorSchema()
doctors_schema = DoctorSchema(many=True)

class DoctorListSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(dump_only=True)
    first_name = fields.Str(dump_only=True)
    last_name = fields.Str(dump_only=True)
    specialty = fields.Str(dump_only=True)
    bio = fields.Str(dump_only=True)
    available = fields.Bool(dump_only=True)
    phone = fields.Str(dump_only=True)
    years_practice = fields.Int(dump_only=True)
    rating = fields.Float(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

doctors_list_schema = DoctorListSchema(many=True)

class PatientSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    dob = fields.Date(required=True)
    gender = fields.Str(required=True, validate=validate.OneOf(["Male", "Female", "Other"]))
    address = fields.Str(required=True)
    phone = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    appointments = fields.Nested("AppointmentSchema", many=True, exclude=("patient",), dump_only=True)
    reviews = fields.Nested("ReviewSchema", many=True, exclude=("patient",), dump_only=True)

patient_schema = PatientSchema()
patients_schema = PatientSchema(many=True)

class PatientListSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(dump_only=True)
    first_name = fields.Str(dump_only=True)
    last_name = fields.Str(dump_only=True)
    dob = fields.Date(dump_only=True)
    gender = fields.Str(dump_only=True)
    address = fields.Str(dump_only=True)
    phone = fields.Str(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

patients_list_schema = PatientListSchema(many=True)

class HospitalSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    address = fields.Str(required=True)
    phone = fields.Str(required=True)
    email = fields.Email(required=True)
    website = fields.Str()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    appointments = fields.Nested("AppointmentSchema", many=True, exclude=("hospital",), dump_only=True)

hospital_schema = HospitalSchema()
hospitals_schema = HospitalSchema(many=True)

class HospitalListSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(dump_only=True)
    address = fields.Str(dump_only=True)
    phone = fields.Str(dump_only=True)
    email = fields.Email(dump_only=True)
    website = fields.Str(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

hospitals_list_schema = HospitalListSchema(many=True)

class AppointmentSchema(Schema):
    id = fields.Int(dump_only=True)
    patient_id = fields.Int(required=True)
    doctor_id = fields.Int(required=True)
    hospital_id = fields.Int(required=True)
    appointment_date = fields.DateTime(required=True)
    appointment_time = fields.Time(required=True)
    status = fields.Str(required=True, validate=validate.OneOf(["Scheduled", "Completed", "Cancelled"]))
    notes = fields.Str(validate=validate.Length(max=500))
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    patient = fields.Nested("PatientSchema", exclude=("appointments", "reviews"), dump_only=True)
    doctor = fields.Nested("DoctorSchema", exclude=("appointments", "reviews"), dump_only=True)
    hospital = fields.Nested("HospitalSchema", exclude=("appointments",), dump_only=True)

appointment_schema = AppointmentSchema()
appointments_schema = AppointmentSchema(many=True)

class AppointmentListSchema(Schema):
    id = fields.Int(dump_only=True)
    patient_id = fields.Int(dump_only=True)
    doctor_id = fields.Int(dump_only=True)
    hospital_id = fields.Int(dump_only=True)
    appointment_date = fields.DateTime(dump_only=True)
    appointment_time = fields.Time(dump_only=True)
    status = fields.Str(dump_only=True)
    notes = fields.Str(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

appointments_list_schema = AppointmentListSchema(many=True)

class ReviewSchema(Schema):
    id = fields.Int(dump_only=True)
    appointment_id = fields.Int(required=True)
    patient_id = fields.Int(required=True)
    doctor_id = fields.Int(required=True)
    rating = fields.Float(required=True, validate=validate.Range(min=1, max=5))
    comment = fields.Str(validate=validate.Length(max=500))
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    patient = fields.Nested("PatientSchema", exclude=("appointments", "reviews"), dump_only=True)
    doctor = fields.Nested("DoctorSchema", exclude=("appointments", "reviews"), dump_only=True)

review_schema = ReviewSchema()
reviews_schema = ReviewSchema(many=True)

class ReviewListSchema(Schema):
    id = fields.Int(dump_only=True)
    appointment_id = fields.Int(dump_only=True)
    patient_id = fields.Int(dump_only=True)
    doctor_id = fields.Int(dump_only=True)
    rating = fields.Float(dump_only=True)
    comment = fields.Str(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

reviews_list_schema = ReviewListSchema(many=True)


class LoginSchema(Schema):
    email_address = fields.Email(required=True)
    password = fields.Str(load_only=True)

login_schema = LoginSchema()


class RegisterSchema(Schema):
    id = fields.Int(dump_only=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    email_address = fields.Email(required=True)
    phone = fields.Str(required=True)
    password = fields.Str(load_only=True, validate=validate.Length(min=8))
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    @validates_schema
    def validate_schema(self, data, **kwargs):
        errors = {}
        if all(key in data for key in ["first_name", "last_name", "phone"]):
            if len(data["first_name"]) < 1:
                errors["first_name"] = ["Firstname is required"]
            if len(data["last_name"]) < 1:
                errors["last_name"] = ["Lastname is required"]
            if len(data["phone"]) != 10:
                errors["phone"] = ["phone number must be 10 characters"]
        if errors:
            raise ValidationError(errors)

register_schema = RegisterSchema()