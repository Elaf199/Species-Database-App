# Rai Matak Species Guide
### English–Tetum Bilingual Field Application
*Offline • Bilingual • Reforestation Support*

---

## Project Overview

The **Rai Matak Species Guide** is a dedicated mobile application developed to support the field staff, botanists, and community partners involved in the Rai Matak reforestation efforts.

Designed specifically for the challenging remote environments of Timor-Leste, the app's core value is its complete **offline functionality**. It ensures that critical species identification, ecological data, and learning resources are accessible exactly when and where they are needed, regardless of internet connectivity.

---

## Rai Matak

*Rai Matak* translates to **"Green Land"** or **"Lush Earth"** in Tetum, reflecting the program's vital mission to restore Timor-Leste's natural biodiversity and forest cover.

---

## Key Features

This application is built to be robust, intuitive, and highly functional in the field:

- **Bilingual Support (English & Tetum):**
  All content, navigation, and species descriptions are available in both English and Tetum, ensuring accessibility for all staff.

- **100% Offline Access:**
  Once the app is downloaded, all species data, photos, and identification keys are stored locally. No internet connection is required for day-to-day operation.

- **Species Identification:**
  Detailed profiles for native and important endemic tree species relevant to the Rai Matak program.

- **Rich Data Fields:**
  Each species profile includes:
  - Common and scientific names
  - Tetum names (*Naran Tetum*)
  - Detailed photographs (leaves, bark, fruit, flowers)
  - Ecological notes (habitat, elevation, soil type)
  - Propagation and management advice

- **Intuitive Search and Filtering:**
  Quickly locate species by name, characteristic, or habitat type.

---

## Admin Authentication and Session Security

The application includes a secure Admin authentication system with advanced session management features designed to protect administrative access.

### Architecture Overview

- **Single Active Session Policy:** Each Admin user can have only one active session at a time. New logins automatically revoke previous sessions.
- **Token-Based Authentication:** Admins use short-lived access tokens (40 minutes) and longer-lived refresh tokens (7 days) for secure, stateless authentication.
- **Refresh Token Rotation:** Refresh tokens are rotated on each use to prevent reuse attacks.
- **Session Revocation:** Sessions are immediately invalidated on logout, expiry, or replacement.
- **Audit Logging:** All authentication events are logged to both the audit history and analytics systems.

### Authentication Flow

1. **Login:** Admin provides credentials (password or Google OAuth).
2. **Session Creation:** System revokes any existing active sessions, generates access/refresh tokens, stores hashed refresh token.
3. **Token Usage:** Access tokens are sent in Authorization header for API requests.
4. **Refresh:** When access token expires, use refresh token to obtain new tokens.
5. **Logout:** Revokes current session and refresh token.

### Session Metadata

Each Admin session tracks:
- Admin user ID
- Session ID
- Access token issue/expiry timestamps
- Refresh token issue/expiry timestamps
- Last activity timestamp
- IP address
- User agent
- Session status (active/revoked)
- Revocation reason (logout/expired/new_login/refresh_expired)
- Event type (login/logout/refresh/expiry/failed_login/session_replacement/refresh_expired)

### Authentication Events

Events logged include:
- **admin_login:** Successful login
- **admin_logout:** User logout
- **admin_refresh:** Token refresh
- **admin_failed_login:** Failed login attempt
- **expiry:** Session expired
- **session_replacement:** Previous session revoked due to new login
- **refresh_expired:** Refresh token expired

### API Endpoints

- `POST /api/auth/admin-login` - Password login
- `POST /api/auth/google-admin` - Google OAuth login
- `POST /api/auth/admin-logout` - Logout
- `POST /api/auth/admin-refresh` - Refresh tokens
- `GET /api/admin/session-audit` - View session audit history

### Security Controls

- Refresh tokens stored as bcrypt hashes (not plaintext)
- Tokens never logged in full
- IP and User-Agent tracking for security monitoring
- Automatic session expiry and revocation
- Failed login logging for anomaly detection

