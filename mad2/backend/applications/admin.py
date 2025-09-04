from flask import request, jsonify
from flask_restful import Resource
from datetime import datetime
from werkzeug.security import check_password_hash
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from .models import User, HouseholdServices, HouseholdRequest, db
from .task import data_export
import matplotlib.pyplot as plt
import io
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.ticker import MaxNLocator
from sqlalchemy import func
from flask_caching import Cache


cache = Cache()
class AdminAuth(Resource):
    def post(self):
        data = request.json
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return {'message': 'Username and password are required'}, 400

        admin = User.query.filter_by(admin_status=True, username=username).first()
        if admin and check_password_hash(admin.user_password, password):
            access_token = create_access_token(identity=admin.id)
            return {
                'message': 'Logged in successfully',
                'access_token': access_token,
                'is_admin': True,
                'username': admin.username
            }, 200

        return {'message': 'Invalid credentials. Please try again.'}, 401

class AdminDashboard(Resource):
    @jwt_required()
    @cache.cached(timeout=100)
    def get(self):
        admin_id = get_jwt_identity()
        admin = User.query.get(admin_id)

        if not admin or not admin.admin_status:
            return {'message': 'Unauthorized'}, 403

        services = HouseholdServices.query.all()
        requests = HouseholdRequest.query.all()
        professionals = User.query.filter_by(professional_status=True).all()
        
        return {
            'services': [{'id': s.id, 'service_title': s.service_title, 'service_details': s.service_details, 'duration_required': s.duration_required, 'starting_price': s.starting_price} for s in services],
            'requests': [{'customer_name': r.customer.username, 'service_title': r.service.service_title, 'id': r.id, 
                          'professional_name': r.professional.username if r.professional else None, 
                          'date_requested': r.created_at.isoformat(), 'date_closed': r.closed_at.isoformat() if r.closed_at else None, 
                          'status': r.request_status} for r in requests],
            'professionals': [{ 'id': p.id,
            'username': p.username,
            'user_address': p.user_address,
            'postal_code': p.postal_code,
            'professional_status': p.professional_status,
            'approval_status': p.approval_status,
            'average_rating': p.average_rating,
            'professional_experience_level': p.professional_experience_level,
            'service_title': p.service.service_title } for p in professionals],
            'admin_name': admin.username
        }, 200


class ServiceManagement(Resource):
    @jwt_required()
    def post(self):
        admin_id = get_jwt_identity()
        admin = User.query.get(admin_id)

        if not admin or not admin.admin_status:
            return {'message': 'Unauthorized'}, 403

        data = request.json
        service_title = data.get('service_title')
        service_details = data.get('service_details')
        starting_price = data.get('starting_price')
        duration_required = data.get('duration_required')

        if not all([service_title, service_details, starting_price, duration_required]):
            return {'message': 'All fields are required.'}, 400

        if HouseholdServices.query.filter_by(service_title=service_title).first():
            return {'message': f"A service with the title '{service_title}' already exists."}, 400

        
        new_service = HouseholdServices(
            service_title=service_title,
            service_details=service_details,
            starting_price=int(starting_price),
            duration_required=duration_required
        )
        db.session.add(new_service)
        db.session.commit()
        return {'message': 'Service created successfully.'}, 201
        
    @jwt_required()
    def put(self, service_id):
        print("here")
        current_user_id = get_jwt_identity()
        admin = User.query.get(current_user_id)
        if not admin or not admin.admin_status:
            return {'message': 'Please log in as an admin first.'}, 403
        service = HouseholdServices.query.get_or_404(service_id)
        data = request.json
        service_title = data.get('service_title')
        service_details = data.get('service_details')
        starting_price = data.get('starting_price')
        duration_required = data.get('duration_required')
        if not service_title or not service_details or not starting_price or not duration_required:
            return {'message': 'All fields are required.'}, 400

        service.service_title = service_title
        service.service_details = service_details
        service.starting_price = starting_price
        service.duration_required = duration_required
        db.session.commit()
        return {'message': 'Service updated successfully.'}, 200
    
    @jwt_required()
    def delete(self, service_id):
        admin_id = get_jwt_identity()
        admin = User.query.get(admin_id)

        if not admin or not admin.admin_status:
            return {'message': 'Unauthorized'}, 403

        service = HouseholdServices.query.get_or_404(service_id)

        # Disable approval for professionals linked to this service
        professionals = User.query.filter_by(service_id=service_id, professional_status=True).all()
        for prof in professionals:
            prof.approval_status = False

        db.session.delete(service)
        db.session.commit()
        return {'message': f'Service {service_id} deleted successfully'}, 200

