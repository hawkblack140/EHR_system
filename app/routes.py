from app.models import PatientRecord
from app.forms import PatientRecordForm

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app.models import User
from app.forms import LoginForm, RegisterForm

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return redirect(url_for('main.login'))

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password,
            role=form.role.data
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash(f'Welcome, {user.username}!', 'success')

            if user.role == 'doctor':
                return redirect(url_for('main.dashboard'))
            elif user.role == 'patient':
                return redirect(url_for('main.patient_dashboard'))
            else:
                flash("Invalid role assigned to user.", "danger")
                return redirect(url_for('main.login'))
        else:
            flash('Invalid email or password.', 'danger')

    return render_template('login.html', form=form)


@main.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'doctor':
        records = PatientRecord.query.filter_by(doctor_id=current_user.id).order_by(PatientRecord.created_at.desc()).all()
        return render_template('doctor_dashboard.html', records=records)
    else:
        return render_template('patient_dashboard.html')


@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))


@main.route('/add_record', methods=['GET', 'POST'])
@login_required
def add_record():
    if current_user.role != 'doctor':
        flash('Access denied.', 'danger')
        return redirect(url_for('main.dashboard'))

    form = PatientRecordForm()
    if form.validate_on_submit():
        record = PatientRecord(
            patient_name=form.patient_name.data,
            symptoms=form.symptoms.data,
            diagnosis=form.diagnosis.data,
            prescription=form.prescription.data,
            doctor_id=current_user.id
        )
        db.session.add(record)
        db.session.commit()
        flash('Patient record saved successfully.', 'success')
        return redirect(url_for('main.dashboard'))

    return render_template('add_record.html', form=form)


@main.route('/edit_record/<int:record_id>', methods=['GET', 'POST'])
@login_required
def edit_record(record_id):
    record = PatientRecord.query.get_or_404(record_id)
    
    if current_user.id != record.doctor_id:
        flash('Access denied. You can only edit your own records.', 'danger')
        return redirect(url_for('main.dashboard'))

    form = PatientRecordForm(obj=record)
    
    if form.validate_on_submit():
        record.patient_name = form.patient_name.data
        record.symptoms = form.symptoms.data
        record.diagnosis = form.diagnosis.data
        record.prescription = form.prescription.data
        db.session.commit()
        flash('Patient record updated successfully.', 'success')
        return redirect(url_for('main.dashboard'))
    
    return render_template('edit_record.html', form=form, record=record)


@main.route('/delete_record/<int:record_id>', methods=['POST'])
@login_required
def delete_record(record_id):
    record = PatientRecord.query.get_or_404(record_id)
    
    if current_user.id != record.doctor_id:
        flash('Access denied. You can only delete your own records.', 'danger')
        return redirect(url_for('main.dashboard'))

    db.session.delete(record)
    db.session.commit()
    flash('Patient record deleted successfully.', 'success')
    return redirect(url_for('main.dashboard'))


@main.route('/patient_dashboard')
@login_required
def patient_dashboard():
    if current_user.role == 'patient':
        records = PatientRecord.query.filter_by(patient_name=current_user.username).order_by(PatientRecord.created_at.desc()).all()
        return render_template('patient_dashboard.html', records=records)
    else:
        return redirect(url_for('main.dashboard'))
