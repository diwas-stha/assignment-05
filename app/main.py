from fastapi import FastAPI, status, HTTPException
from database import Base, engine
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, init_db
from models import Employee
from schemas import EmployeeCreate, EmployeeResponse

from typing import List
app = FastAPI()


app = FastAPI()

# Initialize the database
init_db()

# Dependency to get the database session


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
def create_table():
    Base.metadata.create_all(bind=engine)


@app.get("/employees/", response_model=List[EmployeeResponse])
def get_all_employees(db: Session = Depends(get_db)):
    # Create a new database session
    session = db

    # Get all employees from the database
    employees = session.query(Employee).all()

    # Close the session
    session.close()

    return employees


@app.get("/employees/{employee_id}", response_model=EmployeeResponse)
def get_employee(id: int, db: Session = Depends(get_db)):
    # create a new database session
    session = db

    # Get the employee with the given ID
    employee = session.query(Employee).filter(Employee.id == id).first()

    session.close()

    if not employee:
        raise HTTPException(
            status_code=404, detail=f"Employee with id {id} not found")

    return employee


@app.post("/employees/", response_model=EmployeeResponse)
def insert_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    # Create a new database session
    session = db

    # Create an instance of the Employee database model
    new_employee = Employee(**employee.dict())

    # Add the new employee to the session and commit it
    session.add(new_employee)
    session.commit()

    # Refresh the object to get the auto-generated ID
    session.refresh(new_employee)

    # Close the session
    session.close()

    # Return the newly created employee
    return new_employee


@app.delete("/employees/{employee_id}", response_model=EmployeeResponse)
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    # Create a new database session
    session = db

    # Get the employee with the given ID
    employee = session.query(Employee).filter(
        Employee.id == employee_id).first()

    if not employee:
        raise HTTPException(
            status_code=404, detail=f"Employee with id {employee_id} not found")

    # Delete the employee
    session.delete(employee)
    session.commit()

    # Close the session
    session.close()

    return employee


@app.put("/employees/{employee_id}/{column}/{new_value}", response_model=EmployeeResponse)
def update_employee_column(
    employee_id: int, column: str, new_value: str, db: Session = Depends(get_db)
):
    # Create a new database session
    session = db

    # Get the employee with the given ID
    employee = session.query(Employee).filter(
        Employee.id == employee_id).first()

    if not employee:
        raise HTTPException(
            status_code=404, detail=f"Employee with id {employee_id} not found")

    # Update the specified column
    if hasattr(employee, column):
        setattr(employee, column, new_value)
        session.commit()

        # Refresh the object
        session.refresh(employee)

    # Close the session
    session.close()

    return employee
