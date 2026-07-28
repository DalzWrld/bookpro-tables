from flask import make_response, request
from flask_restful import Resource
from marshmallow import ValidationError

from extensions import log
from models import Review, db
from schemas import review_schema, reviews_schema, reviews_list_schema


class Reviews(Resource):
    def get(self):
        reviews = Review.query.all()
        log.info("get_all_reviews", request_data=reviews_list_schema.dump(reviews))

        return make_response(reviews_list_schema.dump(reviews), 200)

    def post(self):
        try:
            data = request.get_json()
            validated_data = review_schema.load(data)

            review = Review(
                appointment_id=validated_data["appointment_id"],
                patient_id=validated_data["patient_id"],
                doctor_id=validated_data["doctor_id"],
                rating=validated_data["rating"],
                comment=validated_data.get("comment"),
            )

            db.session.add(review)
            db.session.commit()

            return make_response(review_schema.dump(review), 201)

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


class ReviewByID(Resource):
    def get(self, id):
        review = Review.query.filter_by(id=id).first()

        if review:
            return make_response(review_schema.dump(review), 200)
        else:
            response = {
                "status": 404,
                "message": "Review not found"
            }

            return make_response(response, 404)

    def put(self, id):
        review = Review.query.get_or_404(id)

        try:
            data = review_schema.load(request.get_json(), partial=True)

            for key, value in data.items():
                setattr(review, key, value)

            db.session.commit()

            return make_response(review_schema.dump(review), 200)

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
        review = Review.query.filter_by(id=id).first()

        if review:
            db.session.delete(review)
            db.session.commit()

            response = {
                "message": "Review deleted successfully"
            }

            return make_response(response, 200)
        else:
            response = {
                "status": 404,
                "message": "Review not found"
            }

            return make_response(response, 404)
