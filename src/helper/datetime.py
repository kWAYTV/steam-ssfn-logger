import pytz
from datetime import datetime

class DateTime:
    def __init__(self):
        return

    def get_current_timestamp(self):
        # Set the timezone to Central European Time (Spain)
        timezone = pytz.timezone('Europe/Madrid')
        # Get the current time in the specified timezone
        current_time = datetime.now(timezone)
        # Set the embed timestamp to the current time
        return current_time