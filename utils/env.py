import os
from typing import Any
from dotenv import load_dotenv

load_dotenv()

def env(key: str, default: Any = None, split: bool = False, as_bool: bool = False):
    """
    Fetch an environment variable from the .env file.
    
    :param key: The environment variable name.
    :param default: The default value to return if the key is not found.
    :param split: If True, split the value by comma and return as a list.
    :param as_bool: If True, consider the value as a boolean value and return it as bool instead of string.
    :return: The value as a string or a list of strings.
    """
    value = os.getenv(key)
    
    if value is None:
        return default
    
    if split:
        return [v.strip() for v in value.split(',') if v.strip()]
    
    if as_bool:
        return value.strip().lower() in ('true', '1', 'yes', 'on')

    return value