### Configuration

- Access token expiry: 40 minutes
- Refresh token expiry: 7 days
- Hashing: bcrypt with salt
- Database: PostgreSQL via Supabase

### Test Procedure

1. Login as Admin user
2. Verify single session enforcement (login from another device revokes first)
3. Test token refresh before expiry
4. Attempt access with expired/revoked tokens
5. Check audit logs for all events
6. Verify analytics integration

---

## Security & CI/CD

This project implements automated security scanning to ensure code quality and dependency safety:

- **Security Scanning:** Uses SNYK for vulnerability detection in Python dependencies, along with Safety checks and npm audit for Node.js packages.
- **Secrets Scanning:** TruffleHog is used to detect potential secrets in the codebase.
- **CI Pipeline:** Security scans run automatically on pushes and pull requests to the `master` and `DevSecOps` branches, or can be triggered manually.
- **Vulnerability Reporting:** See [SECURITY.md](SECURITY.md) for information on reporting security vulnerabilities.

---

## Setup & Running

The project has three components that need to be set up and run separately. Follow the steps below for each.

---

### 1. Backend

The backend is a Python Flask server. Follow these steps to set it up from scratch.

**Step 1: Navigate to the backend folder**
```bash
cd /[userfolder]/backend

# Example:
# cd "/Users/antonymathiyalan/Desktop/Species-Database-App/backend"
```

**Step 2: Remove any old virtual environments**
```bash
rm -rf venv .venv
```

**Step 3: Create a new virtual environment**
```bash
python3 -m venv venv
```

**Step 4: Activate the virtual environment**
```bash
source venv/bin/activate
```

**Step 5: Confirm you are using the correct Python (Important)**
```bash
which python
python -c "import sys; print(sys.executable)"
```

**Step 6: Upgrade pip and install dependencies**
```bash
python -m pip install --upgrade pip
python -m pip install -r ../requirements.txt
python -m pip install flask-cors
```

**Step 7: Navigate into the backend sub-folder (where app.py lives)**
```bash
cd backend
```

**Step 8: Run the backend server**
```bash
python app.py
```

---

### 2. Frontend (Admin)

The Admin frontend is a React dashboard. Run the following commands from the project root or the `ReactDash` folder.

```bash
cd ReactDash
npm install
npm run dev
```

---

### 3. Frontend (User)

The User frontend is an HTML-based application that can be run in two ways:

#### Option A — Quick Preview with VS Code Live Server

1. Install the **Go Live** extension in Visual Studio Code.
2. Open the project folder in VS Code.
3. Right-click the main HTML file and select **Open with Live Server**.

---

#### Option B — Run on Android via Capacitor & Android Studio

**Make Sure you have latest Android Studio**
To build and run the app as an APK on a real device or emulator, follow these steps:

**Step 1: Install dependencies**
```bash
npm install
```

**Step 2: Install Capacitor dependencies** *(if not already installed)*
```bash
npm install @capacitor/core @capacitor/android
```

**Step 3: Initialize Capacitor** *(first time only)*
```bash
npx cap init
```
> Enter your **App Name** and **App ID** (e.g. `com.raimatak.app`) when prompted.

**Step 4: Build the web assets**
```bash
npm run build
```

**Step 5: Sync web assets to the Android project**
```bash
npx cap sync android
```

**Step 6: Open the project in Android Studio**
```bash
npx cap open android
```

**Step 7: Run the app from Android Studio**
1. Wait for Gradle to finish syncing.
2. Select a connected device or an emulator from the device dropdown.
3. Click the green **Run** button (or press `Shift + F10`) to build and deploy the APK.

> **Tip:** Every time you update your web code, repeat **Steps 3 and 5** (build + sync) before running again in Android Studio.

---

*Rai Matak Species Guide • Timor-Leste Reforestation Program*