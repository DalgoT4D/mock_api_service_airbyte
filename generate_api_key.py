#!/usr/bin/env python3
"""
Utility script to generate API keys for testing.
API keys are JWT tokens containing configuration parameters.
"""

import jwt
import datetime
import sys
import os
from dotenv import load_dotenv

load_dotenv()

def generate_api_key(total_records: int = 100, expiry_days: int = 30):
    """
    Generate an API key (JWT token) with the specified parameters.
    
    Args:
        total_records: Number of total records the API should mock
        expiry_days: Number of days until the token expires
    
    Returns:
        JWT token string
    """
    secret = os.getenv("JWT_SECRET", "your-secret-key-change-in-production")
    
    payload = {
        "total_records": total_records,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=expiry_days),
        "iat": datetime.datetime.utcnow(),
        "sub": "mock-api-client"
    }
    
    token = jwt.encode(payload, secret, algorithm="HS256")
    return token

def main():
    if len(sys.argv) > 1:
        try:
            total_records = int(sys.argv[1])
        except ValueError:
            print("Usage: python generate_api_key.py [total_records]")
            print("Example: python generate_api_key.py 500")
            sys.exit(1)
    else:
        total_records = 100
    
    api_key = generate_api_key(total_records)
    
    print("\n" + "="*60)
    print("Generated API Key:")
    print("="*60)
    print(api_key)
    print("="*60)
    print(f"\nConfiguration:")
    print(f"  - Total Records: {total_records}")
    print(f"  - Expiry: 30 days from now")
    print("\nUsage:")
    print("  Add this to your request headers:")
    print(f"  X-API-Key: {api_key}")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()