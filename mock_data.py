from faker import Faker
from typing import List, Dict, Optional
import hashlib

fake = Faker()

def generate_stable_id(entity_type: str, index: int) -> str:
    """Generate a stable ID based on entity type and index"""
    return hashlib.md5(f"{entity_type}_{index}".encode()).hexdigest()[:12]

def generate_student(index: int) -> Dict:
    """Generate a mock student record"""
    fake.seed_instance(index)  # Ensure consistent data for same index
    return {
        "id": generate_stable_id("student", index),
        "student_id": f"STU{index:06d}",
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": f"student{index}@school.edu",
        "grade": fake.random_int(min=1, max=12),
        "age": fake.random_int(min=6, max=18),
        "enrollment_date": fake.date_between(start_date='-3y', end_date='today').isoformat(),
        "school_id": generate_stable_id("school", (index % 50) + 1),
        "village_id": generate_stable_id("village", (index % 20) + 1),
        "status": fake.random_element(["active", "inactive", "graduated"]),
        "gpa": round(fake.random.uniform(2.0, 4.0), 2)
    }

def generate_school(index: int) -> Dict:
    """Generate a mock school record"""
    fake.seed_instance(index + 10000)  # Different seed for schools
    school_types = ["Elementary", "Middle", "High", "K-12"]
    return {
        "id": generate_stable_id("school", index),
        "school_id": f"SCH{index:04d}",
        "name": f"{fake.last_name()} {fake.random_element(school_types)} School",
        "address": fake.street_address(),
        "city": fake.city(),
        "state": fake.state_abbr(),
        "zip_code": fake.zipcode(),
        "phone": fake.phone_number(),
        "email": f"admin@school{index}.edu",
        "principal": fake.name(),
        "student_count": fake.random_int(min=100, max=2000),
        "teacher_count": fake.random_int(min=10, max=100),
        "founded_year": fake.random_int(min=1900, max=2020),
        "school_type": fake.random_element(school_types),
        "village_id": generate_stable_id("village", (index % 20) + 1),
        "rating": round(fake.random.uniform(3.0, 5.0), 1)
    }

def generate_village(index: int) -> Dict:
    """Generate a mock village record"""
    fake.seed_instance(index + 20000)  # Different seed for villages
    return {
        "id": generate_stable_id("village", index),
        "village_id": f"VIL{index:03d}",
        "name": f"{fake.city()} Village",
        "population": fake.random_int(min=1000, max=50000),
        "area_sq_km": round(fake.random.uniform(10.0, 500.0), 2),
        "district": fake.city(),
        "state": fake.state(),
        "country": "USA",
        "postal_code": fake.zipcode(),
        "mayor": fake.name(),
        "established_year": fake.random_int(min=1700, max=1950),
        "schools_count": fake.random_int(min=1, max=10),
        "literacy_rate": round(fake.random.uniform(70.0, 99.9), 1),
        "coordinates": {
            "latitude": float(fake.latitude()),
            "longitude": float(fake.longitude())
        }
    }

def get_paginated_data(
    generator_func,
    total_records: int,
    page: int,
    page_size: int
) -> Optional[List[Dict]]:
    """
    Generate paginated mock data.
    Returns None if page is out of range.
    """
    if page < 1 or page_size < 1:
        return []
    
    start_index = (page - 1) * page_size
    end_index = min(start_index + page_size, total_records)
    
    if start_index >= total_records:
        return None  # Page out of range
    
    # Generate data for the requested page
    data = []
    for i in range(start_index, end_index):
        data.append(generator_func(i + 1))  # +1 to make index 1-based
    
    return data