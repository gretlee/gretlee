import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_sms_alert(phone, message):
    """
    Send SMS alert using Twilio API.
    
    Args:
        phone: Phone number to send SMS to (format: +1234567890)
        message: Message content
    
    Returns:
        Boolean indicating success
    """
    try:
        # Check if Twilio credentials are available
        account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
        auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
        from_phone = os.environ.get('TWILIO_PHONE_NUMBER')
        
        if not all([account_sid, auth_token, from_phone]):
            print("Warning: Twilio credentials not configured. SMS not sent.")
            print(f"Would have sent to {phone}: {message}")
            return False
        
        # Import Twilio client (only if credentials available)
        try:
            from twilio.rest import Client
            
            client = Client(account_sid, auth_token)
            
            message = client.messages.create(
                body=message,
                from_=from_phone,
                to=phone
            )
            
            print(f"SMS sent successfully. SID: {message.sid}")
            return True
            
        except ImportError:
            print("Warning: Twilio library not installed. Install with: pip install twilio")
            print(f"Would have sent to {phone}: {message}")
            return False
            
    except Exception as e:
        print(f"Error sending SMS: {str(e)}")
        return False

def send_email_alert(email, subject, message):
    """
    Send email alert using SMTP.
    
    Args:
        email: Email address to send to
        subject: Email subject
        message: Message content
    
    Returns:
        Boolean indicating success
    """
    try:
        # Get SMTP configuration from environment
        smtp_host = os.environ.get('SMTP_HOST', 'smtp.gmail.com')
        smtp_port = int(os.environ.get('SMTP_PORT', '587'))
        smtp_user = os.environ.get('SMTP_USER')
        smtp_password = os.environ.get('SMTP_PASSWORD')
        from_email = os.environ.get('FROM_EMAIL', smtp_user)
        
        if not all([smtp_user, smtp_password]):
            print("Warning: SMTP credentials not configured. Email not sent.")
            print(f"Would have sent to {email}:")
            print(f"Subject: {subject}")
            print(f"Message: {message}")
            return False
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = email
        msg['Subject'] = subject
        
        msg.attach(MIMEText(message, 'plain'))
        
        # Connect to SMTP server and send
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(msg)
        
        print(f"Email sent successfully to {email}")
        return True
        
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False

def notify_allocation(allocation, request_data, center_data, contact_info):
    """
    Send notification about resource allocation.
    
    Args:
        allocation: Allocation dictionary
        request_data: Request information
        center_data: Center information
        contact_info: Dictionary with 'phone' and/or 'email' keys
    
    Returns:
        Dictionary with notification status
    """
    message = f"""
Disaster Relief Alert - Resource Allocation

Request ID: {allocation['request_id']}
Relief Center: {allocation['center_id']}
Resources Allocated: {allocation['resources_sent']} units
Distance: {allocation['distance']} km

The relief center will dispatch resources shortly.
Stay safe!
    """.strip()
    
    results = {}
    
    if 'phone' in contact_info and contact_info['phone']:
        sms_success = send_sms_alert(contact_info['phone'], message)
        results['sms'] = 'sent' if sms_success else 'failed'
    
    if 'email' in contact_info and contact_info['email']:
        email_success = send_email_alert(
            contact_info['email'],
            f"Resource Allocation - {allocation['request_id']}",
            message
        )
        results['email'] = 'sent' if email_success else 'failed'
    
    return results
