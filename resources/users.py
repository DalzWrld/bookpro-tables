from flask import make_response, request
from flask_restful import Resource

# from marshmallow import ValidationError
from extensions import log
from models import User, db
from schemas import user_schema, users_schema


class Users(Resource):
    def get(self):
        users = User.query.all()
        log.info("get_all_users", request_data=users_schema.dump(users))

        return users_schema.dump(User.query.all()), 200

    def post(self):
        data = request.get_json()
        user = User(**data)
        db.session.add(user)
        db.session.commit()
        
        log.info("create_user", user_id=user.id)
        return user_schema.dump(user), 201


class UserByID(Resource):
    def get(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return {"message": "User not found"}, 404
        
        log.info("get_user_by_id", user_id=user_id)
        return user_schema.dump(user), 200

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