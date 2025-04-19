from datetime import datetime
from flask_login import UserMixin
from app import db, login_manager

# User Loader Function
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# User Model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)  # longer for hashed pw
    role = db.Column(db.String(50), nullable=False)  # doctor or patient

    # Optional: Helpful representation for debugging
    def __repr__(self):
        return f'<User {self.username} ({self.role})>'

# Patient Record Model
class PatientRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_name = db.Column(db.String(150), nullable=False)
    symptoms = db.Column(db.Text, nullable=False)
    diagnosis = db.Column(db.Text, nullable=False)
    prescription = db.Column(db.Text, nullable=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    doctor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Relationship to User
    doctor = db.relationship('User', backref='records')

    def __repr__(self):
        return f'<Record {self.patient_name} - DoctorID: {self.doctor_id}>'
