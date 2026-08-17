from fastapi import APIRouter
from fastapi.responses import RedirectResponse
import httpx
import os

router = APIRouter()

# قاموس لحفظ التوكنز مؤقتاً (للتجربة)
USER_TOKENS = {}

# يجب إضافة هذه المتغيرات في ملف .env الخاص بك
CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = "http://localhost:8000/api/oauth/google/callback"

@router.get("/api/oauth/google/login")
async def google_login():
    url = (
        f"https://accounts.google.com/o/oauth2/v2/auth?"
        f"client_id={CLIENT_ID}&"
        f"redirect_uri={REDIRECT_URI}&"
        f"response_type=code&"
        f"scope=https://www.googleapis.com/auth/gmail.send&"
        f"access_type=offline&"
        f"prompt=consent"
    )
    return RedirectResponse(url)

@router.get("/api/oauth/google/callback")
async def google_callback(code: str):
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            "https://oauth2.googleapis.com/token",
            data={
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": REDIRECT_URI
            }
        )
        data = resp.json()
        if "access_token" in data:
            # حفظ التوكن للمستخدم الوهمي "test_user"
            USER_TOKENS["test_user"] = data["access_token"]
            return {"message": "Gmail connected successfully! You can close this window."}
        return {"error": "Failed to connect", "details": data}