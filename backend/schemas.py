from pydantic import BaseModel
from datetime import date
from typing import Optional

# Request schema for creating a leave request
class LeaveRequestCreate(BaseModel):
    user_id: int
    policy_id: int
    leave_type: str
    start_date: date
    end_date: date

# Response schema for a leave request
class LeaveRequestResponse(BaseModel):
    id: int
    user_id: int
    policy_id: int
    leave_type: str
    start_date: date
    end_date: date
    status: str
    approver_id: Optional[int] = None

    class Config:
        orm_mode = True

# Request schema for updating leave request status
class LeaveRequestUpdate(BaseModel):
    status: str

# Organization Schema
class OrganizationCreate(BaseModel):
    name: str

class OrganizationResponse(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

# Leave Policy Schema
class LeavePolicyCreate(BaseModel):
    organization_id: int
    leave_type: str
    max_days: int

class LeavePolicyResponse(BaseModel):
    id: int
    organization_id: int
    leave_type: str
    max_days: int

    class Config:
        orm_mode = True
