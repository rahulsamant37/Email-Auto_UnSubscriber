"""Configuration utilities for the Auto Email Unsubscriber."""
import os

def check_env_variables():
    """
    Check if required environment variables are set.
    
    Returns:
        bool: True if all required variables are set, False otherwise
    """
    username = os.getenv("EMAIL")
    password = os.getenv("PASSWORD")
    
    if not username:
        print("ERROR: EMAIL environment variable is not set in .env file")
        return False
    if not password:
        print("ERROR: PASSWORD environment variable is not set in .env file")
        return False
    return True