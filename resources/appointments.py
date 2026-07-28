from flask import make_response, request
from flask_restful import Resource
from marshmallow import ValidationError

from extensions import log
from models import Appointment, db
from schemas import appointment_schema, appointments_schema, appointments_list_schema


class Appointments(Resource):
    def get(self):
        appointments = Appointment.query.all()
        log.info("get_all_appointments", request_data=appointments_list_schema.dump(appointments))

        return make_response(appointments_list_schema.dump(appointments), 200)

    def post(self):
        try:
            data = request.get_json()
            validated_data = appointment_schema.load(data)

            appointment = Appointment(
                patient_id=validated_data["patient_id"],
                doctor_id=validated_data["doctor_id"],
                hospital_id=validated_data["hospital_id"],
                appointment_date=validated_data["appointment_date"],
                appointment_time=validated_data.get("appointment_time"),
                status=validated_data.get("status", "Scheduled"),
                notes=validated_data.get("notes"),
            )

            db.session.add(appointment)
            db.session.commit()

            return make_response(appointment_schema.dump(appointment), 201)

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


class AppointmentByID(Resource):
    def get(self, id):
        appointment = Appointment.query.filter_by(id=id).first()

        if appointment:
            return make_response(appointment_schema.dump(appointment), 200)
        else:
            response = {
                "status": 404,
                "message": "Appointment not found"
            }

            return make_response(response, 404)

    def put(self, id):
        appointment = Appointment.query.get_or_404(id)

        try:
            data = appointment_schema.load(request.get_json(), partial=True)

            for key, value in data.items():
                setattr(appointment, key, value)

            db.session.commit()

            return make_response(appointment_schema.dump(appointment), 200)

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
        appointment = Appointment.query.filter_by(id=id).first()

        if appointment:
            db.session.delete(appointment)
            db.session.commit()

            response = {
                "message": "Appointment deleted successfully"
            }

            return make_response(response, 200)
        else:
            response = {
                "status": 404,
                "message": "Appointment not found"
            }

            return make_response(response, 404)
