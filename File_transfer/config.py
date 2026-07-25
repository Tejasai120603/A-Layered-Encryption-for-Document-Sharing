
import os

class Config:
    SECRET_KEY = os.urandom(24)
    # Use an absolute path for the database
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(BASE_DIR, "instance", "app.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads', 'encrypted')
    MAIL_USERNAME = 'tejasairavikumar@gmail.com'  
    MAIL_PASSWORD = 'xvhn wukv iefp eilt'
    
