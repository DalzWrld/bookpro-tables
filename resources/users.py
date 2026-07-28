from flask import make_response, request
from flask_restful import Resource
from marshmallow import ValidationError

from extensions import log
from models import User, db
from schemas import user_schema, users_schema


class Users(Resource):
    def get(self):
        users = User.query.all()
        log.info("get_all_users", request_data=users_schema.dump(users))

        return make_response(users_schema.dump(users), 200)

    def post(self):
        try:
            data = request.get_json()
            validated_data = user_schema.load(data)

            if User.query.filter_by(email=validated_data["email"]).first():
                return make_response(
                    {"status": 409, "message": "Email address already taken"}, 409
                )
            if User.query.filter_by(phone=validated_data["phone"]).first():
                return make_response(
                    {"status": 409, "message": "Phone number already taken"}, 409
                )

            user = User(
                first_name=validated_data["first_name"],
                last_name=validated_data["last_name"],
                email=validated_data["email"],
                phone=validated_data["phone"],
            )

            db.session.add(user)
            db.session.commit()

            return make_response(user_schema.dump(user), 201)
        
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



class UserByID(Resource):
    def get(self, id):
        user = User.query.filter_by(id=id).first()

        if user:
            return make_response(user_schema.dump(user), 200)
        else:
            response = {
                "status": 404, 
                "message": "User not found"
            }

            return make_response(response, 404)


    def put(self, id):
        user = User.query.get_or_404(id)

        try:
            data = user_schema.load(request.get_json(), partial=True)

            for key, value in data.items():
                setattr(user, key, value)

            db.session.commit()

            return make_response(user_schema.dump(user), 200)

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
        user = User.query.filter_by(id=id).first()

        if user:
            db.session.delete(user)
            db.session.commit()

            response = {
                "message": "User deleted successfully"
            }

            return make_response(response, 200)
        else:
            response = {
                "status": 404,
                "message": "User not found"
            }
            
            return make_response(response, 404)