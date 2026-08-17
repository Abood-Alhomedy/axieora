import base64
from email.message import EmailMessage
import httpx
from .base import ToolConfig, ToolRegistry

gmail_send_config = ToolConfig(
    id="gmail_send",
    name="Gmail Send",
    description="Send emails using Gmail",
    parameters={
        "type": "object",
        "properties": {
            "to": {"type": "string", "description": "Recipient email address"},
            "subject": {"type": "string", "description": "Email subject"},
            "body": {"type": "string", "description": "Email body content"}
        },
        "required": ["to", "body"]
    }
)

async def execute_gmail_send(params: dict, context: dict) -> dict:
    access_token = context.get("access_token")
    if not access_token:
        return {"success": False, "error": "No access token. User must connect Gmail."}
    
    # بناء رسالة الإيميل
    message = EmailMessage()
    message.set_content(params["body"])
    message["To"] = params["to"]
    message["Subject"] = params.get("subject", "")
    
    # تحويل الرسالة لصيغة يقبلها Gmail
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    
    # إرسال الطلب لـ Gmail API
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            "https://gmail.googleapis.com/gmail/v1/users/me/messages/send",
            headers={"Authorization": f"Bearer {access_token}"},
            json={"raw": encoded_message}
        )
        if resp.status_code == 200:
            return {"success": True, "output": {"content": "Email sent successfully"}}
        return {"success": False, "error": resp.text}

# تسجيل الأداة
ToolRegistry.register(gmail_send_config, execute_gmail_send)