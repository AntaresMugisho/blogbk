import os
from dotenv import load_dotenv

load_dotenv()

def env(key: str, split: bool = False, as_bool=False):
    """
    Fetch an environment variable from the .env file.
    
    :param key: The environment variable name.
    :param split: If True, split the value by comma and return as a list.
    :return: The value as a string or a list of strings.
    """
    value = os.getenv(key)
    
    if value is None:
        raise KeyError(f"Environment variable '{key}' not found.")
    
    if split:
        return [v.strip() for v in value.split(',') if v.strip()]
    
    if as_bool:
        return value.strip().lower() in ('true', '1', 'yes', 'on')

    return value