class ProfessionalManagement(Resource):
    @jwt_required()
    @cache.cached(timeout=100)
    def get(self, professional_id):
        current_user_id = get_jwt_identity()
        admin = User.query.get(current_user_id)
        if not admin or not admin.admin_status:
            return {'message': 'Please log in as an admin first.'}, 403
        professional = User.query.get_or_404(professional_id)
        professional_data = {
            'id': professional.id,
            'username': professional.username,
            'user_address': professional.user_address,
            'postal_code': professional.postal_code,
            'professional_status': professional.professional_status,
            'approval_status': professional.approval_status,
            'average_rating': professional.average_rating,
            'professional_experience_level': professional.professional_experience_level,
            'service_id': professional.service_id
        }
        return jsonify(professional_data)
    
    @jwt_required()
    def put(self, professional_id):
        admin_id = get_jwt_identity()
        admin = User.query.get(admin_id)

        if not admin or not admin.admin_status:
            return {'message': 'Unauthorized'}, 403

        professional = User.query.get_or_404(professional_id)
        professional.approval_status = True
        db.session.commit()
        return {'message': 'Professional approved successfully.'}, 200

    @jwt_required()
    def patch(self, professional_id):
        admin_id = get_jwt_identity()
        admin = User.query.get(admin_id)

        if not admin or not admin.admin_status:
            return {'message': 'Unauthorized'}, 403

        professional = User.query.get_or_404(professional_id)
        professional.approval_status = False
        db.session.commit()
        return {'message': 'Professional blocked successfully.'}, 200
    
    @jwt_required()
    def delete(self, professional_id):
        admin_id = get_jwt_identity()
        admin = User.query.get(admin_id)

        if not admin or not admin.admin_status:
            return {'message': 'Unauthorized'}, 403

        professional = User.query.get_or_404(professional_id)
        db.session.delete(professional)
        db.session.commit()
        return {'message': 'Professional rejected successfully.'}, 200


class AdminStatistics(Resource):
    @jwt_required()
    @cache.cached(timeout=100)
    def get(self):
        admin_id = get_jwt_identity()
        admin = User.query.get(admin_id)

        if not admin or not admin.admin_status:
            return {'message': 'Unauthorized'}, 403

        total_users = User.query.filter_by(admin_status=False).count()
        total_requests = HouseholdRequest.query.count()
        approved_users = User.query.filter_by(approval_status=True, admin_status=False).count()
        flagged_users = User.query.filter_by(approval_status=False, admin_status=False).count()

        avg_rating = db.session.query(func.avg(User.average_rating)).filter(
            User.professional_status == True, User.admin_status == False
        ).scalar() or 0

        total_services_provided = HouseholdRequest.query.filter_by(request_status="Closed").count()

        # Pie Chart: Approved vs Flagged Users
        fig1, ax1 = plt.subplots()
        ax1.pie([approved_users, flagged_users], labels=['Approved', 'Flagged'],
                autopct='%1.1f%%', startangle=90, colors=['#28a745', '#dc3545'])
        ax1.axis('equal')
        user_status_chart = io.BytesIO()
        FigureCanvas(fig1).print_png(user_status_chart)
        user_status_chart_base64 = base64.b64encode(user_status_chart.getvalue()).decode('utf-8')

        # Bar Chart: Service Requests
        service_data = {s.service_title: HouseholdRequest.query.filter_by(service_id=s.id).count()
                        for s in HouseholdServices.query.all()}
        fig2, ax2 = plt.subplots()
        ax2.bar(service_data.keys(), service_data.values(), color='blue')
        ax2.yaxis.set_major_locator(MaxNLocator(integer=True))
        bar_chart = io.BytesIO()
        FigureCanvas(fig2).print_png(bar_chart)
        bar_chart_base64 = base64.b64encode(bar_chart.getvalue()).decode('utf-8')

        return {
            'total_users': total_users,
            'total_requests': total_requests,
            'approved_users': approved_users,
            'flagged_users': flagged_users,
            'avg_rating': avg_rating,
            'total_services_provided': total_services_provided,
            'user_status_chart': user_status_chart_base64,
            'bar_chart': bar_chart_base64
        }, 200

class ExportData(Resource):
    @jwt_required()
    def get(self):
        admin_id = get_jwt_identity()
        admin = User.query.get(admin_id)

        if not admin or not admin.admin_status:
            return {'message': 'Unauthorized'}, 403

        completed_requests = HouseholdRequest.query.filter_by(request_status='Closed').all()

        if not completed_requests:
            return {'message': 'No completed requests found'}, 404

        request_details = []
        for request in completed_requests:
            request_details.append({
                'Service Title': request.service.service_title if request.service else 'Unknown',
                'Request Type': request.request_type,
                'Created At': request.created_at,
                'Closed At': request.closed_at or 'Pending',
                'Review': request.customer_review or 'No Review'
            })

        data_export(request_details)
        return {'message': 'Your data export task has been initiated, please check your inbox.'}, 200
