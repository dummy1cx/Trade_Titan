from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import engine, SessionLocal, Base
import models, scemas, crud
from typing import List

Base.metadata.create_all(bind = engine)

app = FastAPI()

### Dependecnins with the datbases

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


## end points
# 1. create an employee
@app.post('/employees', response_model = scemas.EmployeeOut)
def create_employee(employee: scemas.EmployeeCreate, db: Session = Depends(get_db)):
    return crud.create_employee(db, employee)


## get all the employees records

@app.get('/employees', response_model = List[scemas.EmployeeOut])
def get_employees(db: Session = Depends(get_db)):
    return crud.get_employees(db)

##geta particular employee from the data base

@app.get('/employees/{emp_id}', response_model = scemas.EmployeeOut)
def get_employee(emp_id:int, db: Session = Depends(get_db)):
    employee = crud.get_employee(db, emp_id)
    if employee is None:
        raise HTTPException(status_code = 404, detail = "employee not found")
    return employee

## Update an employee

@app.put('/employees/{emp_id}', response_model = scemas.EmployeeOut)
def update_employee(emp_id: int, employee: scemas.EmployeeUpdate,db: Session = Depends(get_db)):
    db_employee = crud.update_employee(db, emp_id, employee)
    if db_employee is None:
        raise HTTPException(status_code = 404, detail = 'employee not found')
    return db_employee

# delete
@app.delete('/employees/{emp_id}', response_model = dict)
def delete_employee(emp_id : int, db : Session = Depends(get_db)):
    employee = crud.delete_employee(db, emp_id)
    if employee is None:
        raise HTTPException(status_code = 404, detail = 'EMplloyee not found')
    return {'detail': 'Employee Deleted'}
