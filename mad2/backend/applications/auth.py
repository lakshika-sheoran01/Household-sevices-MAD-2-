from flask import request, jsonify
from flask_restful import Resource
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token
from .models import User


class UserLogin(Resource):
    def post(self):
        data = request.json
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return {"message": "Username and password are required."}, 400

        
        user = User.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.user_password, password):
            return {"message": "Invalid username or password."}, 401

        if not user.approval_status:
            return {"message": "Your account has been flagged or not yet approved. Please contact support for assistance."}, 403

        access_token = create_access_token(identity=username)

        if user.customer_status:
            print(user.customer_status)
            return jsonify({
                "message": "Login successful.",
                "access_token": access_token,
                "user_role": "customer"
            })
        elif user.professional_status:
            if not user.service_id:
                return {"message": "Your selected service is not available. Please create a new account with a valid service."}, 400
            return jsonify({
                "message": "Login successful.",
                "access_token": access_token,
                "user_role": "professional"
            })
        else:
            return {"message": "Invalid user role."}, 403

