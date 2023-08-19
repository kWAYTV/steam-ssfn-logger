import sqlite3
from src.util.logger import Logger
from src.helper.config import Config

class AccountsDB:
    def __init__(self):
        self.config = Config()
        self.logger = Logger()
        self.connection = self._connect_to_db()
        self.create_table()

    # Function to connect to the database
    def _connect_to_db(self):
        try:
            return sqlite3.connect('src/database/container/accounts.sqlite')
        except sqlite3.Error as e:
            self.logger.log("ERROR", f"Error connecting to database: {e}")
            return None

    # Function to close the connection to the database
    def __del__(self):
        if self.connection:
            self.connection.close()

    # Function to create the table if it does not exist
    def create_table(self):
        if not self.connection:
            return

        try:
            with self.connection:
                self.connection.execute('''
                    CREATE TABLE IF NOT EXISTS accounts_db (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT,
                        password TEXT,
                        ssfn TEXT
                    );
                ''')
        except sqlite3.Error as e:
            self.logger.log("ERROR", f"Error creating table: {e}")

    # Function to check if account exists in the database by username
    def account_exists_by_username(self, username):
        if not self.connection:
            return False

        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM accounts_db WHERE username=?", (username,))
            row = cursor.fetchone()
            return row is not None
        except sqlite3.Error as e:
            self.logger.log("ERROR", f"Error fetching data: {e}")
            return False

    # Function to check if account exists in the database by ID
    def account_exists_by_id(self, user_id):
        if not self.connection:
            return False

        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM accounts_db WHERE id=?", (user_id,))
            row = cursor.fetchone()
            return row is not None
        except sqlite3.Error as e:
            self.logger.log("ERROR", f"Error fetching data: {e}")
            return False

    # Function to add user to the database
    def add_user(self, username, password, ssfn):
        if not self.connection:
            return False

        try:
            with self.connection:
                self.connection.execute("INSERT INTO accounts_db(username, password, ssfn) VALUES(?, ?, ?)", (username, password, ssfn))
                self.connection.commit()
            return True  # User added successfully
        except sqlite3.Error as e:
            self.connection.rollback() # Rollback changes
            self.logger.log("ERROR", f"Error adding user: {e}")
            return False  # Error occurred during insertion

    # Function to remove user from the database by ID
    def remove_user_by_id(self, user_id):
        if not self.connection:
            return False

        try:
            with self.connection:
                self.connection.execute("DELETE FROM accounts_db WHERE id=?", (user_id,))
                self.connection.commit()
            return True  # User removed successfully
        except sqlite3.Error as e:
            self.connection.rollback()  # Rollback changes
            self.logger.log("ERROR", f"Error removing user by ID: {e}")
            return False  # Error occurred during deletion

    # Function to remove user from the database by username
    def remove_user_by_username(self, username):
        if not self.connection:
            return False

        try:
            with self.connection:
                self.connection.execute("DELETE FROM accounts_db WHERE username=?", (username,))
                self.connection.commit()
            return True  # User removed successfully
        except sqlite3.Error as e:
            self.connection.rollback()  # Rollback changes
            self.logger.log("ERROR", f"Error removing user by username: {e}")
            return False  # Error occurred during deletion

    # Function to get all users from the database
    def get_all_users(self):
        if not self.connection:
            return False

        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM accounts_db")
            rows = cursor.fetchall()

            # Check if rows is empty and return the desired message
            if not rows:
                return "No one in the database"
                
            # Prepare data for printing
            headers = ['ID', 'Username', 'Password', 'SSFN']
            formatted_data = [' • '.join(headers)]
            formatted_data.append("\n")
            for row in rows:
                formatted_data.append(' • '.join(map(str, row)))

            return '\n'.join(formatted_data)

        except sqlite3.Error as e:
            self.logger.log("ERROR", f"Error fetching data: {e}")
            return []

    # Function to get account info by id 
    def get_account_by_id(self, user_id):
        if not self.connection:
            return False

        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM accounts_db WHERE id=?", (user_id,))
            row = cursor.fetchone()
            return row
        except sqlite3.Error as e:
            self.logger.log("ERROR", f"Error fetching data: {e}")
            return False

    # Function to get account info by username
    def get_account_by_username(self, username):
        if not self.connection:
            return False

        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM accounts_db WHERE username=?", (username,))
            row = cursor.fetchone()
            return row
        except sqlite3.Error as e:
            self.logger.log("ERROR", f"Error fetching data: {e}")
            return False