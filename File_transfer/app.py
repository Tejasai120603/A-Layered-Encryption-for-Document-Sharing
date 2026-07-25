from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
from cryptography.fernet import Fernet
from Crypto.Cipher import AES, DES3
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from flask import abort
from flask import Response

import os
import hashlib
import smtplib
from email.mime.text import MIMEText
import base64
import uuid
import logging

# Configure logging

app = Flask(__name__)
app.config.from_object('config.Config')

# Ensure directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(os.path.dirname(os.path.join(app.config['BASE_DIR'], 'instance', 'app.db')), exist_ok=True)

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200), nullable=False)
    encrypted_path = db.Column(db.String(200), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    algorithm = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
    # Relationships
    sender = db.relationship('User', foreign_keys=[sender_id], backref='sent_files')
    receiver = db.relationship('User', foreign_keys=[receiver_id], backref='received_files')

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# Encryption Functions
def encrypt_file_fernet(file_data, key):
    fernet = Fernet(key)
    return fernet.encrypt(file_data), key

def decrypt_file_fernet(encrypted_data, key):
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_data)

def encrypt_file_aes(file_data, key):
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(file_data, AES.block_size))
    iv = cipher.iv
    return ct_bytes, key, iv

def decrypt_file_aes(encrypted_data, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    pt = unpad(cipher.decrypt(encrypted_data), AES.block_size)
    return pt

def encrypt_file_3des(file_data, key):
    cipher = DES3.new(key, DES3.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(file_data, DES3.block_size))
    iv = cipher.iv
    return ct_bytes, key, iv

def decrypt_file_3des(encrypted_data, key, iv):
    cipher = DES3.new(key, DES3.MODE_CBC, iv=iv)
    pt = unpad(cipher.decrypt(encrypted_data), DES3.block_size)
    return pt

# Email Function
def send_email(to_email, subject, body, max_retries=3):
    import time
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = app.config['MAIL_USERNAME']
    msg['To'] = to_email
    
    for attempt in range(max_retries):
        try:
            # Try port 587 with explicit TLS
            with smtplib.SMTP('smtp.gmail.com', 587, timeout=10) as server:
                server.starttls()         # Secure the connection
                server.login(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
                server.send_message(msg)
            return True # Success!
        except Exception as e:
            app.logger.warning(f"Email attempt {attempt + 1} failed for {to_email}: {str(e)}")
            if attempt < max_retries - 1:
                time.sleep(2)  # Wait 2 seconds before retrying
            else:
                app.logger.error(f"Failed to send email to {to_email} after {max_retries} attempts.")
                logging.exception("Detailed Email Connection Error:")
                return False

# Routes
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            flash('Email already registered. Please log in or use another email.')
            return redirect(url_for('signup'))

        existing_username = User.query.filter_by(username=username).first()
        if existing_username:
            flash('Username already taken. Please choose another username.')
            return redirect(url_for('signup'))

        hashed_password = generate_password_hash(password)
        user = User(username=username, email=email, password=hashed_password)
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash('Account already exists with this email or username.')
            return redirect(url_for('signup'))
        email_sent = send_email(email, 'Welcome to Secure File Transfer', 'Thank you for signing up!')
        if email_sent:
            flash('Signup successful! Please log in.')
        else:
            flash('Signup successful! However, the welcome email failed to send.')
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form['email']).first()
        if user and check_password_hash(user.password, request.form['password']):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Invalid credentials.')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if request.method == 'POST':
        search = request.form['search']
        users = User.query.filter(
            (User.username.ilike(f'%{search}%')) | (User.email.ilike(f'%{search}%'))
        ).all()
        return render_template('dashboard.html', users=users)
    return render_template('dashboard.html', users=[])

@app.route('/send_file/<int:receiver_id>', methods=['GET', 'POST'])
@login_required
def send_file(receiver_id):
    receiver = db.session.get(User, receiver_id) or abort(404)
    if request.method == 'POST':
        file = request.files['file']
        algorithm = request.form['algorithm']
        file_data = file.read()
        
        # Generate key based on algorithm
        if algorithm == 'fernet':
            key = Fernet.generate_key()
            encrypted_data, key = encrypt_file_fernet(file_data, key)
            iv = None
        elif algorithm == 'aes':
            key = get_random_bytes(16)
            encrypted_data, key, iv = encrypt_file_aes(file_data, key)
        elif algorithm == '3des':
            key = get_random_bytes(24)
            encrypted_data, key, iv = encrypt_file_3des(file_data, key)
        
        # Save encrypted file
        filename = f"{uuid.uuid4()}_{file.filename}"
        encrypted_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        with open(encrypted_path, 'wb') as f:
            f.write(encrypted_data)
        
        # Save file metadata
        file_record = File(
            filename=file.filename,
            encrypted_path=encrypted_path,
            sender_id=current_user.id,
            receiver_id=receiver_id,
            algorithm=algorithm
        )
        db.session.add(file_record)
        db.session.commit()
        
        # Send email with key
        key_b64 = base64.b64encode(key).decode()
        iv_b64 = base64.b64encode(iv).decode() if iv else None
        body = f"A file has been shared with you.\nEncryption Key: {key_b64}"
        if iv:
            body += f"\nIV: {iv_b64}"
        email_sent = send_email(receiver.email, 'New File Shared', body)
        
        if email_sent:
            flash('File sent successfully! An email with the key was sent to the receiver.')
        else:
            flash('File saved, but there was an error sending the decryption key email.')
        return redirect(url_for('dashboard'))
    
    return render_template('send_file.html', receiver=receiver)

@app.route('/received_files')
@login_required
def received_files():
    files = File.query.filter_by(receiver_id=current_user.id).all()
    return render_template('received_files.html', files=files)

@app.route('/shared_files')
@login_required
def shared_files():
    files = File.query.filter_by(sender_id=current_user.id).all()
    return render_template('shared_files.html', files=files)

@app.route('/decrypt_file/<int:file_id>', methods=['GET', 'POST'])
@login_required
def decrypt_file(file_id):
    file = db.session.get(File, file_id) or abort(404)
    if file.receiver_id != current_user.id:
        flash('Unauthorized access.')
        return redirect(url_for('received_files'))
    
    if request.method == 'POST':
        try:
            key_b64 = request.form['key']
            key = base64.b64decode(key_b64)
            iv = base64.b64decode(request.form['iv']) if 'iv' in request.form else None
            
            if not os.path.exists(file.encrypted_path):
                flash('Encrypted file not found on server.')
                return redirect(url_for('received_files'))
            
            with open(file.encrypted_path, 'rb') as f:
                encrypted_data = f.read()
            
            try:
                if file.algorithm == 'fernet':
                    decrypted_data = decrypt_file_fernet(encrypted_data, key)
                elif file.algorithm == 'aes':
                    if not iv:
                        flash('IV required for AES decryption.')
                        return redirect(url_for('decrypt_file', file_id=file_id))
                    decrypted_data = decrypt_file_aes(encrypted_data, key, iv)
                elif file.algorithm == '3des':
                    if not iv:
                        flash('IV required for 3DES decryption.')
                        return redirect(url_for('decrypt_file', file_id=file_id))
                    decrypted_data = decrypt_file_3des(encrypted_data, key, iv)
                
                # Create a response with the decrypted data
                response = Response(decrypted_data)
                response.headers['Content-Type'] = 'application/octet-stream'
                response.headers['Content-Disposition'] = f'attachment; filename="{file.filename}"'
                return response
            
            except Exception as e:
                flash(f'Decryption failed: {str(e)}')
                return redirect(url_for('decrypt_file', file_id=file_id))
        
        except base64.binascii.Error:
            flash('Invalid key or IV format.')
            return redirect(url_for('decrypt_file', file_id=file_id))
    
    return render_template('decrypt_file.html', file=file)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=3000)
