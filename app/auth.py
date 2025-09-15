
from fastapi import Request, HTTPException
from .firebase import verify_firebase_token


def get_current_user(required: bool = True):    
    def dependency(request: Request):
        token = request.cookies.get("token") # extract token from cookie
        
        if not token:
            if required:
                raise HTTPException(status_code=401, detail="Not authenticated")
            return None

        try:
            decoded_token = verify_firebase_token(token)
            return decoded_token
        except Exception:
            if required:
                raise HTTPException(status_code=401, detail="Invalid token")
            return None
    return dependency
