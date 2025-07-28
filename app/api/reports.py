"""Reports API endpoints."""

from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime

from ..models import Report, ReportRequest, ReportType, Session
from ..services import Database
from .auth import get_current_session

router = APIRouter(prefix="/reports", tags=["reports"])
database = Database()


@router.post("/", response_model=Report)
async def generate_report(
    report_request: ReportRequest,
    current_session: Session = Depends(get_current_session)
):
    """Generate a new report."""
    try:
        import uuid
        
        # Generate report data based on type
        report_data = await _generate_report_data(report_request.report_type, report_request.parameters)
        
        report = Report(
            report_id=str(uuid.uuid4()),
            report_type=report_request.report_type,
            title=report_request.title,
            generated_at=datetime.now(),
            generated_by=current_session.user_id,
            parameters=report_request.parameters,
            data=report_data,
            format=report_request.format
        )
        
        return report
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to generate report: {str(e)}"
        )


@router.get("/types")
async def get_report_types(
    current_session: Session = Depends(get_current_session)
):
    """Get available report types."""
    return {
        "report_types": [
            {
                "type": ReportType.ACCESS_SUMMARY,
                "name": "Access Summary",
                "description": "Summary of access logs over a time period"
            },
            {
                "type": ReportType.PERMISSION_AUDIT,
                "name": "Permission Audit",
                "description": "Audit of user permissions and changes"
            },
            {
                "type": ReportType.DEVICE_STATUS,
                "name": "Device Status",
                "description": "Status report of all devices and gateways"
            },
            {
                "type": ReportType.SECURITY_INCIDENTS,
                "name": "Security Incidents",
                "description": "Report of security incidents and failed access attempts"
            }
        ]
    }


async def _generate_report_data(report_type: ReportType, parameters: Dict[str, Any]) -> Dict[str, Any]:
    """Generate report data based on type and parameters."""
    
    if report_type == ReportType.ACCESS_SUMMARY:
        return await _generate_access_summary_report(parameters)
    elif report_type == ReportType.PERMISSION_AUDIT:
        return await _generate_permission_audit_report(parameters)
    elif report_type == ReportType.DEVICE_STATUS:
        return await _generate_device_status_report(parameters)
    elif report_type == ReportType.SECURITY_INCIDENTS:
        return await _generate_security_incidents_report(parameters)
    else:
        raise ValueError(f"Unsupported report type: {report_type}")


async def _generate_access_summary_report(parameters: Dict[str, Any]) -> Dict[str, Any]:
    """Generate access summary report."""
    start_date = parameters.get("start_date")
    end_date = parameters.get("end_date")
    
    room_stats = []
    # Fetch room statistics from the DB
    
    return {
        "summary": {
            "period": {"start": start_date, "end": end_date},
            "total_rooms": len(room_stats),
            "room_statistics": room_stats
        }
    }


async def _generate_permission_audit_report(parameters: Dict[str, Any]) -> Dict[str, Any]:
    """Generate permission audit report."""
    user_id = parameters.get("user_id")
    
    # Build example SQL query
    query = """
        SELECT 
            p.user_id,
            u.username,
            u.full_name,
            p.room_id,
            p.is_active,
            p.created_at
        FROM permissions p
        JOIN users u ON p.user_id = u.user_id
    """
    
    query_params = []
    if user_id:
        query += " WHERE p.user_id = ?"
        query_params.append(user_id)
    
    query += " ORDER BY p.user_id, p.room_id"
    
    permissions = []
   
    # Send query to database to fetch permission report
    
    return {
        "audit": {
            "permissions": permissions,
            "total_permissions": len(permissions),
            "active_permissions": len([p for p in permissions if p["is_active"]])
        }
    }


async def _generate_device_status_report(parameters: Dict[str, Any]) -> Dict[str, Any]:
    """Generate device status report."""
    # This would typically query gateway and device status
    # For now, return mock data
    return {
        "devices": {
            "total_gateways": 0,
            "online_gateways": 0,
            "offline_gateways": 0,
            "total_devices": 0,
            "active_devices": 0,
            "low_battery_devices": 0
        }
    }


async def _generate_security_incidents_report(parameters: Dict[str, Any]) -> Dict[str, Any]:
    """Generate security incidents report."""
    start_date = parameters.get("start_date")
    end_date = parameters.get("end_date")
    
    # Build SQL query and fetch access log records where access was not granted
    
    incidents = []
    
    return {
        "security_incidents": {
            "period": {"start": start_date, "end": end_date},
            "total_incidents": len(incidents),
            "incidents": incidents
        }
    }
