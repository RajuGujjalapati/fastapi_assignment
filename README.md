# FastAPI Address Book

This is a simple FastAPI-based address book application that allows users to create, update, and delete addresses. The addresses are stored in an SQLite database, and input data is validated.

## Prerequisites

Before you get started, make sure you have the following prerequisites installed on your system:

- Python 3.6+
- Git (optional, if you want to clone the repository)

## Setup

1. Clone the repository (optional):

   ```bash
   git clone https://github.com/RajuGujjalapati/fastapi_assignment.git
   cd fastapi-assignment
2. create a virtual environment
  python -m venv venv
  source venv/bin/activate  # On Windows, use: venv\Scripts\activate
3. pip install -r requirements.txt
4. Start the FastAPI application using Uvicorn:
    ``` uvicorn main:app --reload ```
    Replace main with the filename (without the .py extension) where your FastAPI instance (app) is defined.

    The application will be accessible at http://127.0.0.1:8000.

5. Access Swagger Documentation
    To access the Swagger documentation for the API, open your web browser and go to:

    http://127.0.0.1:8000/docs

6. Sample Data
To add sample data, you can use tools like curl or Postman to send POST requests to the /addresses/ endpoint with sample JSON data. Here's an example JSON data:
  ```bash
  {
      "latitude": 40.7128,
      "longitude": -74.0060,
      "name": "Sample Address",
      "address": "123 Main St",
      "city": "Sample City",
      "state": "Sample State",
      "zip_code": "12345"
  }

```
Send a POST request to http://127.0.0.1:8000/addresses/ to create a new address.

Followed by all other API's for CRUD operations.
check the sample PDF for execution flow.


