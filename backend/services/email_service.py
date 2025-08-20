import os
import tempfile
import pandas as pd
import smtplib
import requests
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
from fastapi import HTTPException
import logging
from dotenv import load_dotenv

load_dotenv()

# Configure logging

logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self):

        self.supabase_url = os.getenv("SUPABASE_URL")
        self.supabase_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
        self.sender_email = os.getenv("EMAIL_USER")
        self.email_password = os.getenv("EMAIL_PASSWORD")
        
        self.headers = {
            'apikey': self.supabase_key,
            'Authorization': f'Bearer {self.supabase_key}',
            'Content-Type': 'application/json'
        }
    
    def fetch_data_from_supabase(self, table_name: str, query: str = "*", filters: dict = None):
        """Fetch data from Supabase table with optional filters"""
        try:
            url = f"{self.supabase_url}/rest/v1/{table_name}"
            
            params = {}
            if query != "*":
                params['select'] = query
            
            # Add filters if provided
            if filters:
                for key, value in filters.items():
                    params[key] = value
            
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Error fetching data: {response.status_code} - {response.text}")
                raise HTTPException(status_code=response.status_code, detail=response.text)
                
        except Exception as e:
            logger.error(f"Error fetching data from Supabase: {e}")
            raise HTTPException(status_code=500, detail=f"Error fetching data: {str(e)}")
    
    def create_csv_from_data(self, data: list, filename: str = None) -> str:
        """Create CSV file from data"""
        if not data:
            raise HTTPException(status_code=404, detail="No data available for export")
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"supabase_export_{timestamp}.csv"
        
        try:
            df = pd.DataFrame(data)
            temp_dir = tempfile.gettempdir()
            csv_path = os.path.join(temp_dir, filename)
            df.to_csv(csv_path, index=False)
            
            logger.info(f"CSV created at: {csv_path}")
            return csv_path
            
        except Exception as e:
            logger.error(f"Error creating CSV: {e}")
            raise HTTPException(status_code=500, detail=f"Error creating CSV: {str(e)}")
    
    def send_email_with_attachment(self, receiver_email: str, subject: str, body: str, attachment_path: str) -> bool:
        """Send email with CSV attachment"""
        if not all([self.sender_email, self.email_password]):
            logger.error("Email credentials not configured")
            raise HTTPException(status_code=500, detail="Email credentials not configured")
        
        try:
            message = MIMEMultipart()
            message["From"] = self.sender_email
            message["To"] = receiver_email
            message["Subject"] = subject
            
            message.attach(MIMEText(body, "plain"))
            
            with open(attachment_path, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
            
            encoders.encode_base64(part)
            
            filename = os.path.basename(attachment_path)
            part.add_header("Content-Disposition", f"attachment; filename={filename}")
            message.attach(part)
            
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(self.sender_email, self.email_password)
                server.sendmail(self.sender_email, receiver_email, message.as_string())
            
            logger.info("Email sent successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error sending email: {e}")
            raise HTTPException(status_code=500, detail=f"Error sending email: {str(e)}")
    
    def generate_and_send_history_report(self, receiver_email: str, subject: str = None, 
                                       body: str = None, warehouse_name: str = None, 
                                       warehouse_id: str = None) -> dict:
        """Generate and send history report filtered by warehouse"""
        try:
            # Default values
            if subject is None:
                subject = "Historial de acciones de bodega"
            if body is None:
                body = f"""Buenas tardes,

En este email se hace envio de un archivo resumen de las acciones 
realizadas dentro de la bodega.

Bodega: {warehouse_name or 'Todas las bodegas'}
Fecha del reporte: {datetime.now().strftime('%d/%m/%Y %H:%M')}

Espero que tenga buenas tardes.
"""
            
            # Build filters for current warehouse
            filters = {}
            if warehouse_id:
                filters['warehouse_id'] = f'eq.{warehouse_id}'
                logger.info(f"Filtering history for warehouse_id: {warehouse_id}")
            
            # Fetch data with warehouse filter
            custom_query = "id, action_type, item_name, quantity, obra, n_factura, warehouse_name, user_name, action_date, notes"
            data = self.fetch_data_from_supabase("history", custom_query, filters)
            
            if not data:
                raise HTTPException(status_code=404, detail="No history data found for this warehouse")
            
            # Create CSV
            filename = f"historial_bodega_{warehouse_name or 'general'}_{datetime.now().strftime('%Y%m%d')}.csv"
            csv_path = self.create_csv_from_data(data, filename)
            
            # Send email
            success = self.send_email_with_attachment(receiver_email, subject, body, csv_path)
            
            # Cleanup
            try:
                os.remove(csv_path)
                logger.info("Temporary file cleaned up")
            except:
                pass
            
            return {
                "success": success,
                "message": "Report sent successfully" if success else "Failed to send report",
                "records_count": len(data),
                "receiver_email": receiver_email,
                "warehouse_filtered": bool(warehouse_id)
            }
            
        except Exception as e:
            logger.error(f"Error in generate_and_send_history_report: {e}")
            raise