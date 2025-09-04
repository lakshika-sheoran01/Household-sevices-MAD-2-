from flask import Flask, request
from flask_jwt_extended import JWTManager
from applications.models import db, User
from applications.admin import AdminAuth, AdminDashboard, AdminStatistics, ServiceManagement, ProfessionalManagement, cache, ExportData
from applications.professional import ProfessionalProfileManagement, ProfessionalDashboard, AcceptOrRejectRequest
from applications.customer import CustomerProfileManagement, CustomerDashboard, CustomerServiceRequestManagment
from applications.auth import UserLogin
from applications.worker import celery
from applications.task import *
from datetime import timedelta
from flask_cors import CORS      
from flask_restful import Api
from werkzeug.security import generate_password_hash
import os

curr_dir = os.path.dirname(os.path.abspath(__file__))

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configure database URI and other settings
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///household_services_database.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  
app.config['SECRET_KEY'] = '@sheoran'  
app.secret_key = 'household'  
app.config['CACHE_TYPE'] = 'redis'
app.config['CACHE_REDIS_HOST'] = 'localhost'
app.config['CACHE_REDIS_PORT'] = 6379
app.config['CACHE_REDIS_DB'] = 0
app.config['CACHE_REDIS_URL'] = "redis://localhost:6379"
app.config['CACHE_DEFAULT_TIMEOUT'] = 300

# Configure file upload settings
app.config['UPLOAD_EXTENSIONS'] = ['.pdf', '.jpg', '.png', '.jpeg', '.gif']
app.config['UPLOAD_PATH'] = os.path.join(curr_dir, 'static')  
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'png', 'jpg', 'jpeg', 'gif'}  

# JWT Configuration
app.config['JWT_SECRET_KEY'] = 'your-secret-key'  
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=24)  


db.init_app(app)
cache.init_app(app)  
api = Api(app)
jwt = JWTManager(app)
app.app_context().push()

celery.conf.update(
    broker_url='redis://localhost:6379/0',
    result_backend='redis://localhost:6379/1',
    timezone = 'Asia/Kolkata'
)

@app.before_request
def clear_cache_when_change_db():
    if request.method != "GET":
        cache.clear() 

def create_admin():
    with app.app_context():
        admin_user = User.query.filter_by(admin_status=True).first()
        if not admin_user:
            admin_user = User(
                username="admin",
                user_password=generate_password_hash('pass'),
                admin_status=True 
            )
            db.session.add(admin_user)
            db.session.commit()
            print("Admin user created successfully")

with app.app_context():
    db.create_all()
    create_admin()


# api.add_resource(HelloWorld, '/')
api.add_resource(AdminAuth, '/admin/authenticate')  
api.add_resource(AdminDashboard, '/admin/dashboard')
api.add_resource(ExportData, '/admin/export')
api.add_resource(AdminStatistics, '/admin/stats')
api.add_resource(ProfessionalManagement, '/admin/approve_professional/<int:professional_id>', '/admin/reject_professional/<int:professional_id>', '/admin/block_professional/<int:professional_id>')
api.add_resource(ServiceManagement, '/admin/service', '/admin/service/<int:service_id>')
api.add_resource(UserLogin, '/user/login')
api.add_resource(CustomerDashboard, '/customer/dashboard')
api.add_resource(CustomerProfileManagement, '/customer/register', '/customer/profile')
api.add_resource(ProfessionalProfileManagement, '/professional/register', '/professional/profile')
api.add_resource(CustomerServiceRequestManagment, '/customer/service/<int:service_id>', '/customer/request/<int:request_id>/close', '/customer/request/<int:request_id>/rate')
api.add_resource(ProfessionalDashboard, '/professional/dashboard')
api.add_resource(AcceptOrRejectRequest, '/professional/request/<int:request_id>/<string:action>')

if __name__ == '__main__':
    app.run(debug=True)