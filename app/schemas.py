from pydantic import BaseModel


class EmployeeBase(BaseModel):
    name: str
    department: str


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeResponse(EmployeeBase):
    id: int

    class Config:
        orm_mode = True
