from flask import make_response, request
from flask_restful import Resource
from marshmallow import ValidationError

from extensions import log
from models import Doctor, db
from schemas import doctor_schema, doctors_list_schema


class Doctors(Resource):
    def get(self):
        doctors = Doctor.query.all()
        log.info("get_all_doctors", request_data=doctors_list_schema.dump(doctors))

        return make_response(doctors_list_schema.dump(doctors), 200)

    def post(self):
        try:
            data = request.get_json()
            validated_data = doctor_schema.load(data)

            if Doctor.query.filter_by(phone=validated_data["phone"]).first():
                return make_response(
                    {"status": 409, "message": "Phone number already taken"}, 409
                )

            doctor = Doctor(
                user_id=validated_data["user_id"],
                first_name=validated_data["first_name"],
                last_name=validated_data["last_name"],
                specialty=validated_data["specialty"],
                bio=validated_data.get("bio"),
                available=validated_data.get("available", True),
                phone=validated_data["phone"],
                years_practice=validated_data.get("years_practice", 0),
            )

            if "rating" in validated_data:
                doctor.rating = validated_data["rating"]

            db.session.add(doctor)
            db.session.commit()

            return make_response(doctor_schema.dump(doctor), 201)

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


class DoctorByID(Resource):
    def get(self, id):
        doctor = Doctor.query.filter_by(id=id).first()

        if doctor:
            return make_response(doctor_schema.dump(doctor), 200)
        else:
            response = {
                "status": 404,
                "message": "Doctor not found"
            }

            return make_response(response, 404)

    def put(self, id):
        doctor = Doctor.query.get_or_404(id)

        try:
            data = doctor_schema.load(request.get_json(), partial=True)

            for key, value in data.items():
                setattr(doctor, key, value)

            db.session.commit()

            return make_response(doctor_schema.dump(doctor), 200)

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
        doctor = Doctor.query.filter_by(id=id).first()

        if doctor:
            db.session.delete(doctor)
            db.session.commit()

            response = {
                "message": "Doctor deleted successfully"
            }

            return make_response(response, 200)
        else:
            response = {
                "status": 404,
                "message": "Doctor not found"
            }

            return make_response(response, 404)
