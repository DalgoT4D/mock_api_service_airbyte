import jwt
from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader
from typing import Dict, Optional
import os

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=True)

def decode_api_key(api_key: str) -> Dict:
    """
    Decode the API key to extract configuration parameters.
    The API key should be a JWT token containing:
    - total_records: Total number of records to mock
    - response_delay: Delay in seconds for each API response (default: 0.01)
    """
    try:
        secret = os.getenv("JWT_SECRET", "your-secret-key-change-in-production")
        decoded = jwt.decode(api_key, secret, algorithms=["HS256"])
        return decoded
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="API key has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid API key")

def get_api_key_data(api_key: str = Security(api_key_header)) -> Dict:
    """
    Dependency to validate and decode API key from request header.
    """
    return decode_api_key(api_key)