from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class PaginationParams(BaseModel):
    page: int = 1
    page_size: int = 10

class PaginatedResponse(BaseModel):
    data: Optional[List[Dict[str, Any]]]
    page: int
    page_size: int
    total_records: int
    total_pages: int
    has_next: bool
    has_previous: bool