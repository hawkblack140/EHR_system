from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, Email


# ---------- Login Form ----------
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(message="Email is required."),
        Email(message="Invalid email address.")
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message="Password is required.")
    ])
    submit = SubmitField('Login')


# ---------- Register Form ----------
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(message="Username is required."),
        Length(min=3, max=150)
    ])
    email = StringField('Email', validators=[
        DataRequired(), Email()
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=6, message="Password must be at least 6 characters.")
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message="Passwords must match.")
    ])
    role = SelectField('Role', choices=[
        ('doctor', 'Doctor'),
        ('patient', 'Patient')
    ])
    submit = SubmitField('Register')


# ---------- Patient Record Form ----------
class PatientRecordForm(FlaskForm):
    patient_name = StringField('Patient Name', validators=[
        DataRequired(message="Patient name is required.")
    ])
    symptoms = TextAreaField('Symptoms', validators=[
        DataRequired(message="Symptoms are required.")
    ])
    diagnosis = TextAreaField('Diagnosis', validators=[
        DataRequired(message="Diagnosis is required.")
    ])
    prescription = TextAreaField('Prescription', validators=[
        DataRequired(message="Prescription is required.")
    ])
    submit = SubmitField('Save Record')
