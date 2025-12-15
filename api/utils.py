import hashlib
import hmac
import json
import os
import secrets
import string

def generate_secret(length: int = 32) -> str:
    """Generate a secret key using the secrets module."""
    return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(length))

def generate_api_key(length: int = 32) -> str:
    """Generate an API key using the secrets module."""
    return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(length))

def sign_request(request: dict, secret_key: str) -> dict:
    """Sign a request using the HMAC algorithm."""
    signature = hmac.new(secret_key.encode(), json.dumps(request, sort_keys=True).encode(), hashlib.sha256).hexdigest()
    return {**request, 'signature': signature}

def verify_request(request: dict, secret_key: str) -> bool:
    """Verify a request signature using the HMAC algorithm."""
    try:
        expected_signature = hmac.new(secret_key.encode(), json.dumps(request, sort_keys=True).encode(), hashlib.sha256).hexdigest()
        return hmac.compare_digest(request.get('signature'), expected_signature)
    except (ValueError, KeyError):
        return False

def load_environment_variables() -> dict:
    """Load environment variables from a file named '.env'."""
    if os.path.exists('.env'):
        with open('.env', 'r') as file:
            return {key: value.strip() for key, value in [line.split('=') for line in file.readlines()]}
    else:
        return {}

def save_environment_variables(env_variables: dict) -> None:
    """Save environment variables to a file named '.env'."""
    with open('.env', 'w') as file:
        for key, value in env_variables.items():
            file.write(f'{key}={value}\n')