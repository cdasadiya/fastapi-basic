# 🚀 FastAPI Basic - Complete Learning Guide

<div align="center">

![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688?style=flat-square&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3.7+-3776ab?style=flat-square&logo=python)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)

A comprehensive playground and learning resource for FastAPI fundamentals with practical examples and best practices.

</div>

---

## 📑 Table of Contents

- [1. What is an API?](#1-what-is-an-api)
- [2. What is FastAPI?](#2-what-is-fastapi-how-is-it-different)
- [3. CRUD Operations](#3-crud--handling-data-operations)
- [4. HTTP Protocol](#4-http-protocol--client--server-communication)
- [5. HTTP Methods](#5-http-methods)
- [6. Path Parameters](#6-path-parameters)
- [7. Path() Function](#7-path-function-in-fastapi)
- [8. HTTP Status Codes](#8-http-status-codes)
- [9. HTTPException](#9-httpexception)
- [10. Query Parameters](#10-query-parameters)
- [License & Author](#-license--author)

---

## 1. What is an API?

**API (Application Programming Interface)** = contract between two software systems. One system exposes functionality; another consumes it — without knowing internal implementation.

### Real-world Analogy 🍽️
Restaurant menu. You (client) order from the menu (API). Kitchen (server) processes and returns food (response). You never enter the kitchen.

### Concrete Example

```
You open a weather app → app calls OpenWeatherMap API →
API returns JSON → app displays "32°C, Sunny"
```

```json
GET https://api.openweathermap.org/data/2.5/weather?q=Delhi

Response:
{
  "city": "Delhi",
  "temp": 32,
  "condition": "Sunny"
}
```

---

## 2. What is FastAPI? How is it Different?

**"Regular API"** = broad concept (any interface between systems).  
**FastAPI** = specific Python *framework* to **build** APIs.

### Comparison Table

| Feature | Flask/Django (older) | FastAPI |
|---|---|---|
| Speed | Slower | ⚡ One of the fastest Python frameworks |
| Type hints | Manual/optional | ✅ Built-in, enforced via Pydantic |
| Auto docs | ❌ No | ✅ Yes — Swagger UI + ReDoc auto-generated |
| Async support | Limited | ✅ Native `async/await` |
| Validation | Manual | ✅ Automatic via type hints |

### Minimal FastAPI App

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/hello")
def greet():
    return {"message": "Hello, World!"}
```

Run → visit `http://127.0.0.1:8000/docs` → interactive Swagger UI appears automatically.

---

## 3. CRUD — Handling Data Operations

CRUD = the four fundamental data operations any software performs.

| Operation | HTTP Method | SQL | Example |
|---|---|---|---|
| **C**reate | POST | INSERT | Add new patient |
| **R**ead | GET | SELECT | Fetch patient by ID |
| **U**pdate | PUT / PATCH | UPDATE | Edit patient details |
| **D**elete | DELETE | DELETE | Remove patient record |

### Static Data Example (Dict/List in Memory)

```python
patients = {}  # in-memory store

@app.post("/patients")       # Create
@app.get("/patients/{id}")   # Read
@app.put("/patients/{id}")   # Update
@app.delete("/patients/{id}")# Delete
```

**Dynamic data (database):** Replace `patients = {}` with DB queries — CRUD logic stays identical; only the storage layer changes.

---

## 4. HTTP Protocol — Client ↔ Server Communication

**HTTP (HyperText Transfer Protocol)** = language client and server use to talk.

```
CLIENT                        SERVER
  |                              |
  |--- HTTP Request -----------> |
  |    Method: GET               |
  |    URL: /patients/42         |
  |    Headers: {Accept: JSON}   |
  |                              |
  |<-- HTTP Response ----------- |
  |    Status: 200 OK            |
  |    Body: {"id": 42, ...}     |
```

### Every HTTP Interaction Has:

- **Request:** method + URL + headers + (optional) body
- **Response:** status code + headers + body

### Role in API Call:

1. Client sends HTTP request to API endpoint
2. FastAPI receives, routes to correct function
3. Function processes, returns data
4. FastAPI wraps data in HTTP response
5. Client reads response

---

## 5. HTTP Methods

| Method | Purpose | Has Body? | Example |
|---|---|---|---|
| `GET` | Fetch data | No | Get patient list |
| `POST` | Create new resource | Yes | Add new patient |
| `PUT` | Replace entire resource | Yes | Update all patient fields |
| `PATCH` | Update partial resource | Yes | Update only phone number |
| `DELETE` | Remove resource | No | Delete patient |

### Complete CRUD Example

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
db = {}

class Patient(BaseModel):
    name: str
    age: int

@app.get("/patients")
def get_all():
    """Fetch all patients"""
    return db

@app.get("/patients/{pid}")
def get_one(pid: int):
    """Fetch single patient by ID"""
    return db[pid]

@app.post("/patients")
def create(patient: Patient):
    """Create new patient"""
    db[len(db)+1] = patient
    return {"message": "Created"}

@app.put("/patients/{pid}")
def update(pid: int, patient: Patient):
    """Replace entire patient record"""
    db[pid] = patient
    return {"message": "Updated"}

@app.delete("/patients/{pid}")
def delete(pid: int):
    """Delete patient record"""
    del db[pid]
    return {"message": "Deleted"}
```

---

## 6. Path Parameters

**Path parameters** = dynamic segments embedded directly in the URL path to identify a specific resource.

```
/patients/{patient_id}
           ^^^^^^^^^^^
           path parameter — changes per request
```

### Real Examples

```
/patients/42      → fetch patient with ID 42
/patients/99      → fetch patient with ID 99
/doctors/7/slots  → fetch slots for doctor 7
```

### FastAPI Usage

```python
@app.get("/patients/{patient_id}")
def get_patient(patient_id: int):
    # patient_id extracted automatically from URL
    return {"id": patient_id}
```

FastAPI automatically:
- ✅ Extracts value from URL
- ✅ Converts to declared type (`int`)
- ✅ Returns 422 if type mismatch

---

## 7. `Path()` Function in FastAPI

`Path()` adds **validation + metadata** to path parameters. Without it, parameters work but have no docs or constraints. With it, Swagger UI shows rich documentation and server rejects invalid inputs before your code runs.

### Basic Example

```python
from fastapi import FastAPI, Path

app = FastAPI()

@app.get("/patients/{patient_id}")
def get_patient(
    patient_id: int = Path(
        title="Patient ID",
        description="Unique numeric ID of the patient in the system",
        example=42,
        ge=1,          # must be >= 1
        lt=10000       # must be < 10000
    )
):
    return {"patient_id": patient_id}
```

### All `Path()` Parameters

| Parameter | Purpose | Example |
|---|---|---|
| `title` | Label in Swagger UI | `"Patient ID"` |
| `description` | Detailed explanation in docs | `"Numeric ID, 1–9999"` |
| `example` | Sample value shown in docs | `42` |
| `ge` | Greater than or equal | `ge=1` → rejects 0, negatives |
| `gt` | Strictly greater than | `gt=0` → rejects 0 |
| `le` | Less than or equal | `le=100` |
| `lt` | Strictly less than | `lt=10000` |
| `min_length` | Min string length | `min_length=3` |
| `max_length` | Max string length | `max_length=20` |
| `regex` | Pattern match | `regex="^P[0-9]+"` |

### String Path Parameter with Regex

```python
@app.get("/records/{record_code}")
def get_record(
    record_code: str = Path(
        title="Record Code",
        description="Format: REC- followed by digits",
        min_length=5,
        max_length=10,
        regex=r"^REC-\d+$",   # must match REC-123
        example="REC-4521"
    )
):
    return {"code": record_code}
```

Requesting `/records/INVALID` → FastAPI returns `422 Unprocessable Entity` automatically.

---

## 8. HTTP Status Codes

3-digit code in every HTTP response. First digit = category.

### Status Code Categories

| Range | Category | Meaning |
|---|---|---|
| `1xx` | ℹ️ Informational | Request received, processing |
| `2xx` | ✅ Success | Request succeeded |
| `3xx` | 🔄 Redirection | Resource moved |
| `4xx` | ⚠️ Client Error | Bad request from client |
| `5xx` | 🔴 Server Error | Server failed |

### Common Codes in APIs

| Code | Name | When to use |
|---|---|---|
| `200` | OK | GET/PUT/DELETE succeeded |
| `201` | Created | POST created a new resource |
| `204` | No Content | DELETE succeeded, nothing to return |
| `400` | Bad Request | Invalid input from client |
| `401` | Unauthorized | Not authenticated |
| `403` | Forbidden | Authenticated but no permission |
| `404` | Not Found | Resource doesn't exist |
| `422` | Unprocessable Entity | Validation failed (FastAPI default) |
| `500` | Internal Server Error | Bug/crash on server |

### Set Custom Status Code

```python
from fastapi import FastAPI
from fastapi import status

app = FastAPI()

@app.post("/patients", status_code=status.HTTP_201_CREATED)
def create_patient(name: str):
    # If we reach here, response will be 201, not 200
    return {"name": name, "message": "Patient created"}
```

---

## 9. HTTPException

When something goes wrong (patient not found, invalid access), FastAPI should return a proper error — not crash or return `200 OK` with an error message buried in JSON.

`HTTPException` does this cleanly.

### Basic Example

```python
from fastapi import FastAPI, HTTPException

app = FastAPI()

patients = {1: "Alice", 2: "Bob"}

@app.get("/patients/{pid}")
def get_patient(pid: int):
    if pid not in patients:
        raise HTTPException(
            status_code=404,
            detail=f"Patient with ID {pid} not found"
        )
    return {"name": patients[pid]}
```

**Request:** `GET /patients/99`  
**Response:**
```json
HTTP 404 Not Found
{
  "detail": "Patient with ID 99 not found"
}
```

### With Custom Headers (e.g., Auth Errors)

```python
raise HTTPException(
    status_code=401,
    detail="Token expired. Please log in again.",
    headers={"WWW-Authenticate": "Bearer"}
)
```

### Common Patterns

| Scenario | Code | Detail message |
|---|---|---|
| Record not found | `404` | `"Patient {id} not found"` |
| Duplicate entry | `400` | `"Patient already exists"` |
| No permission | `403` | `"Access denied"` |
| Invalid input | `400` | `"Age must be positive"` |

---

## 10. Query Parameters

**Query parameters** = key-value pairs after `?` in URL. Don't change the endpoint path — used for filtering, sorting, searching, pagination.

```
/patients?city=Delhi&sort_by=age&page=2
          ^          ^            ^
          filter     sort         pagination
```

### Structure

- `?` starts the query string
- `key=value` pairs
- `&` separates multiple parameters

### FastAPI — Automatic Detection

Any function parameter not in the path `{}` is treated as a query parameter.

```python
@app.get("/patients")
def get_patients(city: str, sort_by: str = "name"):
    # city → required query param
    # sort_by → optional, defaults to "name"
    return {"city": city, "sort_by": sort_by}
```

Calling `/patients?city=Delhi` → `city="Delhi"`, `sort_by="name"`

### `Query()` Function

Like `Path()`, but for query parameters. Adds validation, defaults, and Swagger metadata.

```python
from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/patients")
def search_patients(
    city: str = Query(
        default="Mumbai",
        title="City Filter",
        description="Filter patients by city of residence",
        example="Delhi",
        min_length=2,
        max_length=50
    ),
    min_age: int = Query(
        default=0,
        ge=0,
        le=150,
        description="Minimum age filter"
    ),
    sort_by: str = Query(
        default="name",
        regex="^(name|age|city)$",   # only these 3 values allowed
        description="Sort field: name, age, or city"
    ),
    page: int = Query(
        default=1,
        ge=1,
        description="Page number for pagination"
    )
):
    return {
        "city": city,
        "min_age": min_age,
        "sort_by": sort_by,
        "page": page
    }
```

**Sample request:** `/patients?city=Delhi&min_age=30&sort_by=age&page=2`

### All `Query()` Parameters

| Parameter | Purpose | Example |
|---|---|---|
| `default` | Default if not provided | `Query("Mumbai")` |
| `title` | Label in Swagger | `"City Filter"` |
| `description` | Explanation in docs | `"Filter by city"` |
| `example` | Sample value in docs | `"Delhi"` |
| `examples` | Multiple named samples | `{"ex1": {...}}` |
| `min_length` | Min string length | `min_length=2` |
| `max_length` | Max string length | `max_length=100` |
| `ge` | Numeric ≥ | `ge=0` |
| `gt` | Numeric > | `gt=0` |
| `le` | Numeric ≤ | `le=150` |
| `lt` | Numeric < | `lt=200` |
| `regex` | Pattern constraint | `regex="^[A-Z]+"` |

### Quick Reference — Path vs Query Parameters

| Feature | Path Parameter | Query Parameter |
|---|---|---|
| Position in URL | Inside path: `/items/{id}` | After `?`: `?id=5` |
| Required? | Always required | Optional (can have default) |
| Purpose | Identify resource | Filter / sort / paginate |
| FastAPI function | `Path()` | `Query()` |
| Example | `/patients/42` | `/patients?city=Delhi` |

---

## 🚀 Getting Started

### Installation

```bash
# Install FastAPI
pip install fastapi

# Install Uvicorn (ASGI server)
pip install uvicorn

# Or install both
pip install fastapi uvicorn
```

### Run Your First API

```bash
# Create a file: main.py
uvicorn main:app --reload
```

Visit: `http://127.0.0.1:8000/docs` for interactive Swagger UI

---

## 📚 Quick Tips

- ✅ Use **type hints** — FastAPI uses them for validation
- ✅ Use **Path()** and **Query()** for better documentation
- ✅ Always return appropriate **HTTP status codes**
- ✅ Use **HTTPException** for error handling
- ✅ Check Swagger UI at `/docs` endpoint
- ✅ Use async functions for better performance

---

## 📋 License & Author

<div align="center">

### MIT License

This project is licensed under the MIT License - see below for details.

```
Copyright (c) 2026 cdasadiya

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

### Author

**👤 [cdasadiya](https://github.com/cdasadiya)**

- 🐙 GitHub: [@cdasadiya](https://github.com/cdasadiya)
- 💼 Repository: [fastapi-basic](https://github.com/cdasadiya/fastapi-basic)

---

### 💡 Contributing

Found a bug or have a suggestion? Feel free to open an issue or submit a pull request!

### ⭐ Support

If you found this guide helpful, please give it a star! 🌟

---

<sub>Last updated: May 2026</sub>

</div>