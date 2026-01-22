from datetime import datetime
from typing import Dict


def get_current_date() -> Dict[str, str]:
    """
    Get the current date in YYYY-MM-DD format.
    """
    return {"current_date": datetime.now().strftime("%Y-%m-%d")}

def get_current_time() -> Dict[str, str]:
    """
    Get the current time in HH:MM:SS format.
    """
    return {"current_time": datetime.now().strftime("%H:%M:%S")}