from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, Base, get_db
import models
import schemas

# Initialize the FastAPI app
app = FastAPI()

# Create database tables if they do not exist
Base.metadata.create_all(bind=engine)

# API Endpoint: Health Check
@app.get("/")
def root():
    return {"message": "Leave Management System API is running!"}

# API Endpoint: Create a Leave Request
@app.post("/leave-requests/", response_model=schemas.LeaveRequestResponse)
def request_leave(request: schemas.LeaveRequestCreate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == request.user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    policy = db.query(models.LeavePolicy).filter(models.LeavePolicy.id == request.policy_id).first()
    
    if not policy:
        raise HTTPException(status_code=404, detail="Leave policy not found")

    if request.leave_type == "vacation":
        if user.days_remaining < (request.end_date - request.start_date).days:
            raise HTTPException(status_code=400, detail="Not enough leave balance")

        user.days_remaining -= (request.end_date - request.start_date).days

    new_request = models.LeaveRequest(
        user_id=request.user_id,
        policy_id=request.policy_id,
        leave_type=request.leave_type,
        start_date=request.start_date,
        end_date=request.end_date,
        status="pending"
    )

    db.add(new_request)
    db.commit()
    db.refresh(new_request)

    return new_request

# API Endpoint: Approve or Reject a Leave Request
@app.put("/leave-requests/{request_id}/", response_model=schemas.LeaveRequestResponse)
def update_leave_request(
    request_id: int,
    status: schemas.LeaveRequestUpdate,
    db: Session = Depends(get_db)
):
    leave_request = db.query(models.LeaveRequest).filter(models.LeaveRequest.id == request_id).first()
    
    if not leave_request:
        raise HTTPException(status_code=404, detail="Leave request not found")

    if status.status not in ["approved", "rejected"]:
        raise HTTPException(status_code=400, detail="Invalid status")

    leave_request.status = status.status
    db.commit()
    db.refresh(leave_request)

    return leave_request

# API Endpoint: List All Leave Requests
@app.get("/leave-requests/", response_model=list[schemas.LeaveRequestResponse])
def get_leave_requests(db: Session = Depends(get_db)):
    leave_requests = db.query(models.LeaveRequest).all()
    return leave_requests

# API Endpoint: Get a Leave Request by ID
@app.get("/leave-requests/{request_id}/", response_model=schemas.LeaveRequestResponse)
def get_leave_request(request_id: int, db: Session = Depends(get_db)):
    leave_request = db.query(models.LeaveRequest).filter(models.LeaveRequest.id == request_id).first()

    if not leave_request:
        raise HTTPException(status_code=404, detail="Leave request not found")

    return leave_request

# API Endpoint: Create Leave Policy
@app.post("/leave-policies/", response_model=schemas.LeavePolicyResponse)
def create_leave_policy(policy: schemas.LeavePolicyCreate, db: Session = Depends(get_db)):
    new_policy = models.LeavePolicy(
        organization_id=policy.organization_id,
        leave_type=policy.leave_type,
        max_days=policy.max_days
    )

    db.add(new_policy)
    db.commit()
    db.refresh(new_policy)

    return new_policy

# API Endpoint: List All Leave Policies
@app.get("/leave-policies/", response_model=list[schemas.LeavePolicyResponse])
def get_leave_policies(db: Session = Depends(get_db)):
    leave_policies = db.query(models.LeavePolicy).all()
    return leave_policies

# API Endpoint: Create an Organization
@app.post("/organizations/", response_model=schemas.OrganizationResponse)
def create_organization(org: schemas.OrganizationCreate, db: Session = Depends(get_db)):
    new_organization = models.Organization(name=org.name)
    
    db.add(new_organization)
    db.commit()
    db.refresh(new_organization)

    return new_organization

# API Endpoint: Get All Organizations
@app.get("/organizations/", response_model=list[schemas.OrganizationResponse])
def get_organizations(db: Session = Depends(get_db)):
    organizations = db.query(models.Organization).all()
    return organizations
