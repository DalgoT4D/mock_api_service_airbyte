from fastapi import FastAPI, Query, Depends, HTTPException
from typing import Dict, Optional
import math
import asyncio
from dotenv import load_dotenv

from auth import get_api_key_data
from models import PaginatedResponse
from mock_data import (
    generate_student,
    generate_school,
    generate_village,
    get_paginated_data
)

load_dotenv()

app = FastAPI(
    title="Mock API Service",
    description="A mock API service with API key authentication and pagination",
    version="1.0.0"
)

@app.get("/")
def root():
    return {
        "message": "Mock API Service",
        "endpoints": ["/api/students", "/api/schools", "/api/villages"],
        "authentication": "API Key required in X-API-Key header"
    }

@app.get("/api/students", response_model=PaginatedResponse)
async def get_students(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=1000, description="Items per page"),
    api_key_data: Dict = Depends(get_api_key_data)
):
    """
    Get paginated list of students.
    Requires API key authentication.
    """
    # Add configurable delay
    response_delay = api_key_data.get("response_delay", 0.01)
    await asyncio.sleep(response_delay)
    
    total_records = api_key_data.get("total_records", 100)
    total_pages = math.ceil(total_records / page_size)
    
    data = get_paginated_data(
        generate_student,
        total_records,
        page,
        page_size
    )
    
    return PaginatedResponse(
        data=data,
        page=page,
        page_size=page_size,
        total_records=total_records,
        total_pages=total_pages,
        has_next=page < total_pages,
        has_previous=page > 1
    )

@app.get("/api/schools", response_model=PaginatedResponse)
async def get_schools(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=1000, description="Items per page"),
    api_key_data: Dict = Depends(get_api_key_data)
):
    """
    Get paginated list of schools.
    Requires API key authentication.
    """
    # Add configurable delay
    response_delay = api_key_data.get("response_delay", 0.01)
    await asyncio.sleep(response_delay)
    
    total_records = api_key_data.get("total_records", 100)
    total_pages = math.ceil(total_records / page_size)
    
    data = get_paginated_data(
        generate_school,
        total_records,
        page,
        page_size
    )
    
    return PaginatedResponse(
        data=data,
        page=page,
        page_size=page_size,
        total_records=total_records,
        total_pages=total_pages,
        has_next=page < total_pages,
        has_previous=page > 1
    )

@app.get("/api/villages", response_model=PaginatedResponse)
async def get_villages(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=1000, description="Items per page"),
    api_key_data: Dict = Depends(get_api_key_data)
):
    """
    Get paginated list of villages.
    Requires API key authentication.
    """
    # Add configurable delay
    response_delay = api_key_data.get("response_delay", 0.01)
    await asyncio.sleep(response_delay)
    
    total_records = api_key_data.get("total_records", 100)
    total_pages = math.ceil(total_records / page_size)
    
    data = get_paginated_data(
        generate_village,
        total_records,
        page,
        page_size
    )
    
    return PaginatedResponse(
        data=data,
        page=page,
        page_size=page_size,
        total_records=total_records,
        total_pages=total_pages,
        has_next=page < total_pages,
        has_previous=page > 1
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
