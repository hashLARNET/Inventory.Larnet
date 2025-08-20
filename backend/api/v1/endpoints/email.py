from fastapi import APIRouter, HTTPException, Depends
from typing import Optional
from pydantic import BaseModel, EmailStr
from ....services.email_service import EmailService

router = APIRouter()

class EmailRequest(BaseModel):
    receiver_email: EmailStr
    subject: Optional[str] = None
    body: Optional[str] = None
    warehouse_name: Optional[str] = None
    warehouse_id: Optional[str] = None  # Add warehouse_id field

@router.post("/send-history-report")
async def send_history_report(request: EmailRequest):
    """Send history report via email filtered by warehouse"""
    try:
        email_service = EmailService()
        result = email_service.generate_and_send_history_report(
            receiver_email=request.receiver_email,
            subject=request.subject,
            body=request.body,
            warehouse_name=request.warehouse_name,
            warehouse_id=request.warehouse_id  # Pass warehouse_id
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def email_health_check():
    """Check if email service is configured properly"""
    try:
        email_service = EmailService()
        # Just check if credentials are available
        if not all([email_service.sender_email, email_service.email_password]):
            return {"status": "error", "message": "Email credentials not configured"}
        return {"status": "ok", "message": "Email service is ready"}
    except Exception as e:
        return {"status": "error", "message": str(e)}