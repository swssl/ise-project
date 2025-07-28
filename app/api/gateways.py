"""Gateway management API endpoints."""

from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks

from ..models import Gateway, DeviceStatus, Session
from ..services import GatewayCommService
from .auth import get_current_session

router = APIRouter(prefix="/gateways", tags=["gateways"])
gateway_service = GatewayCommService()


@router.post("/", response_model=Gateway)
async def register_gateway(
    gateway_data: Dict[str, Any],
    current_session: Session = Depends(get_current_session)
):
    """Register a new gateway."""
    try:
        from datetime import datetime
        
        gateway = Gateway(
            gateway_id=gateway_data["gateway_id"],
            name=gateway_data["name"],
            location=gateway_data["location"],
            is_online=True,
            last_heartbeat=datetime.now(),
            ip_address=gateway_data.get("ip_address")
        )
        
        gateway_service.register_gateway(gateway)
        return gateway
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to register gateway: {str(e)}"
        )


@router.get("/", response_model=List[Gateway])
async def get_gateways(
    current_session: Session = Depends(get_current_session)
):
    """Get all registered gateways."""
    return list(gateway_service.gateway_connections.values())


@router.get("/{gateway_id}", response_model=Gateway)
async def get_gateway(
    gateway_id: str,
    current_session: Session = Depends(get_current_session)
):
    """Get a specific gateway."""
    gateway = gateway_service.gateway_connections.get(gateway_id)
    if not gateway:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Gateway not found"
        )
    return gateway


@router.delete("/{gateway_id}")
async def unregister_gateway(
    gateway_id: str,
    current_session: Session = Depends(get_current_session)
):
    """Unregister a gateway."""
    if gateway_id not in gateway_service.gateway_connections:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Gateway not found"
        )
    
    gateway_service.unregister_gateway(gateway_id)
    return {"message": f"Gateway {gateway_id} unregistered successfully"}


@router.post("/{gateway_id}/sync")
async def sync_gateway(
    gateway_id: str,
    background_tasks: BackgroundTasks,
    current_session: Session = Depends(get_current_session)
):
    """Synchronize with a specific gateway."""
    if gateway_id not in gateway_service.gateway_connections:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Gateway not found"
        )
    
    # Direct call since it's no longer async
    success = gateway_service.sync_with_gateway(gateway_id)
    if success:
        return {"message": f"Sync initiated for gateway {gateway_id}"}
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to sync with gateway"
        )


@router.post("/{gateway_id}/card-update")
async def send_card_update(
    gateway_id: str,
    card_data: Dict[str, str],
    background_tasks: BackgroundTasks,
    current_session: Session = Depends(get_current_session)
):
    """Send card update to a specific gateway."""
    if gateway_id not in gateway_service.gateway_connections:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Gateway not found"
        )
    
    try:
        # Convert hex string back to bytes
        card_bytes = bytes.fromhex(card_data["card_data"])
        # Direct call since it's no longer async
        success = gateway_service.send_card_update(gateway_id, card_bytes)
        if success:
            return {"message": f"Card update sent to gateway {gateway_id}"}
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to send card update"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to send card update: {str(e)}"
        )


@router.post("/{gateway_id}/access-log")
async def receive_access_log(
    gateway_id: str,
    access_log_data: Dict[str, Any],
    background_tasks: BackgroundTasks,
    current_session: Session = Depends(get_current_session)
):
    """Receive access log from gateway."""
    if gateway_id not in gateway_service.gateway_connections:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Gateway not found"
        )
    
    try:
        # Direct call since it's no longer async
        access_log = gateway_service.receive_access_log(access_log_data)
        return {"message": "Access log received successfully", "log": access_log}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to process access log: {str(e)}"
        )


@router.post("/{gateway_id}/device-status")
async def receive_device_status(
    gateway_id: str,
    status_data: Dict[str, Any],
    background_tasks: BackgroundTasks,
    current_session: Session = Depends(get_current_session)
):
    """Receive device status from gateway."""
    if gateway_id not in gateway_service.gateway_connections:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Gateway not found"
        )
    
    try:
        # Direct call since it's no longer async
        device_status = gateway_service.receive_device_status(status_data)
        return {"message": "Device status received successfully", "status": device_status}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to process device status: {str(e)}"
        )
