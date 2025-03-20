from sqlalchemy import Column, Integer, String, ForeignKey, Date, TIMESTAMP, Enum
from sqlalchemy.orm import relationship
from database import Base
import datetime

# Organizations Table
class Organization(Base):
    __tablename__ = "organizations"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)
    
    users = relationship("User", back_populates="organization")
    leave_policies = relationship("LeavePolicy", back_populates="organization")

# Users Table
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id", ondelete="CASCADE"))
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    role = Column(Enum("employee", "admin", name="user_roles"), nullable=False)
    days_remaining = Column(Integer, default=23)  # New field for leave balance
    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)
    
    organization = relationship("Organization", back_populates="users")
    leave_requests = relationship("LeaveRequest", back_populates="user", foreign_keys="LeaveRequest.user_id")
    approved_leaves = relationship("LeaveRequest", back_populates="approver", foreign_keys="LeaveRequest.approver_id")

# Leave Policies Table
class LeavePolicy(Base):
    __tablename__ = "leave_policies"
    
    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id", ondelete="CASCADE"))
    leave_type = Column(String(100), nullable=False)
    max_days = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)
    
    organization = relationship("Organization", back_populates="leave_policies")
    leave_requests = relationship("LeaveRequest", back_populates="policy")

# Leave Requests Table
class LeaveRequest(Base):
    __tablename__ = "leave_requests"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    policy_id = Column(Integer, ForeignKey("leave_policies.id", ondelete="CASCADE"))
    leave_type = Column(String(100), nullable=False)  # New field for leave type
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    status = Column(Enum("pending", "approved", "rejected", name="leave_status"), default="pending")
    approver_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)
    
    user = relationship("User", back_populates="leave_requests", foreign_keys=[user_id])
    policy = relationship("LeavePolicy", back_populates="leave_requests")
    approver = relationship("User", back_populates="approved_leaves", foreign_keys=[approver_id])
