import firebase_admin
from firebase_admin import credentials, auth


import os
print(os.path.abspath("app/serviceAccountKey.json"))

# Initialize Firebase Admin SDK (service account key file must be in your project)
cred = credentials.Certificate("./app/serviceAccountKey.json")  # download from Firebase Console
firebase_admin.initialize_app(cred)

# helper to verify id token
def verify_firebase_token(id_token: str):
    """
    Verify Firebase ID token sent from frontend.
    Returns decoded token (dict) if valid, otherwise raises error.
    """
    try:
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token
    except Exception as e:
        raise ValueError(f"Invalid token: {e}")
