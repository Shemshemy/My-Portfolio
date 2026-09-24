# Dennis Shem Limo — Professional Portfolio & CMS

A high-performance, dark-themed personal portfolio and content management system for **Dennis Shem O. Limo** (Data Analyst • Python Developer • Data Scientist).

Built with a lightweight **Python (Flask)** backend, **SQLite** database, and pure **Vanilla HTML/CSS/JavaScript** for ultra-fast load times and interactive 3D aesthetics.

---

## 🌟 Features

- **Dynamic CMS Backed by SQLite**: Manage projects, skills, blog articles, and profile bio in real-time.
- **Admin Control Center**: Built-in protected dashboard (`/admin`) for publishing content, reviewing contact inquiries, and reading visitor telemetry.
- **Visitor Analytics Engine**: Track page views, device metrics, and interaction events without heavy third-party tracking scripts.
- **File & Image Uploads**: Secure multipart file uploader for project thumbnails and profile media.
- **Production Hardened**:
  - Secure static asset routing (prevents backend source code and `.db` exposure).
  - Reverse proxy support via `ProxyFix` (logs real visitor IPs on Render, Railway, Cloudflare, Nginx).
  - Configurable persistent database paths for cloud volumes.
  - Gunicorn multi-threaded WSGI configuration.
  - SEO-ready (`robots.txt`, `sitemap.xml`, Open Graph & Twitter meta tags).
  - Health check probes (`/health`, `/api/health`).

---

## 🚀 Quick Local Start

### 1. Clone & Set Up Virtual Environment

```bash
# Navigate to project directory
cd "My Portfolio"

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment (Optional)

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

### 3. Run Locally

**Development Server:**
```bash
python app.py
```
Or with **Gunicorn** (production mode):
```bash
gunicorn --config gunicorn.conf.py app:app
```

- Open portfolio: [http://localhost:5000](http://localhost:5000)
- Admin portal: [http://localhost:5000/admin](http://localhost:5000/admin) (Default key: `dennis2024`)
- Health check: [http://localhost:5000/health](http://localhost:5000/health)

---

## ☁️ Deployment Options

### Option 1: Render (Recommended)

Render is pre-configured with [`render.yaml`](render.yaml) and [`Procfile`](Procfile).

#### Method A: Render Blueprint (1-Click)
1. Push your repository to GitHub.
2. Log into [Render Dashboard](https://dashboard.render.com).
3. Click **New +** -> **Blueprint**.
4. Connect your repository. Render will automatically read `render.yaml` and configure everything.

#### Method B: Manual Web Service
1. In Render, select **New +** -> **Web Service**.
2. Connect your GitHub repository.
3. Configure the settings:
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn --config gunicorn.conf.py app:app`
   - **Health Check Path**: `/health`
4. In **Environment Variables**, add:
   - `PORTFOLIO_ADMIN_KEY`: Set your secret admin passcode.
   - `SECRET_KEY`: Set a long random string.
   - `PYTHON_VERSION`: `3.11.9`
5. Click **Create Web Service**.

> **Note on Persistent Storage**: On Render's Free tier, storage is ephemeral. Initial data is safely pre-seeded on startup. If you add a Render Persistent Disk (available on paid plans), set `DATABASE_PATH=/var/data/portfolio.db` and `UPLOAD_FOLDER=/var/data/uploads` to retain uploads permanently across rebuilds.

---

### Option 2: Railway

1. Install Railway CLI or connect via [railway.app](https://railway.app).
2. Click **New Project** -> **Deploy from GitHub repo**.
3. Railway automatically detects `Procfile` and `requirements.txt`.
4. Set environment variables:
   - `PORTFOLIO_ADMIN_KEY`: `your_secure_password`
   - `SECRET_KEY`: `your_random_secret`
5. Railway provides a live HTTPS domain instantly.

---

### Option 3: PythonAnywhere

1. Log into your [PythonAnywhere](https://www.pythonanywhere.com/) dashboard.
2. Open a Bash console and clone your repo or upload files.
3. Set up a virtualenv:
   ```bash
   mkvirtualenv --python=/usr/bin/python3.10 myportfolio
   pip install -r requirements.txt
   ```
4. Go to the **Web** tab:
   - Create a **Manual configuration** app with Python 3.10.
   - Set virtualenv path to `/home/<your-username>/.virtualenvs/myportfolio`.
5. Edit the **WSGI configuration file**:
   ```python
   import sys
   import os

   path = '/home/<your-username>/myportfolio'
   if path not in sys.path:
       sys.path.append(path)

   os.environ['PORTFOLIO_ADMIN_KEY'] = 'your_admin_key'

   from app import app as application
   ```
6. Click **Reload**.

---

### Option 4: Docker & Docker Compose (VPS / Fly.io / Cloud)

Run with Docker Compose:

```bash
docker compose up -d --build
```

Persistent SQLite data and uploaded images are automatically stored in Docker volumes `portfolio_data` and `portfolio_uploads`.

---

## ⚙️ Environment Variables Reference

| Variable | Default | Purpose |
| :--- | :--- | :--- |
| `PORT` | `5000` | Port for the HTTP server to listen on. |
| `PORTFOLIO_ADMIN_KEY` | `dennis2024` | Secret passcode to log in to `/admin` and authenticate CMS APIs. |
| `SECRET_KEY` | *(Built-in default)* | Secret key for Flask cookies and sessions. |
| `DATABASE_PATH` | `portfolio.db` | Absolute or relative path to the SQLite database file. |
| `UPLOAD_FOLDER` | `assets/images/uploads` | Path where user-uploaded media files are saved. |
| `WEB_CONCURRENCY` | `2` | Number of Gunicorn worker processes. |
| `GUNICORN_THREADS` | `4` | Threads per Gunicorn worker process. |

---

## 🛡️ Security Best Practices Implemented

1. **Restricted Asset Delivery**: Source files (`app.py`, `portfolio.db`, `.env`, `Procfile`) cannot be accessed over HTTP.
2. **Reverse Proxy Compatibility**: Client IP spoofing protection with Werkzeug `ProxyFix`.
3. **Security Headers**: Automatic injection of `X-Content-Type-Options: nosniff`, `X-Frame-Options: SAMEORIGIN`, and `X-XSS-Protection`.
4. **Admin Protection**: All mutation endpoints (`POST`, `PUT`, `DELETE`) require the `X-Admin-Key` header matching `PORTFOLIO_ADMIN_KEY`.
