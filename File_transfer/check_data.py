import sqlite3
import os
from datetime import datetime

# Define the path to the SQLite database
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, 'instance', 'app.db')

def connect_db():
    """Connect to the SQLite database and return the connection and cursor."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        return conn, cursor
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None, None

def fetch_users(cursor):
    """Fetch and display all users from the User table."""
    try:
        cursor.execute("SELECT id, username, email FROM user")
        users = cursor.fetchall()
        if not users:
            print("No users found in the database.")
            return
        print("\n=== Users ===")
        print(f"{'ID':<5} {'Username':<20} {'Email':<30}")
        print("-" * 60)
        for user in users:
            print(f"{user[0]:<5} {user[1]:<20} {user[2]:<30}")
    except sqlite3.Error as e:
        print(f"Error fetching users: {e}")

def fetch_files(cursor):
    """Fetch and display all files from the File table, including sender and receiver usernames."""
    try:
        # Join File with User to get sender and receiver usernames
        cursor.execute("""
            SELECT f.id, f.filename, f.encrypted_path, f.algorithm, f.timestamp,
                   s.username AS sender_username, r.username AS receiver_username
            FROM file f
            LEFT JOIN user s ON f.sender_id = s.id
            LEFT JOIN user r ON f.receiver_id = r.id
        """)
        files = cursor.fetchall()
        if not files:
            print("No files found in the database.")
            return
        print("\n=== Files ===")
        print(f"{'ID':<5} {'Filename':<30} {'Sender':<20} {'Receiver':<20} {'Algorithm':<10} {'Timestamp':<20}")
        print("-" * 110)
        for file in files:
            print(f"{file[0]:<5} {file[1]:<30} {file[5] or 'Unknown':<20} {file[6] or 'Unknown':<20} {file[3]:<10} {file[4]:<20}")
    except sqlite3.Error as e:
        print(f"Error fetching files: {e}")

def main():
    """Main function to check data in the database."""
    print("Checking data in Secure File Transfer database...")
    print(f"Database path: {DB_PATH}")

    # Connect to the database
    conn, cursor = connect_db()
    if not conn or not cursor:
        print("Failed to connect to the database. Exiting.")
        return

    try:
        # Fetch and display users
        fetch_users(cursor)
        # Fetch and display files
        fetch_files(cursor)
    finally:
        # Close the connection
        conn.close()
        print("\nDatabase connection closed.")

if __name__ == "__main__":
    main()
