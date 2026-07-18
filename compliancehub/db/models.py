from sqlalchemy import Column, String, Integer, Text, ForeignKey, Date, DateTime
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Control(Base):
    __tablename__ = 'control'
    id = Column(String, primary_key=True)
    framework = Column(String)
    title = Column(String)
    description = Column(Text)
    domain = Column(String)

class AssessmentResult(Base):
    __tablename__ = 'assessment_result'
    id = Column(Integer, primary_key=True)
    control_id = Column(String, ForeignKey("control.id"))
    status = Column(String)
    rationale = Column(Text)
    evidence_note = Column(Text)
    assessed_at = Column(DateTime)
    
    control = relationship("Control")

class RiskFinding(Base):
    __tablename__ = 'risk_finding'
    id = Column(Integer, primary_key=True)
    control_id = Column(String, ForeignKey("control.id"), nullable=True)
    description = Column(Text)
    likelihood = Column(String)
    impact = Column(String)
    risk_rating = Column(String)
    remediation_owner = Column(String)
    target_date = Column(Date)
    status = Column(String)
    
    control = relationship("Control")

class Policy(Base):
    __tablename__ = 'policy'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    linked_control_ids = Column(String)
    body = Column(Text)
