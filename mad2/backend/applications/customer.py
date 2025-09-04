from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request, jsonify
from werkzeug.security import generate_password_hash
from datetime import datetime
from .models import db, User, HouseholdRequest, HouseholdServices
from .admin import cache
# ---------------------------- Customer Registration ----------------------------
class CustomerProfileManagement(Resource):
    def post(self):
        data = request.json
        username = data.get('username')
        password = data.get('password')
        address = data.get('address')
        postal_code = data.get('postal_code')

        if not all([username, password, address, postal_code]):
            return {"message": "All fields are required."}, 400

        if User.query.filter_by(username=username).first():
            return {"message": "User already exists. Choose a different username."}, 400

        new_user = User(
            username=username,
            user_password=generate_password_hash(password),
            customer_status=True,
            approval_status=True,
            user_address=address,
            postal_code=postal_code
        )
        db.session.add(new_user)
        db.session.commit()
        return {"message": "Registration successful. Please log in."}, 201

    @jwt_required()
    def put(self):
        current_user = get_jwt_identity()
        customer = User.query.filter_by(username=current_user, customer_status=True).first()
        if not customer:
            return {"message": "Customer not found or unauthorized."}, 403

        data = request.json
        print(request.json)
        username = data.get('username')
        password = data.get('password') if data.get('password') else customer.user_password
        address = data.get('user_address')
        postal_code = data.get('postal_code')

        if not all([username, password, address, postal_code]):
            return {"message": "All fields are required."}, 400

        if User.query.filter(User.username == username, User.id != customer.id).first():
            return {"message": "Username already taken."}, 400

        customer.username = username
        customer.user_password = generate_password_hash(password)
        customer.user_address = address
        customer.postal_code = postal_code
        
        db.session.commit()
        return {"message": "Profile updated successfully."}, 200


# ---------------------------- Customer Dashboard ----------------------------
class CustomerDashboard(Resource):
    @jwt_required()
    @cache.cached(timeout=100)
    def get(self):
        current_user = get_jwt_identity()
        customer = User.query.filter_by(username=current_user, customer_status=True).first()
        if not customer:
            return {"message": "Customer not found or unauthorized."}, 403

        services = HouseholdServices.query.all()
        service_history = HouseholdRequest.query.filter_by(client_id=customer.id).all()

        service_history_data = [
            {
                "id": req.id,
                "service_title": req.service.service_title,
                "professional_name": req.professional.username if req.professional else None,
                "details": req.details,
                "request_status": req.request_status,
                "created_at": req.created_at.isoformat() if req.created_at else None,
                "closed_at": req.closed_at.isoformat() if req.closed_at else None,
                "customer_rating": req.customer_rating,
                "customer_review": req.customer_review
            }
            for req in service_history
        ]

        return jsonify({
            "message": "Customer dashboard data retrieved successfully.",
            'services': [{'id': s.id, 'service_title': s.service_title, 'service_details': s.service_details, 'duration_required': s.duration_required, 'starting_price': s.starting_price} for s in services],
            "customer": {
                "id": customer.id,
                "username": customer.username,
                "user_address": customer.user_address,
                "postal_code": customer.postal_code
            },
            "service_history": service_history_data
        })
    
# ---------------------------- Request Service ----------------------------
class CustomerServiceRequestManagment(Resource):
    @jwt_required()
    @cache.cached(timeout=100)
    def get(self, service_id):
        current_user_username = get_jwt_identity()
        customer = User.query.filter_by(username=current_user_username).first()
        if not customer:
            return {"message": "Customer not found."}, 404
        if not customer.customer_status:
            return {"message": "Access denied. You are not a customer."}, 403

        service = HouseholdServices.query.get(service_id)
        if not service:
            return {"message": "Service not found."}, 404

        professionals = User.query.filter_by(professional_status=True, approval_status=True, service_id=service_id).all()
        professionals_data = [{
            "id": professional.id,
            "username": professional.username,
            "professional_experience_level": professional.professional_experience_level,
            "rating_total": professional.rating_total,
            "average_rating": professional.average_rating
        } for professional in professionals]

        return jsonify({
            "message": "Service and professionals data retrieved successfully.",
            "service": {
                "id": service.id,
                "service_title": service.service_title,
                "service_details": service.service_details,
                "duration_required": service.duration_required,
                "starting_price": service.starting_price
            },
            "professionals": professionals_data
        })
    @jwt_required()
    def post(self, service_id):
        current_user = get_jwt_identity()
        customer = User.query.filter_by(username=current_user, customer_status=True).first()
        if not customer:
            return {"message": "Customer not found or unauthorized."}, 403

        data = request.json
        professional_username = data.get('professional')
        request_details = data.get('details')

        if not all([professional_username, request_details]):
            return {"message": "All fields are required."}, 400

        professional = User.query.filter_by(username=professional_username, professional_status=True, approval_status=True).first()
        if not professional:
            return {"message": "Professional not found or unavailable."}, 400

        new_request = HouseholdRequest(
            client_id=customer.id,
            professional_id=professional.id,
            service_id=service_id,
            details=request_details,
            request_status="Pending",
            request_type="Private"
        )
        db.session.add(new_request)
        db.session.commit()
        return {"message": "Service request sent successfully."}, 201
    
    @jwt_required()
    def patch(self, request_id):
        current_user = get_jwt_identity()
        customer = User.query.filter_by(username=current_user, customer_status=True).first()
        if not customer:
            return {"message": "Customer not found or unauthorized."}, 403

        service_request = HouseholdRequest.query.get(request_id)
        if not service_request or service_request.client_id != customer.id:
            return {"message": "Request not found or unauthorized action."}, 403

        service_request.request_status = "Closed"
        service_request.closed_at = datetime.utcnow()
        db.session.commit()
        return {"message": "Service marked as done successfully."}, 200

    @jwt_required()
    def put(self, request_id):
        current_user = get_jwt_identity()
        customer = User.query.filter_by(username=current_user, customer_status=True).first()
        if not customer:
            return {"message": "Customer not found or unauthorized."}, 403

        service_request = HouseholdRequest.query.get(request_id)
        if not service_request or service_request.client_id != customer.id:
            return {"message": "Request not found or unauthorized action."}, 403

        data = request.json
        rating = data.get("rating")
        review = data.get("review")

        if not rating or not (1 <= int(rating) <= 5):
            return {"message": "Invalid rating. Provide a value between 1 and 5."}, 400

        service_request.customer_rating = float(rating)
        service_request.customer_review = review
        db.session.commit()
        return {"message": "Thank you for your feedback!"}, 200
