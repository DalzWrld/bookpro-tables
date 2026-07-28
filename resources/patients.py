from flask import make_response, request
from flask_restful import Resource
from marshmallow import ValidationError

from extensions import log
from models import Patient, db
from schemas import patient_schema, patients_list_schema


class Patients(Resource):
    def get(self):
        patients = Patient.query.all()
        log.info("get_all_patients", request_data=patients_list_schema.dump(patients))

        return make_response(patients_list_schema.dump(patients), 200)

    def post(self):
        try:
            data = request.get_json()
            validated_data = patient_schema.load(data)

            if Patient.query.filter_by(phone=validated_data["phone"]).first():
                return make_response(
                    {"status": 409, "message": "Phone number already taken"}, 409
                )

            patient = Patient(
                user_id=validated_data["user_id"],
                first_name=validated_data["first_name"],
                last_name=validated_data["last_name"],
                dob=validated_data["dob"],
                gender=validated_data["gender"],
                address=validated_data["address"],
                phone=validated_data["phone"],
            )

            db.session.add(patient)
            db.session.commit()

            return make_response(patient_schema.dump(patient), 201)

        except ValidationError as err:
            log.error("validation_error", errors=err.messages)

            response = {
                "status": 400,
                "message": "Validation error(s) occurred",
                "errors": {**err.messages},
            }

            return make_response(response, 400)

        except ValueError as ve:
            db.session.rollback()
            log.error("value_error", error=str(ve))

            response = {
                "status": 400,
                "message": "Wrong value(s) entered.",
            }

            return make_response(response, 400)


class PatientByID(Resource):
    def get(self, id):
        patient = Patient.query.filter_by(id=id).first()

        if patient:
            return make_response(patient_schema.dump(patient), 200)
        else:
            response = {
                "status": 404,
                "message": "Patient not found"
            }

            return make_response(response, 404)

    def put(self, id):
        patient = Patient.query.get_or_404(id)

        try:
            data = patient_schema.load(request.get_json(), partial=True)

            for key, value in data.items():
                setattr(patient, key, value)

            db.session.commit()

            return make_response(patient_schema.dump(patient), 200)

        except ValidationError as err:
            log.error("validation_error", errors=err.messages)

            response = {
                "status": 400,
                "message": "Validation error(s) occurred",
                "errors": {**err.messages},
            }

            return make_response(response, 400)

        except ValueError as ve:
            db.session.rollback()
            log.error("value_error", error=str(ve))

            response = {
                "status": 400,
                "message": "Wrong value(s) entered.",
            }

            return make_response(response, 400)

    def delete(self, id):
        patient = Patient.query.filter_by(id=id).first()

        if patient:
            db.session.delete(patient)
            db.session.commit()

            response = {
                "message": "Patient deleted successfully"
            }

            return make_response(response, 200)
        else:
            response = {
                "status": 404,
                "message": "Patient not found"
            }

            return make_response(response, 404)
