import sqlite3, time
from colorama import Fore, Style
from src.util.logger import Logger
from src.helper.config import Config

class AccountsDB:
    DB_PATH = 'src/database/container/accounts.sqlite'
    
    def __init__(self):
        self.config = Config()
        self.logger = Logger()
        self.connection = self._connect_to_db()
        self.create_table()

    def _connect_to_db(self):
        try:
            return sqlite3.connect(self.DB_PATH)
        except sqlite3.Error as e:
            self.logger.log("ERROR", f"Error connecting to database: {e}")
            return None

    def _execute_query(self, query, parameters=()):
        try:
            with self.connection as conn:
                cursor = conn.cursor()
                cursor.execute(query, parameters)
                return cursor
        except sqlite3.Error as e:
            self.logger.log("ERROR", f"Error executing query: {e}")
            return None

    def create_table(self):
        create_table_sql = '''
            CREATE TABLE IF NOT EXISTS accounts_db (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                password TEXT,
                ssfn TEXT,
                is_banned INTEGER DEFAULT 0,
                banned_timestamp INTEGER DEFAULT 0
            );
        '''
        self._execute_query(create_table_sql)

    def account_exists(self, column, value):
        cursor = self._execute_query(f"SELECT * FROM accounts_db WHERE {column}=?", (value,))
        if cursor:
            return cursor.fetchone() is not None
        return False

    def add_user(self, username, password, ssfn):
        cursor = self._execute_query(
            "INSERT INTO accounts_db(username, password, ssfn) VALUES(?, ?, ?)", 
            (username, password, ssfn)
        )
        return cursor is not None

    def remove_user(self, column, value):
        cursor = self._execute_query(f"DELETE FROM accounts_db WHERE {column}=?", (value,))
        return cursor is not None

    from colorama import Fore, Style

    def get_all_users(self):
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
                line = f"{Fore.WHITE}{row[0]} • {row[1]} • {row[2]} • {row[3]} • {formatted_banned} • {formatted_duration}{Style.RESET_ALL}"
                formatted_data.append(line)

            return '\n'.join(formatted_data)
        return "Error fetching data"

    def get_account(self, column, value):
        cursor = self._execute_query(f"SELECT * FROM accounts_db WHERE {column}=?", (value,))
        if cursor:
            return cursor.fetchone()
        return None

    def add_ban(self, column, identifier, weeks=0, days=0, hours=0, minutes=0):
        if not self.connection:
            return False

        # Convert the ban duration to seconds
        ban_duration = weeks * 604800 + days * 86400 + hours * 3600 + minutes * 60
        banned_timestamp = time.time() + ban_duration

        try:
            cursor = self.connection.cursor()
            cursor.execute(f"UPDATE accounts_db SET is_banned = 1, banned_timestamp = ? WHERE {column}=?", (banned_timestamp, identifier))

            self.connection.commit()

            return True  # Ban added successfully

        except sqlite3.Error as e:
            self.logger.log("ERROR", f"Error imposing ban: {e}")
            return False

    def remove_ban(self, column, identifier):
        if not self.connection:
            return False

        try:
            cursor = self.connection.cursor()
            cursor.execute(f"UPDATE accounts_db SET is_banned = 0, banned_timestamp = 0 WHERE {column}=?", (identifier,))

            self.connection.commit()

            return True  # Ban removed successfully

        except sqlite3.Error as e:
            self.logger.log("ERROR", f"Error removing ban: {e}")
            return False

    def is_user_banned(self, column, identifier):
        if not self.connection:
            return False, None  # Indicates the user is not banned and there's no remaining time

        try:
            cursor = self.connection.cursor()
            cursor.execute(f"SELECT is_banned, banned_timestamp FROM accounts_db WHERE {column}=?", (identifier,))

            row = cursor.fetchone()
            if not row:
                return False, None  # User not found

            is_banned, banned_timestamp = row
            if is_banned:
                current_time = time.time()
                # If the banned_timestamp is in the future, compute the remaining time
                if banned_timestamp > current_time:
                    remaining_time = banned_timestamp - current_time

                    # Convert remaining_time to day(s), hour(s), and second(s)
                    days, remainder = divmod(remaining_time, 86400)
                    hours, seconds = divmod(remainder, 3600)
                    minutes, seconds = divmod(seconds, 60)
                    time_str = f"{int(days)} day(s) {int(hours)} hour(s) {int(minutes)} minute(s) {int(seconds)} second(s)"
                    
                    return True, time_str
                else:
                    self.remove_ban(column, identifier)
                    return False, None  # Ban has expired
            else:
                return False, None  # User is not banned

        except sqlite3.Error as e:
            self.logger.log("ERROR", f"Error fetching data: {e}")
            return False, None

    def get_identifier_column(self, identifier):
        if self.account_exists("id", identifier):
            return "id"
        elif self.account_exists("username", identifier):
            return "username"
        else:
            return False

    def __del__(self):
        if self.connection:
            self.connection.close()