# Mock API Service

A FastAPI-based mock service with JWT-based API key authentication and pagination support for testing Airbyte connectors or any data integration workflows.

## Features

- **JWT-based API Key Authentication**: Configurable parameters encoded in the token
- **Three Mock Endpoints**: `/api/students`, `/api/schools`, `/api/villages`
- **Pagination Support**: Query parameters for flexible data retrieval
- **Consistent Mock Data**: Stable IDs using hash-based generation
- **Configurable Total Records**: Set via API key payload
- **Configurable Response Delay**: Control API response time via API key
- **No Database Required**: All data generated on-the-fly
- **Out-of-Range Handling**: Returns `null` for pages beyond available data

## Installation

This project uses `uv` for dependency management:

```bash
# Install dependencies
uv sync
```

## Configuration

### Environment Variables

Create or update `.env` file:

```bash
JWT_SECRET=your-secret-key-change-in-production
```

### API Key Structure

API keys are JWT tokens containing:
- `total_records`: Total number of records to mock (determines dataset size)
- `response_delay`: Delay in seconds for each API response (default: 0.01)
- `exp`: Token expiration timestamp
- `iat`: Token issued at timestamp
- `sub`: Subject identifier

## Running the Service

```bash
# Default port 8000
uv run uvicorn main:app --reload

# Custom port
uv run uvicorn main:app --reload --port 9008
```

The service will be available at:
- API: http://localhost:9008
- Swagger UI: http://localhost:9008/docs
- ReDoc: http://localhost:9008/redoc

## Generating API Keys

```bash
# Generate with defaults (100 records, 0.01s delay)
uv run python generate_api_key.py

# Generate with custom record count
uv run python generate_api_key.py 500

# Generate with custom record count and response delay
uv run python generate_api_key.py 500 0.5  # 500 records, 0.5 second delay

# Example output:
# ============================================================
# Generated API Key:
# ============================================================
# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
# ============================================================
```

## API Endpoints

### Authentication

All endpoints require an API key in the header:

```
X-API-Key: YOUR_JWT_TOKEN_HERE
```

### 1. Students Endpoint

```http
GET /api/students?page=1&page_size=10
```

**Response Fields:**
- `id`: Stable hash-based ID
- `student_id`: Sequential student ID
- `first_name`, `last_name`: Generated names
- `email`: Student email
- `grade`: Grade level (1-12)
- `age`: Student age (6-18)
- `enrollment_date`: ISO date
- `school_id`: Associated school
- `village_id`: Associated village
- `status`: active/inactive/graduated
- `gpa`: Grade point average

### 2. Schools Endpoint

```http
GET /api/schools?page=1&page_size=10
```

**Response Fields:**
- `id`: Stable hash-based ID
- `school_id`: Sequential school ID
- `name`: School name
- `address`, `city`, `state`, `zip_code`: Location
- `phone`, `email`: Contact info
- `principal`: Principal name
- `student_count`, `teacher_count`: Statistics
- `founded_year`: Establishment year
- `school_type`: Elementary/Middle/High/K-12
- `village_id`: Associated village
- `rating`: School rating (3.0-5.0)

### 3. Villages Endpoint

```http
GET /api/villages?page=1&page_size=10
```

**Response Fields:**
- `id`: Stable hash-based ID
- `village_id`: Sequential village ID
- `name`: Village name
- `population`: Population count
- `area_sq_km`: Area in square kilometers
- `district`, `state`, `country`: Location hierarchy
- `postal_code`: ZIP code
- `mayor`: Mayor name
- `established_year`: Foundation year
- `schools_count`: Number of schools
- `literacy_rate`: Percentage
- `coordinates`: Latitude and longitude

## Pagination

All endpoints support pagination with:

**Query Parameters:**
- `page`: Page number (default: 1, min: 1)
- `page_size`: Items per page (default: 10, min: 1, max: 1000)

**Response Format:**

```json
{
  "data": [],
  "page": 1,
  "page_size": 10,
  "total_records": 200,
  "total_pages": 20,
  "has_next": true,
  "has_previous": false
}
```

Note: `data` field returns `null` when page exceeds total_pages

## Testing Examples

```bash
# Set API key variable
API_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

# Test students endpoint
curl -H "X-API-Key: $API_KEY" \
  "http://localhost:9008/api/students?page=1&page_size=5"

# Test schools with pagination
curl -H "X-API-Key: $API_KEY" \
  "http://localhost:9008/api/schools?page=2&page_size=10"

# Test villages - out of range (returns null)
curl -H "X-API-Key: $API_KEY" \
  "http://localhost:9008/api/villages?page=100&page_size=10"

# Test without authentication (returns 401)
curl "http://localhost:9008/api/students"
```

## Data Consistency

- **Stable IDs**: Uses MD5 hashing of entity type and index
- **Seeded Faker**: Ensures same data for same index across requests
- **Relationships**: Students and schools are linked to villages
- **Deterministic**: Same API key configuration produces same data

## Use Cases

- Testing Airbyte source connectors
- API integration testing
- Load testing with predictable data
- Development environment mock services
- Pagination implementation testing

## Security Notes

- Change `JWT_SECRET` in production
- API keys have expiration dates (default: 30 days)
- No data persistence - all in-memory generation
- Token validation on every request

## License

MIT