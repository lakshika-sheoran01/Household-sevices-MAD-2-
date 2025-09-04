from flask import request, jsonify
from flask_restful import Resource
from werkzeug.security import generate_password_hash
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from .models import User, HouseholdServices, HouseholdRequest, db
from .admin import cache
class ProfessionalProfileManagement(Resource):  
    def get(self):
        services = HouseholdServices.query.all()
        services_data = [{"id": s.id, "service_title": s.service_title} for s in services]
        return jsonify(services=services_data)

    def post(self):
        data = request.json
        username = data.get('username')
        password = data.get('password')
        address = data.get('address')
        professional_experience_level = data.get('professional_experience')
        postal_code = data.get('postal_code')
        service_title = data.get('service')

        if not all([username, password, address, professional_experience_level, postal_code, service_title]):
            return {"message": "All fields are required."}, 400

        service = HouseholdServices.query.filter_by(service_title=service_title).first()
        if not service:
            return {"message": "Invalid service selected."}, 400

        if User.query.filter_by(username=username).first():
            return {"message": "Username already exists."}, 400

        new_user = User(
            username=username,
            user_password=generate_password_hash(password),
            user_address=address,
            postal_code=postal_code,
            professional_experience_level=professional_experience_level,
            service_id=service.id,
            professional_status=True,
            approval_status=False
        )

        db.session.add(new_user)
        db.session.commit()
        return {"message": "Registration successful. Please wait for admin approval."}, 201


    @jwt_required()
    def put(self):
        username = get_jwt_identity()
        professional = User.query.filter_by(username=username).first()
        if not professional or not professional.professional_status:
            return {"message": "Access denied."}, 403

        data = request.json
        address = data.get('address')
        postal_code = data.get('postal_code')
        experience_level = data.get('experience')

        if not all([address, postal_code, experience_level]):
            return {"message": "All fields are required."}, 400

        professional.user_address = address
        professional.postal_code = postal_code
        professional.professional_experience_level = experience_level
        
        try:
            db.session.commit()
            return {"message": "Profile updated successfully."}, 200
        except Exception as e:
            db.session.rollback()
            return {"message": f"Error updating profile: {str(e)}"}, 500

class ProfessionalDashboard(Resource):
    @jwt_required()
    @cache.cached(timeout=100)
    def get(self):
        username = get_jwt_identity()
        professional = User.query.filter_by(username=username).first()
        if not professional or not professional.professional_status:
            return {"message": "Access denied."}, 403
        if not professional.approval_status:
            return {"message": "Please wait for admin approval."}, 403

        pending_requests = HouseholdRequest.query.filter_by(professional_id=professional.id, request_status="Pending").all()
        accepted_requests = HouseholdRequest.query.filter_by(professional_id=professional.id, request_status="Accepted").all()
        closed_requests = HouseholdRequest.query.filter_by(professional_id=professional.id, request_status="Closed").all()

        if closed_requests:
            avg_rating = sum(request.customer_rating for request in closed_requests if request.customer_rating is not None) / len([request for request in closed_requests if request.customer_rating is not None])
        else:
            avg_rating = 0.0

        return jsonify({
            "professional": {
                "id": professional.id,
                "username": professional.username,
                "address": professional.user_address,
                "postal_code": professional.postal_code,
                "experience": professional.professional_experience_level,
                "service": professional.service.service_title if professional.service else None,
                "rating": avg_rating
            },
            "pending_requests": [            {
                "id": req.id,
                "service_title": req.service.service_title,
                "customer_name": req.customer.username,
                "details": req.details,
                "request_status": req.request_status,
                "created_at": req.created_at.isoformat() if req.created_at else None,
                "closed_at": req.closed_at.isoformat() if req.closed_at else None,
                "customer_rating": req.customer_rating,
                "customer_review": req.customer_review
            } for req in pending_requests],
            "accepted_requests": [            {
                "id": req.id,
                "service_title": req.service.service_title,
                "customer_name": req.customer.username,
                "details": req.details,
                "request_status": req.request_status,
                "created_at": req.created_at.isoformat() if req.created_at else None,
                "closed_at": req.closed_at.isoformat() if req.closed_at else None,
                "customer_rating": req.customer_rating,
                "customer_review": req.customer_review
            } for req in accepted_requests],
            "closed_requests": [            {
                "id": req.id,
                "service_title": req.service.service_title,
                "customer_name": req.customer.username,
                "details": req.details,
                "request_status": req.request_status,
                "created_at": req.created_at.isoformat() if req.created_at else None,
                "closed_at": req.closed_at.isoformat() if req.closed_at else None,
                "customer_rating": req.customer_rating,
                "customer_review": req.customer_review
            } for req in closed_requests]
        })


class AcceptOrRejectRequest(Resource):
    @jwt_required()
    @cache.cached(timeout=100)
    def get(self):
        username = get_jwt_identity()
        professional = User.query.filter_by(username=username).first()
        if not professional:
            return {"message": "Unauthorized access."}, 403

        requests = HouseholdRequest.query.filter_by(professional_id=professional.id).order_by(HouseholdRequest.created_at.desc()).all()
        return jsonify(requests=[req.serialize() for req in requests])

    @jwt_required()
    def post(self, request_id, action):
        username = get_jwt_identity()
        professional = User.query.filter_by(username=username).first()
        if not professional:
            return {"message": "Professional not found."}, 404
        
        request_obj = HouseholdRequest.query.get(request_id)
        if not request_obj or request_obj.professional_id != professional.id:
            return {"message": "Request not found or unauthorized."}, 403
        
        if action == "accept":
            request_obj.request_status = "Accepted"
        elif action == "reject":
            request_obj.request_status = "Rejected"
        else:
            return {"message": "Invalid action."}, 400
        
        try:
            db.session.commit()
            return {"message": f"Request {action}ed successfully."}, 200
        except Exception as e:
            db.session.rollback()
            return {"message": f"Error while processing request: {str(e)}"}, 500
