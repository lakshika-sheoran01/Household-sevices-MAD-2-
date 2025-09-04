from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(72), unique=True, nullable=False)
    user_password = db.Column(db.String(67), nullable=False)
    user_address = db.Column(db.String(100), nullable=True)
    postal_code = db.Column(db.Integer, nullable=True)
    admin_status = db.Column(db.Boolean, default=False)
    professional_status = db.Column(db.Boolean, default=False)
    customer_status = db.Column(db.Boolean, default=False)
    approval_status = db.Column(db.Boolean, default=False)
    rating_total = db.Column(db.Integer, default=0)
    average_rating = db.Column(db.Float, default=0.0)
    professional_document = db.Column(db.String(100), nullable=True)
    professional_experience_level = db.Column(db.String(10), nullable=True)
    service_id = db.Column(db.Integer, db.ForeignKey('householdServices.id', ondelete="SET NULL"), nullable=True)
    
    service = db.relationship('HouseholdServices', back_populates="professionals", foreign_keys=[service_id])
    professional_requests = db.relationship('HouseholdRequest', back_populates="professional", foreign_keys="HouseholdRequest.professional_id")
    customer_requests = db.relationship('HouseholdRequest', back_populates="customer", foreign_keys="HouseholdRequest.client_id")


class HouseholdServices(db.Model):
    __tablename__ = "householdServices"
    id = db.Column(db.Integer, primary_key=True)
    service_title = db.Column(db.String(30), unique=True, nullable=False)
    service_details = db.Column(db.String(40), nullable=True)
    duration_required = db.Column(db.String(30), nullable=True)
    starting_price = db.Column(db.Integer, nullable=True)
    
    professionals = db.relationship('User', back_populates="service", cascade="all, delete", foreign_keys="User.service_id")
    requests = db.relationship('HouseholdRequest', back_populates="service", cascade="all, delete")


class HouseholdRequest(db.Model):
    __tablename__ = "householdRequest"
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('householdServices.id'), nullable=True)
    client_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  
    request_type = db.Column(db.String(20), nullable=False)
    details = db.Column(db.Text, nullable=True)
    request_status = db.Column(db.String(56), nullable=True)
    created_at = db.Column(db.Date, nullable=False, default=datetime.now().date())
    closed_at = db.Column(db.Date, nullable=True)
    customer_rating = db.Column(db.Float, default=0.0)
    customer_review = db.Column(db.String(20), nullable=True)
    
    service = db.relationship('HouseholdServices', back_populates='requests')
    customer = db.relationship('User', back_populates='customer_requests', foreign_keys=[client_id])
    professional = db.relationship('User', back_populates='professional_requests', foreign_keys=[professional_id])  

