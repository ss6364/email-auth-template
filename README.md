
# Email Authentication App with FastAPI and Firebase

This app handles the backend logic for user authentication via Firebase, using FastAPI and MongoDB.

## Setup

### 1. Download Firebase Service Account Key

Download the **`serviceAccountKey.json`** from your Firebase project and save it in the **`app/`** directory (e.g., `.../app/serviceAccountKey.json`).

### 2. Create MongoDB Database

1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) and create a project.
2. Set up a cluster and a database, e.g., name it **`appdb`**.
3. Copy the connection string from your cluster:
   - Navigate to **Cluster > Connect > Drivers**.
   - Copy the connection string for MongoDB and save it for the next step.

### 3. Configure Database Connection in `.env`

Create a `.env` file in the root (./app/.env in this case) directory of your project and paste the following configuration:

```
MONGO_URI="mongodb+srv://USERNAME:password@cluster0.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
DB_NAME="appdb"
```

Make sure to replace USERNAME and password with your actual MongoDB credentials.

### 4. Firebase Configuration

Update the Firebase configuration in the base.html file with your Firebase credentials.

### 5. Set Up Python Virtual Environment

Run the following commands to set up your virtual environment:

```bash
cd Email-auth-template
python3 -m venv myvenv          # Create virtual environment
source myvenv/bin/activate      # Activate virtual environment (Linux/macOS)
myvenv\Scripts\activate         # For Windows
```

### 6. Install Dependencies

Install the necessary Python dependencies:

```bash
pip install -r app/requirements.txt
```

### 7. Run the Application

Start the FastAPI app with Uvicorn:

```bash
uvicorn app.main:app --reload
```

## Directory structure
```
Email-auth-template/
│
├── app/
│    ├── main.py                # FastAPI entry point
│    ├── auth.py                # Authentication utils
│    ├── firebase.py            # Firebase setup
│    │── db.py                  # MongoDB client connection
|    │── templates/             # HTML pages
|    │   ├── login.html
|    │   ├── courses.html
|    │   ├── home.html
|    │   ├── base.html          # base html file for standard UI
|    │   └── profile.html
|    │── static/                # CSS/JS if needed
|    │   └── styles.css.      
|    └── .env                   # .env for mongo db setup
|    └── serviceAccountKey.json # Firebase auth config file
│
└── myvenv                      # virtual environment
```


---

## 🔑 Authentication Flow

1. **User Signs Up**: Firebase creates the account and sends a verification email.
2. **User Verifies Email**: User clicks the link in the email to verify their account.
3. **User Logs In**: Firebase generates an ID token for the user.
4. **Backend Verification**: The token is sent to the FastAPI backend for verification via Firebase Admin SDK.
5. **User Profile**: Upon verification, the backend returns the user’s profile page. Users can also update their profile by adding their name and Twitter ID.

---

## Firebase Configuration Example

Make sure to replace the placeholder values with your Firebase credentials in the **`base.html`**:

```javascript
const firebaseConfig = {
  apiKey: "XXXXX",
  authDomain: "XXXXX.firebaseapp.com",
  projectId: "XXXXXX",
  storageBucket: "XXXXX.appspot.com",
  messagingSenderId: "XXXXXXX",
  appId: "XXXXXXXXXXXXXX"
};
```

### Notes:

- Ensure that you have the correct MongoDB and Firebase configuration before running the application.
- To modify or extend the app, focus on the files inside the **`app/`** directory.
