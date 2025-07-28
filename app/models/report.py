"""Report model."""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from datetime import datetime
from enum import Enum


class ReportType(str, Enum):
    """Types of reports that can be generated."""
    ACCESS_SUMMARY = "access_summary"
    PERMISSION_AUDIT = "permission_audit"
    DEVICE_STATUS = "device_status"
    SECURITY_INCIDENTS = "security_incidents"


class Report(BaseModel):
    """Represents a generated report."""
    report_id: Optional[str] = None
    report_type: ReportType
    title: str
    generated_at: datetime
    generated_by: str
    parameters: Dict[str, Any]
    data: Dict[str, Any]
    format: str = "json"  # json, csv, pdf
    
    class Config:
        from_attributes = True


class ReportRequest(BaseModel):
    """Schema for requesting a report."""
    report_type: ReportType
    title: str
    parameters: Dict[str, Any]
    format: str = "json"
