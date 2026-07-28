from flask import make_response, request
from flask_restful import Resource
from marshmallow import ValidationError

from extensions import log
from models import Hospital, db
from schemas import hospital_schema, hospitals_schema


class Hospitals(Resource):
    def get(self):
        hospitals = Hospital.query.all()
        log.info("get_all_hospitals", request_data=hospitals_schema.dump(hospitals))

        return make_response(hospitals_schema.dump(hospitals), 200)

    def post(self):
        try:
            data = request.get_json()
            validated_data = hospital_schema.load(data)

            if Hospital.query.filter_by(phone=validated_data["phone"]).first():
                return make_response(
                    {"status": 409, "message": "Phone number already taken"}, 409
                )
            if Hospital.query.filter_by(email=validated_data["email"]).first():
                return make_response(
                    {"status": 409, "message": "Email address already taken"}, 409
                )

            hospital = Hospital(
                name=validated_data["name"],
                address=validated_data["address"],
                phone=validated_data["phone"],
                email=validated_data["email"],
                website=validated_data.get("website"),
            )

            db.session.add(hospital)
            db.session.commit()

            return make_response(hospital_schema.dump(hospital), 201)

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


class HospitalByID(Resource):
    def get(self, id):
        hospital = Hospital.query.filter_by(id=id).first()

        if hospital:
            return make_response(hospital_schema.dump(hospital), 200)
        else:
            response = {
                "status": 404,
                "message": "Hospital not found"
            }

            return make_response(response, 404)

    def put(self, id):
        hospital = Hospital.query.get_or_404(id)

        try:
            data = hospital_schema.load(request.get_json(), partial=True)

            for key, value in data.items():
                setattr(hospital, key, value)

            db.session.commit()

            return make_response(hospital_schema.dump(hospital), 200)

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
        hospital = Hospital.query.filter_by(id=id).first()

        if hospital:
            db.session.delete(hospital)
            db.session.commit()

            response = {
                "message": "Hospital deleted successfully"
            }

            return make_response(response, 200)
        else:
            response = {
                "status": 404,
                "message": "Hospital not found"
            }

            return make_response(response, 404)
