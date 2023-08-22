import sqlite3, time, os
from colorama import Fore, Style
from src.util.logger import Logger
from src.helper.config import Config


class AccountsDB:
    DB_PATH = 'src/database/container/accounts.sqlite'

    # Constants for time calculation
    SECONDS_IN_A_WEEK = 604800
    SECONDS_IN_A_DAY = 86400
    SECONDS_IN_AN_HOUR = 3600
    SECONDS_IN_A_MINUTE = 60

    def __init__(self):
        """Initialize database connection and table."""
        self.config = Config()
        self.logger = Logger()
        self.connection = self._connect_to_db()
        self.create_table()

    def _connect_to_db(self):
        """Connect to the database and return the connection."""
        try:
            return sqlite3.connect(self.DB_PATH)
        except sqlite3.Error as e:
            self.logger.log("ERROR", f"Error connecting to database: {e}")
            return None

    def _execute_query(self, query, parameters=()):
        """Execute a given SQL query with parameters and return the cursor."""
        try:
            with self.connection as conn:
                cursor = conn.cursor()
                cursor.execute(query, parameters)
                return cursor
        except sqlite3.Error as e:
            self.logger.log("ERROR", f"Error executing query: {e}")
            return None

    def create_table(self):
        """Create the accounts table if it doesn't exist."""
        create_table_sql = '''
            CREATE TABLE IF NOT EXISTS accounts_db (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                ssfn TEXT NOT NULL,
                is_banned INTEGER DEFAULT 0,
                banned_timestamp INTEGER DEFAULT 0
            );
        '''
        self._execute_query(create_table_sql)

    def account_exists(self, column, value):
        """Check if an account exists based on a column and value."""
        cursor = self._execute_query(f"SELECT * FROM accounts_db WHERE {column}=?", (value,))
        if cursor:
            return cursor.fetchone() is not None
        return False

    def add_user(self, username, password, ssfn):
        """Add a new user to the accounts table."""
        cursor = self._execute_query(
            "INSERT INTO accounts_db(username, password, ssfn) VALUES(?, ?, ?)",
            (username, password, ssfn)
        )
        return cursor is not None

    def remove_user(self, column, value):
        """Remove a user from the accounts table based on a column and value."""
        cursor = self._execute_query(f"DELETE FROM accounts_db WHERE {column}=?", (value,))
        return cursor is not None

    def get_all_users(self):
        """Fetch and format all users from the accounts table."""
        cursor = self._execute_query("SELECT * FROM accounts_db")
        if cursor:
            rows = cursor.fetchall()
            if not rows:
                return "No one in the database"

            headers = ['ID', 'Username', 'Password', 'SSFN', 'Is Banned', 'Banned Duration']
            formatted_data = [Fore.WHITE + ' • '.join(headers) + Style.RESET_ALL]
            formatted_data.append("\n")

            for row in rows:
                # Check if the user is banned and get the duration
                banned_status, banned_duration = self.is_user_banned("id", row[0])

                # Color logic for 'Is Banned' and 'Banned Duration'
                color_banned = Fore.LIGHTRED_EX if banned_status else Fore.LIGHTGREEN_EX
                formatted_banned = color_banned + str(banned_status) + Style.RESET_ALL

                if banned_duration:
                    days, hours, minutes, seconds = map(int, banned_duration.split(' ')[::2])
                    durations = [
                        (days, "day(s)"),
                        (hours, "hour(s)"),
                        (minutes, "minute(s)"),
                        (seconds, "second(s)")
                    ]
                    # Only add non-zero durations
                    banned_duration = ' '.join(f"{value} {unit}" for value, unit in durations if value)
                else:
                    banned_duration = 'None'

                formatted_duration = color_banned + banned_duration + Style.RESET_ALL

                # Constructing the formatted line
                line = f"{Fore.WHITE}{row[0]} • {row[1]} • HIDDEN • {row[3]} • {formatted_banned} • {formatted_duration}{Style.RESET_ALL}"
                formatted_data.append(line)

            return '\n'.join(formatted_data)
        return "Error fetching data"

    def get_account(self, column, value):
        """Fetch a single account based on a column and value."""
        cursor = self._execute_query(f"SELECT * FROM accounts_db WHERE {column}=?", (value,))
        if cursor:
            return cursor.fetchone()
        return None

    def add_ban(self, column, identifier, weeks=0, days=0, hours=0, minutes=0):
        """Ban a user for a specific duration."""
        ban_duration = (weeks * self.SECONDS_IN_A_WEEK + days * self.SECONDS_IN_A_DAY +
                        hours * self.SECONDS_IN_AN_HOUR + minutes * self.SECONDS_IN_A_MINUTE)
        banned_timestamp = time.time() + ban_duration

        with self.connection as conn:
            cursor = conn.cursor()
            cursor.execute(f"UPDATE accounts_db SET is_banned = 1, banned_timestamp = ? WHERE {column}=?", 
                        (banned_timestamp, identifier))
            return True

    def remove_ban(self, column, identifier):
        """Remove a user's ban."""
        with self.connection as conn:
            cursor = conn.cursor()
            cursor.execute(f"UPDATE accounts_db SET is_banned = 0, banned_timestamp = 0 WHERE {column}=?", 
                        (identifier,))
            return True

    def is_user_banned(self, column, identifier):
        """Check if a user is banned and return the remaining ban duration."""
        cursor = self._execute_query(f"SELECT is_banned, banned_timestamp FROM accounts_db WHERE {column}=?", 
                                    (identifier,))
        if cursor:
            row = cursor.fetchone()
            if row:
                is_banned, banned_timestamp = row
                if is_banned:
                    remaining_time = self._get_remaining_ban_time(banned_timestamp)
                    if remaining_time:
                        return True, remaining_time
                    else:
                        self.remove_ban(column, identifier)
                        return False, None
                else:
                    return False, None
            else:
                return False, None
        else:
            return False, None

    def _get_remaining_ban_time(self, banned_timestamp):
        """Calculate the remaining ban time."""
        current_time = time.time()
        if banned_timestamp > current_time:
            remaining_time = banned_timestamp - current_time
            days = int(remaining_time // self.SECONDS_IN_A_DAY)
            hours = int((remaining_time % self.SECONDS_IN_A_DAY) // self.SECONDS_IN_AN_HOUR)
            minutes = int((remaining_time % self.SECONDS_IN_AN_HOUR) // self.SECONDS_IN_A_MINUTE)
            seconds = int(remaining_time % self.SECONDS_IN_A_MINUTE)

            return f"{days} days {hours} hours {minutes} minutes {seconds} seconds"
        return None

    def get_identifier_column(self, identifier):
        """Get the identifier column based on the identifier."""
        if identifier.isdigit():
            return "id"
        elif identifier.isalnum():
            return "username"
        else:
            return None

    def close_connection(self):
        """Close the database connection."""
        if self.connection:
            self.connection.close()

    def import_from_old_db(self):
        """Import the accounts from the old database."""
        old_db_path = input(f" -{Fore.LIGHTCYAN_EX}>{Fore.WHITE} Old database path: {Style.RESET_ALL}")
        if os.path.exists(old_db_path):
            try:
                old_connection = sqlite3.connect(old_db_path)
                old_cursor = old_connection.cursor()
                old_cursor.execute("SELECT * FROM accounts_db")
                rows = old_cursor.fetchall()
                if rows:
                    for row in rows:
                        self.add_user(row[1], row[2], row[3])
                    self.logger.log("INFO", "Successfully imported accounts from the old database!")
                    time.sleep(1)
                    return True
                else:
                    self.logger.log("ERROR", "Old database is empty!")
                    time.sleep(1)
                    return False
            except sqlite3.Error as e:
                self.logger.log("ERROR", f"Error importing accounts from the old database: {e}")
                time.sleep(1)
                return False
            finally:
                old_connection.close()
        else:
            self.logger.log("ERROR", "Old database path not found!")
            time.sleep(1)
            return False

    def __del__(self):
        """Destructor to ensure the connection is closed."""
        self.close_connection()