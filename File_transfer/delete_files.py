
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, filename='clear_files.log', format='%(asctime)s %(levelname)s: %(message)s')

# Initialize Flask app to load configuration
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

# Define the File model (same as in app.py)
class File(db.Model):
    __tablename__ = 'file'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200), nullable=False)
    encrypted_path = db.Column(db.String(200), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    algorithm = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

def clear_all_files():
    """Delete all file records from the database and their corresponding encrypted files."""
    with app.app_context():
        try:
            # Ensure database tables are created
            db.create_all()

            # Query all file records
            files = File.query.all()
            if not files:
                print("No files found in the database.")
                logging.info("No files found in the database.")
                return

            print(f"Found {len(files)} files to delete.")
            logging.info(f"Found {len(files)} files to delete.")

            # Iterate through files to delete from filesystem and database
            for file in files:
                try:
                    # Check if the encrypted file exists and delete it
                    if os.path.exists(file.encrypted_path):
                        os.remove(file.encrypted_path)
                        print(f"Deleted file from filesystem: {file.encrypted_path}")
                        logging.info(f"Deleted file from filesystem: {file.encrypted_path}")
                    else:
                        print(f"File not found on filesystem: {file.encrypted_path}")
                        logging.warning(f"File not found on filesystem: {file.encrypted_path}")
                    
                    # Delete the file record from the database
                    db.session.delete(file)
                    print(f"Deleted file record: {file.filename} (ID: {file.id})")
                    logging.info(f"Deleted file record: {file.filename} (ID: {file.id})")
                
                except OSError as e:
                    print(f"Error deleting file {file.encrypted_path}: {e}")
                    logging.error(f"Error deleting file {file.encrypted_path}: {e}")
                    continue
                except Exception as e:
                    print(f"Error deleting file record {file.filename}: {e}")
                    logging.error(f"Error deleting file record {file.filename}: {e}")
                    continue

            # Commit the database changes
            db.session.commit()
            print("All file records and their encrypted files have been deleted successfully.")
            logging.info("All file records and their encrypted files have been deleted successfully.")

        except Exception as e:
            db.session.rollback()
            print(f"Error during file deletion process: {e}")
            logging.error(f"Error during file deletion process: {e}")
        finally:
            db.session.close()
            print("Database session closed.")
            logging.info("Database session closed.")

def main():
    """Main function to execute the file clearing process."""
    print("Clearing all files from Secure File Transfer database and filesystem...")
    print(f"Database path: {app.config['SQLALCHEMY_DATABASE_URI']}")
    print(f"Upload folder: {app.config['UPLOAD_FOLDER']}")
    logging.info(f"Starting file clearing process. Database: {app.config['SQLALCHEMY_DATABASE_URI']}, Upload folder: {app.config['UPLOAD_FOLDER']}")
    
    # Confirm with user before proceeding
    confirm = input("Are you sure you want to delete ALL file records and their encrypted files? (yes/no): ")
    if confirm.lower() != 'yes':
        print("Operation cancelled.")
        logging.info("Operation cancelled by user.")
        return
    
    clear_all_files()

if __name__ == "__main__":
    main()
