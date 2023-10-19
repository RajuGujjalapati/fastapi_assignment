from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy import orm
from typing import List

# Create a FastAPI instance
app = FastAPI()

# Define a SQLite database and create tables

# Define the database URL, which is a SQLite database located at './address_book.db'.
DATABASE_URL = "sqlite:///./address_book.db"

# Create an SQLAlchemy database engine using the defined URL.
engine = create_engine(DATABASE_URL)

# Create a session factory using SQLAlchemy's sessionmaker.
# The session will manage database connections and transactions.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define the base for the ORM models, which includes table schema definitions.
Base = orm.declarative_base()


# Define the "addresses" table in the database

# Create an SQLAlchemy model for the "addresses" table. Each field in the model
# corresponds to a column in the table. SQLAlchemy will use this model to map
# data between Python objects and the database table.
class Address(Base):
    # Set the table name to "addresses".
    __tablename__ = "addresses"

    # Define the columns in the table.
    id = Column(Integer, primary_key=True, index=True)
    latitude = Column(Float)
    longitude = Column(Float)
    name = Column(String, index=True)
    address = Column(String)
    city = Column(String)
    state = Column(String)
    zip_code = Column(String)


# Create the database tables

# Use the Base metadata to create the database tables in the engine.
Base.metadata.create_all(bind=engine)


# Pydantic model for input data when creating an address

# Define a Pydantic model to validate and parse input data when creating an address.
class AddressCreate(BaseModel):
    latitude: float
    longitude: float
    name: str
    address: str
    city: str
    state: str
    zip_code: str


# Pydantic model for the response when creating or updating an address

# Define a Pydantic model for the response when creating or updating an address.
# This model is used to specify the expected structure of the JSON response.
class AddressResponse(AddressCreate):
    id: int


# Route to create an address with input validation

# Define an API route to create an address. Use the `response_model` parameter to
# specify the Pydantic model to use for the response. Add a summary and description
# for documentation purposes.
@app.post("/addresses/", response_model=AddressResponse, summary="Create Address", description="Create a new address")
def create_address(address: AddressCreate):
    # Create a database session.
    db = SessionLocal()

    # Create an Address object from the input data and add it to the session.
    db_address = Address(**address.dict())
    db.add(db_address)

    # Commit the transaction to save the new address to the database.
    db.commit()

    # Refresh the object to get any updated values from the database.
    db.refresh(db_address)

    # Close the session to release the database connection.
    db.close()

    # Return the newly created address.
    return db_address


# Route to get a list of addresses

# Define an API route to get a list of addresses. Use the `response_model` parameter
# to specify the Pydantic model for the response. Add a summary and description for
# documentation.
@app.get("/addresses/", response_model=List[AddressResponse], summary="List Addresses",
         description="Get a list of addresses")
def read_addresses(skip: int = 0, limit: int = 10):
    # Create a database session.
    db = SessionLocal()

    # Query the database for addresses, offsetting and limiting the results.
    addresses = db.query(Address).offset(skip).limit(limit).all()

    # Close the session to release the database connection.
    db.close()

    # Return the list of addresses.
    return addresses


# Route to get a single address by ID

# Define an API route to get a single address by ID. Use the `response_model` parameter
# to specify the Pydantic model for the response. Add a summary and description for
# documentation.
@app.get("/addresses/{address_id}", response_model=AddressResponse, summary="Get Address",
         description="Get a single address by ID")
def read_address(address_id: int):
    # Create a database session.
    db = SessionLocal()

    # Query the database for an address with the specified ID.
    address = db.query(Address).filter(Address.id == address_id).first()

    # Close the session to release the database connection.
    db.close()

    # If the address is not found, raise an HTTP exception with a 404 status code.
    if address is None:
        raise HTTPException(status_code=404, detail="Address not found")

    # Return the found address.
    return address


# Route to update an address by ID

# Define an API route to update an address by ID. Use the `response_model` parameter
# to specify the Pydantic model for the response. Add a summary and description for
# documentation.
@app.put("/addresses/{address_id}", response_model=AddressResponse, summary="Update Address",
         description="Update an address by ID")
def update_address(address_id: int, address: AddressCreate):
    # Create a database session.
    db = SessionLocal()

    # Query the database for an address with the specified ID.
    db_address = db.query(Address).filter(Address.id == address_id).first()

    # If the address is not found, raise an HTTP exception with a 404 status code.
    if db_address is None:
        db.close()
        raise HTTPException(status_code=404, detail="Address not found")

    # Update the address object with the new data.
    for key, value in address.dict().items():
        setattr(db_address, key, value)

    # Commit the transaction to save the updated address to the database.
    db.commit()

    # Refresh the object to get any updated values from the database.
    db.refresh(db_address)

    # Close the session to release the database connection.
    db.close()

    # Return the updated address.
    return db_address


# Route to delete an address by ID

# Define an API route to delete an address by ID. Add a summary and description for
# documentation.
@app.delete("/addresses/{address_id}", summary="Delete Address", description="Delete an address by ID")
def delete_address(address_id: int):
    # Create a database session.
    db = SessionLocal()

    # Query the database for an address with the specified ID.
    db_address = db.query(Address).filter(Address.id == address_id).first()

    # If the address is not found, raise an HTTP exception with a 404 status code.
    if db_address is None:
        db.close()
        raise HTTPException(status_code=404, detail="Address not found")

    # Delete the address object.
    db.delete(db_address)
