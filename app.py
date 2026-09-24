#!/usr/bin/env python3
"""
BlackOrange Portfolio CMS Backend
Developer: Dennis Shem O. Limo (Data Analyst • Python Developer • Data Science)
Stack: Python (Flask) + SQLite Database
Features:
  - Projects CRUD & Image Uploads
  - Technical Skills Management
  - Blog & Insights Publishing
  - Profile & Bio Settings
  - Contact Form Persistence & Visitor Analytics
  - Admin Inbox & Passcode Authentication
"""

import os
import sqlite3
import json
import time
from werkzeug.utils import secure_filename
from flask import Flask, request, jsonify, send_from_directory

# Optional environment variable support from .env
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# App Initialization - static_folder=None ensures source code & db files are never publicly exposed
app = Flask(__name__, static_folder=None)

# Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.environ.get('DATABASE_PATH', os.path.join(BASE_DIR, 'portfolio.db'))
UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', os.path.join(BASE_DIR, 'assets', 'images', 'uploads'))
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp', 'gif'}
ADMIN_PASSCODE = os.environ.get('PORTFOLIO_ADMIN_KEY', 'dennis2024')
PORT = int(os.environ.get('PORT', 5000))
SECRET_KEY = os.environ.get('SECRET_KEY', 'portfolio-shem-limo-secret-key-2024')

# Ensure directories exist (crucial when using persistent volume mounts on cloud hosts)
db_dir = os.path.dirname(os.path.abspath(DATABASE_PATH))
if db_dir:
    os.makedirs(db_dir, exist_ok=True)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['SECRET_KEY'] = SECRET_KEY
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max

# Reverse Proxy header fix (for Render, Railway, Nginx, Cloudflare visitor IP detection)
try:
    from werkzeug.middleware.proxy_fix import ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
except Exception:
    pass

# ==============================================================================
# DATABASE & SCHEMA
# ==============================================================================

def get_db():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def init_db():
    with get_db() as conn:
        cursor = conn.cursor()

        # 1. Contacts
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT,
                message TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_read INTEGER DEFAULT 0,
                ip_address TEXT
            )
        ''')

        # 2. Analytics
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS analytics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_type TEXT NOT NULL,
                target_name TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ip_address TEXT,
                user_agent TEXT
            )
        ''')

        # 3. Projects
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                subtitle TEXT,
                category TEXT,
                description TEXT NOT NULL,
                live_url TEXT,
                tech_stack TEXT,
                image_url TEXT,
                sort_order INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # 4. Skills
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS skills (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT,
                icon_svg TEXT,
                sort_order INTEGER DEFAULT 0
            )
        ''')

        # 5. Blogs
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS blogs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                category TEXT,
                read_time TEXT,
                date_str TEXT,
                image_url TEXT,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # 6. Profile
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS profile (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                title TEXT NOT NULL,
                bio_short TEXT,
                bio_long TEXT,
                email TEXT,
                phone TEXT,
                location TEXT,
                status_text TEXT
            )
        ''')

        conn.commit()

        # Seed initial data if tables are empty
        seed_initial_data(cursor, conn)

def seed_initial_data(cursor, conn):
    # Seed Projects
    cursor.execute('SELECT COUNT(*) FROM projects')
    if cursor.fetchone()[0] == 0:
        initial_projects = [
            (
                'OrbitIQ',
                'KCSE Results & University Placement Advisor with automated OCR grade extraction.',
                'Solo Project • Live on Render',
                'Engineered an end-to-end university advisory tool that streamlines student qualification evaluation: automated OCR pipeline extracting subject grades from KCSE slip photos, KUCCPS cluster point calculation engine across diverse course categories, and dynamic course-matching advisory reports.',
                'https://orbitiq-cic0.onrender.com',
                'Python, OCR Computer Vision, KUCCPS Engine, Jupyter, HTML/CSS, Render',
                'assets/images/blog-1.jpg',
                1
            ),
            (
                'Business Loan Platform',
                'Secure microfinance loan system with RBAC permissions and session security.',
                'Commercial SaaS Target • Team Project',
                'Co-developed a secure microfinance loan management platform designed for commercial SaaS deployment: architected role-based access control (RBAC), implemented strict session security protocols with automated session resets, and developed backend approval logic in Python with audit-ready action tracking.',
                'https://menace.pythonanywhere.com',
                'Python, RBAC Security, Session Management, Audit Logging, PythonAnywhere, HTML5',
                'assets/images/blog-2.jpg',
                2
            ),
            (
                'Koitalel Samoei Portal',
                'Public client portal & comprehensive administrative management workflows.',
                'Freelance Project • Live System',
                'Comprehensive institutional portal for Koitalel Samoei University: developing both the public client-facing portal and administrative management system with dynamic admin panel capabilities for secure content editing, role management, and operational workflows.',
                'https://ksu-5wmg.onrender.com',
                'Python Full-Stack, Admin CMS Engine, Dynamic RBAC, Render, Responsive Web',
                'assets/images/blog-3.jpg',
                3
            ),
            (
                'Dengue Fever Clinical Analytics',
                'Longitudinal healthcare trend tracking and visual dashboards for clinical staff.',
                'Clinic Client Project • 1-Year Study',
                'Led clinical data analysis on longitudinal healthcare datasets over a 1-year duration to assist medical decision-making: tracked dengue fever case trends, seasonal infection patterns, and patient demographic risk profiles with visual dashboards enabling medical staff to make informed, data-driven decisions.',
                '',
                'Python, Pandas, Power BI, Seaborn, Statistical Modeling, Healthcare Analytics',
                'assets/images/blog-1.jpg',
                4
            )
        ]
        cursor.executemany('''
            INSERT INTO projects (title, subtitle, category, description, live_url, tech_stack, image_url, sort_order)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', initial_projects)

    # Seed Skills
    cursor.execute('SELECT COUNT(*) FROM skills')
    if cursor.fetchone()[0] == 0:
        initial_skills = [
            ('Python', 'Programming & Data', '<svg viewBox="0 0 24 24"><path d="M11.914 0C5.82 0 6.2 2.656 6.2 2.656l.008 2.752h5.81v.825H3.924S0 5.753 0 11.889c0 6.137 3.42 5.95 3.42 5.95h2.04v-2.866s-.11-3.421 3.364-3.421h5.772s3.255.056 3.255-3.153V2.656S18.39 0 11.914 0zm-3.2 1.834a1.077 1.077 0 1 1 0 2.155 1.077 1.077 0 0 1 0-2.155zm3.372 22.166c6.094 0 5.714-2.656 5.714-2.656l-.008-2.752h-5.81v-.825h8.094s3.924.48 3.924-5.656c0-6.136-3.42-5.95-3.42-5.95h-2.04v2.866s.11 3.421-3.364 3.421H8.624s-3.255-.056-3.255 3.153v5.741s-.532 2.656 5.943 2.656zm3.2-1.834a1.077 1.077 0 1 1 0-2.155 1.077 1.077 0 0 1 0 2.155z"/></svg>', 1),
            ('SQL (MySQL)', 'Programming & Data', '<svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 4.02 2 6.5s4.48 4.5 10 4.5 10-2.02 10-4.5S17.52 2 12 2zm0 6C8.13 8 5 6.88 5 5.5S8.13 3 12 3s7 1.12 7 2.5S15.87 8 12 8zm-10 4c0 2.48 4.48 4.5 10 4.5s10-2.02 10-4.5v-2.1c-2.14 1.58-5.84 2.6-10 2.6s-7.86-1.02-10-2.6V12zm0 5.5C2 19.98 6.48 22 12 22s10-2.02 10-4.5v-2.1c-2.14 1.58-5.84 2.6-10 2.6s-7.86-1.02-10-2.6v2.1z"/></svg>', 2),
            ('Scikit-Learn', 'Machine Learning', '<svg viewBox="0 0 24 24"><path d="M12 2a2 2 0 0 1 2 2c0 .26-.05.5-.14.73l2.41 2.41c.23-.09.47-.14.73-.14a2 2 0 1 1 0 4c-.26 0-.5-.05-.73-.14l-2.41 2.41c.09.23.14.47.14.73a2 2 0 1 1-4 0c0-.26.05-.5.14-.73L7.73 11.27c-.23.09-.47.14-.73.14a2 2 0 1 1 0-4c.26 0 .5.05.73.14l2.41-2.41c-.09-.23-.14-.47-.14-.73a2 2 0 0 1 2-2zm0 13a2 2 0 0 1 2 2c0 .26-.05.5-.14.73l2.41 2.41c.23-.09.47-.14.73-.14a2 2 0 1 1 0 4c-.26 0-.5-.05-.73-.14l-2.41-2.41c.09-.23.14-.47.14-.73a2 2 0 1 1-4 0z"/></svg>', 3),
            ('TensorFlow', 'Machine Learning', '<svg viewBox="0 0 24 24"><path d="M12 0L1.605 6v12L12 24l10.395-6V6L12 0zm-1.04 19.387L3.684 15.21V8.79l7.276 4.198v6.399zm2.08 0v-6.399l7.276-4.198v6.42l-7.276 4.177zM12 11.53L4.724 7.332 12 3.134l7.276 4.198L12 11.53z"/></svg>', 4),
            ('Power BI', 'Visualization', '<svg viewBox="0 0 24 24"><path d="M4 11h3v10H4zm5-4h3v14H9zm5-5h3v19h-3zm5 8h3v11h-3z"/></svg>', 5),
            ('Tableau', 'Visualization', '<svg viewBox="0 0 24 24"><path d="M11.39 0v3.42H8.38V4.8h3.01v3.42h1.41V4.8h3.01V3.42h-3.01V0h-1.41zm6.77 5.07v3.08h-2.69v1.24h2.69v3.08h1.27V9.39h2.69V8.15h-2.69V5.07h-1.27zM4.62 6.31v3.08H1.93v1.24h2.69v3.08h1.27v-3.08h2.69V9.39H5.89V6.31H4.62zm6.77 4.3v4.61H7.07v1.86h4.32v4.61h1.92v-4.61h4.32v-1.86h-4.32v-4.61h-1.92z"/></svg>', 6),
            ('Pandas / NumPy', 'Data Analysis', '<svg viewBox="0 0 24 24"><path d="M12 2A10 10 0 1 0 22 12 10 10 0 0 0 12 2zm1 14.93V15h-2v1.93A8 8 0 0 1 4.07 13H6v-2H4.07A8 8 0 0 1 11 4.07V6h2V4.07A8 8 0 0 1 19.93 11H18v2h1.93A8 8 0 0 1 13 16.93zM12 8a4 4 0 1 0 4 4 4 4 0 0 0-4-4z"/></svg>', 7),
            ('OCR Pipelines', 'Computer Vision', '<svg viewBox="0 0 24 24"><path d="M3 4V1h2v2h2v2H3zm16-3h2v3h-4V2h2V1zm2 19v3h-2v-2h-2v-2h4zm-18 3v-3h4v2H5v1H3zm3-12h12v6H6v-6zm2 2v2h8v-2H8z"/></svg>', 8),
            ('Web Integration', 'Full-Stack', '<svg viewBox="0 0 24 24"><path d="M1.5 0h21l-1.91 21.563L11.977 24l-8.565-2.438L1.5 0zm7.031 9.75l-.232-2.718h11.455l.232-2.719H5.539l.71 8.156h8.848l-.348 3.906-2.76.744-2.76-.744-.176-2.031H6.674l.348 4.281 4.965 1.381 4.965-1.381.71-7.669H8.531z"/></svg>', 9),
            ('Cisco CCNA', 'Networking & Security', '<svg viewBox="0 0 24 24"><path d="M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4zm0 10.99h7c-.53 4.12-3.28 7.79-7 8.94V12H5V6.3l7-3.11v8.8z"/></svg>', 10),
            ('Jupyter', 'Research & Tools', '<svg viewBox="0 0 24 24"><path d="M12 0a11.95 11.95 0 0 0-7.3 2.5A5.6 5.6 0 0 1 7.4 5a5.55 5.55 0 0 1 2.3-1.6A11.96 11.96 0 0 1 12 3c4.9 0 9.1 3 10.9 7.2a5.55 5.55 0 0 1-2.3 1.6 5.6 5.6 0 0 1-2.7-2.5A11.95 11.95 0 0 0 12 0zm0 24a11.95 11.95 0 0 0 7.3-2.5 5.6 5.6 0 0 1-2.7-2.5 5.55 5.55 0 0 1-2.3 1.6A11.96 11.96 0 0 1 12 21c-4.9 0-9.1-3-10.9-7.2a5.55 5.55 0 0 1 2.3-1.6 5.6 5.6 0 0 1 2.7 2.5A11.95 11.95 0 0 0 12 24z"/></svg>', 11),
            ('Cloud / Render', 'DevOps & Deploy', '<svg viewBox="0 0 24 24"><path d="M19.35 10.04C18.67 6.59 15.64 4 12 4 9.11 4 6.6 5.64 5.35 8.04 2.34 8.36 0 10.91 0 14c0 3.31 2.69 6 6 6h13c2.76 0 5-2.24 5-5 0-2.64-2.05-4.78-4.65-4.96zM19 18H6c-2.21 0-4-1.79-4-4 0-2.05 1.53-3.76 3.56-3.97l1.07-.11.5-.95C8.08 7.14 9.94 6 12 6c2.62 0 4.88 1.86 5.39 4.43l.3 1.5 1.53.11c1.56.1 2.78 1.41 2.78 2.96 0 1.65-1.35 3-3 3z"/></svg>', 12)
        ]
        cursor.executemany('''
            INSERT INTO skills (name, category, icon_svg, sort_order)
            VALUES (?, ?, ?, ?)
        ''', initial_skills)

    # Seed Blogs
    cursor.execute('SELECT COUNT(*) FROM blogs')
    if cursor.fetchone()[0] == 0:
        initial_blogs = [
            (
                'Engineering an Automated OCR Pipeline for Exam Slip Digitization',
                'Case Study • Python & CV',
                '6 min read',
                'March 25, 2024',
                'assets/images/blog-1.jpg',
                'In building OrbitIQ, our primary bottleneck was manual data entry: students typing dozens of individual KCSE grades led to frequent input errors and skewed university cluster calculations.\n\nBy architecting an automated Optical Character Recognition (OCR) pipeline using computer vision pre-processing (deskewing, adaptive thresholding, and ROI isolation), we automated grade extraction directly from photos taken with mobile phones.\n\nKey Takeaway: Robust preprocessing (noise reduction and contrast enhancement) before feeding images into the OCR engine improved character confidence by over 38% on low-quality smartphone captures.'
            ),
            (
                'Architecting RBAC and Strict Session Security for Commercial SaaS',
                'Architecture • Python Web',
                '5 min read',
                'December 15, 2023',
                'assets/images/blog-2.jpg',
                'In financial microfinance platforms, user permission leaks represent catastrophic compliance risks. In the Business Loan Application Platform, we designed a zero-trust Role-Based Access Control (RBAC) model.\n\nEvery endpoint verifies granular permission tokens on the server rather than trusting client-side flags. Furthermore, we implemented aggressive session termination upon window close or tab defocus to protect sensitive borrower financial records.\n\nKey Takeaway: Never rely on client-side state for authorization. Security in SaaS requires server-side permission trees combined with automated audit trails for every state change.'
            ),
            (
                'Tracking Clinical Infection Trends: Longitudinal Healthcare Analytics',
                'Data Science • Healthcare',
                '7 min read',
                'October 21, 2023',
                'assets/images/blog-3.jpg',
                'During our 1-year clinical study on Dengue fever infection dynamics, we synthesized longitudinal patient metrics to forecast outbreak peaks.\n\nUsing Python (Pandas and Seaborn) alongside interactive Power BI reporting dashboards, medical personnel could monitor infection clusters in real time, shifting resource allocation proactively ahead of epidemic spikes.\n\nKey Takeaway: Data analysis in healthcare is only as valuable as its clinical interpretability. Visual dashboards designed with medical workflows in mind drove tangible improvements in early intervention response times.'
            )
        ]
        cursor.executemany('''
            INSERT INTO blogs (title, category, read_time, date_str, image_url, content)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', initial_blogs)

    # Seed Profile
    cursor.execute('SELECT COUNT(*) FROM profile')
    if cursor.fetchone()[0] == 0:
        cursor.execute('''
            INSERT INTO profile (full_name, title, bio_short, bio_long, email, phone, location, status_text)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            'Dennis Shem O. Limo',
            'Data Analyst • Python Developer • Data Science',
            'Data Analyst • Python Developer • Data Scientist based in Nairobi, Kenya (Remote-Ready).',
            'Versatile Data Analyst and Python developer with a B.Sc. in Computer Science and a Data Science & AI certification from Moringa School. Experienced building end-to-end tools independently — from OCR-driven data extraction systems to role-based web platforms — alongside freelance data analysis, research, and design work since 2019.',
            'shemdennis5@gmail.com',
            '+254 721 877 088',
            'Nairobi, Kenya (Remote-Ready)',
            'Available for full-time, contract, or remote engagements'
        ))

    conn.commit()

# Initialize DB on load
init_db()

# ==============================================================================
# AUTH HELPERS
# ==============================================================================

def verify_admin_auth():
    auth_header = request.headers.get('X-Admin-Key') or request.headers.get('Authorization')
    if auth_header and (auth_header == ADMIN_PASSCODE or auth_header == f'Bearer {ADMIN_PASSCODE}'):
        return True
    key = request.args.get('key')
    return key == ADMIN_PASSCODE

# ==============================================================================
# STATIC & WEB ROUTES
# ==============================================================================

@app.after_request
def set_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    return response

@app.route('/')
def serve_index():
    return send_from_directory(BASE_DIR, 'index.html')

@app.route('/admin')
def serve_admin():
    return send_from_directory(BASE_DIR, 'admin.html')

@app.route('/css/<path:filename>')
def serve_css(filename):
    return send_from_directory(os.path.join(BASE_DIR, 'css'), filename)

@app.route('/js/<path:filename>')
def serve_js(filename):
    return send_from_directory(os.path.join(BASE_DIR, 'js'), filename)

@app.route('/assets/<path:filename>')
def serve_assets(filename):
    return send_from_directory(os.path.join(BASE_DIR, 'assets'), filename)

@app.route('/robots.txt')
def serve_robots():
    return send_from_directory(BASE_DIR, 'robots.txt')

@app.route('/sitemap.xml')
def serve_sitemap():
    return send_from_directory(BASE_DIR, 'sitemap.xml')

@app.route('/favicon.ico')
def serve_favicon():
    return send_from_directory(os.path.join(BASE_DIR, 'assets', 'images'), 'cube-orange.png', mimetype='image/png')

@app.route('/health')
@app.route('/api/health')
def health_check():
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT 1')
            cursor.fetchone()
        return jsonify({
            'status': 'healthy',
            'database': 'connected',
            'timestamp': int(time.time())
        }), 200
    except Exception as e:
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 500

# ==============================================================================
# IMAGE UPLOAD API
# ==============================================================================

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if not verify_admin_auth():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401

    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file part in request'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        ext = file.filename.rsplit('.', 1)[1].lower()
        filename = f"upload_{int(time.time())}_{secure_filename(file.filename)}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        public_url = f"assets/images/uploads/{filename}"
        return jsonify({
            'success': True,
            'url': public_url,
            'filename': filename
        }), 201

    return jsonify({'success': False, 'error': 'Allowed file types: png, jpg, jpeg, webp, gif'}), 400

# ==============================================================================
# PUBLIC CONTENT APIS
# ==============================================================================

@app.route('/api/projects', methods=['GET'])
def get_projects():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM projects ORDER BY sort_order ASC, id DESC')
        rows = cursor.fetchall()
        projects = [dict(r) for r in rows]
        for p in projects:
            p['stack_list'] = [s.strip() for s in (p.get('tech_stack') or '').split(',') if s.strip()]
        return jsonify({'success': True, 'projects': projects})

@app.route('/api/skills', methods=['GET'])
def get_skills():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM skills ORDER BY sort_order ASC, id ASC')
        skills = [dict(r) for r in cursor.fetchall()]
        return jsonify({'success': True, 'skills': skills})

@app.route('/api/blogs', methods=['GET'])
def get_blogs():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM blogs ORDER BY id DESC')
        blogs = [dict(r) for r in cursor.fetchall()]
        return jsonify({'success': True, 'blogs': blogs})

@app.route('/api/profile', methods=['GET'])
def get_profile():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM profile LIMIT 1')
        row = cursor.fetchone()
        return jsonify({'success': True, 'profile': dict(row) if row else {}})

# ==============================================================================
# ADMIN CMS CRUD APIS
# ==============================================================================

# Projects CRUD
@app.route('/api/admin/projects', methods=['POST'])
def add_project():
    if not verify_admin_auth():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    data = request.get_json(silent=True) or {}
    title = data.get('title', '').strip()
    if not title:
        return jsonify({'success': False, 'error': 'Title is required'}), 400

    subtitle = data.get('subtitle', '').strip()
    category = data.get('category', '').strip()
    description = data.get('description', '').strip()
    live_url = data.get('live_url', '').strip()
    tech_stack = data.get('tech_stack', '').strip()
    image_url = data.get('image_url', '').strip() or 'assets/images/blog-1.jpg'

    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO projects (title, subtitle, category, description, live_url, tech_stack, image_url)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (title, subtitle, category, description, live_url, tech_stack, image_url))
        conn.commit()
        new_id = cursor.lastrowid
        return jsonify({'success': True, 'id': new_id, 'message': 'Project added successfully!'}), 201

@app.route('/api/admin/projects/<int:item_id>', methods=['PUT'])
def update_project(item_id):
    if not verify_admin_auth():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    data = request.get_json(silent=True) or {}
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE projects
            SET title = ?, subtitle = ?, category = ?, description = ?, live_url = ?, tech_stack = ?, image_url = ?
            WHERE id = ?
        ''', (
            data.get('title', '').strip(),
            data.get('subtitle', '').strip(),
            data.get('category', '').strip(),
            data.get('description', '').strip(),
            data.get('live_url', '').strip(),
            data.get('tech_stack', '').strip(),
            data.get('image_url', '').strip(),
            item_id
        ))
        conn.commit()
        return jsonify({'success': True, 'message': 'Project updated!'})

@app.route('/api/admin/projects/<int:item_id>', methods=['DELETE'])
def delete_project(item_id):
    if not verify_admin_auth():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM projects WHERE id = ?', (item_id,))
        conn.commit()
        return jsonify({'success': True, 'message': 'Project deleted!'})

# Skills CRUD
@app.route('/api/admin/skills', methods=['POST'])
def add_skill():
    if not verify_admin_auth():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    data = request.get_json(silent=True) or {}
    name = data.get('name', '').strip()
    if not name:
        return jsonify({'success': False, 'error': 'Skill name is required'}), 400
    category = data.get('category', 'Technical Skills').strip()
    icon_svg = data.get('icon_svg', '').strip() or '<svg viewBox="0 0 24 24"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>'

    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO skills (name, category, icon_svg) VALUES (?, ?, ?)', (name, category, icon_svg))
        conn.commit()
        return jsonify({'success': True, 'id': cursor.lastrowid, 'message': 'Skill added!'}), 201

@app.route('/api/admin/skills/<int:item_id>', methods=['DELETE'])
def delete_skill(item_id):
    if not verify_admin_auth():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM skills WHERE id = ?', (item_id,))
        conn.commit()
        return jsonify({'success': True, 'message': 'Skill removed!'})

# Blogs CRUD
@app.route('/api/admin/blogs', methods=['POST'])
def add_blog():
    if not verify_admin_auth():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    data = request.get_json(silent=True) or {}
    title = data.get('title', '').strip()
    if not title:
        return jsonify({'success': False, 'error': 'Blog title is required'}), 400

    category = data.get('category', 'Insights').strip()
    read_time = data.get('read_time', '5 min read').strip()
    date_str = data.get('date_str', time.strftime('%B %d, %Y')).strip()
    image_url = data.get('image_url', '').strip() or 'assets/images/blog-1.jpg'
    content = data.get('content', '').strip()

    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO blogs (title, category, read_time, date_str, image_url, content)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (title, category, read_time, date_str, image_url, content))
        conn.commit()
        return jsonify({'success': True, 'id': cursor.lastrowid, 'message': 'Blog published!'}), 201

@app.route('/api/admin/blogs/<int:item_id>', methods=['PUT'])
def update_blog(item_id):
    if not verify_admin_auth():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    data = request.get_json(silent=True) or {}
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE blogs
            SET title = ?, category = ?, read_time = ?, date_str = ?, image_url = ?, content = ?
            WHERE id = ?
        ''', (
            data.get('title', '').strip(),
            data.get('category', '').strip(),
            data.get('read_time', '').strip(),
            data.get('date_str', '').strip(),
            data.get('image_url', '').strip(),
            data.get('content', '').strip(),
            item_id
        ))
        conn.commit()
        return jsonify({'success': True, 'message': 'Blog post updated!'})

@app.route('/api/admin/blogs/<int:item_id>', methods=['DELETE'])
def delete_blog(item_id):
    if not verify_admin_auth():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM blogs WHERE id = ?', (item_id,))
        conn.commit()
        return jsonify({'success': True, 'message': 'Blog deleted!'})

# Profile Update
@app.route('/api/admin/profile', methods=['POST'])
def update_profile():
    if not verify_admin_auth():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    data = request.get_json(silent=True) or {}

    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE profile
            SET full_name = ?, title = ?, bio_short = ?, bio_long = ?, email = ?, phone = ?, location = ?, status_text = ?
            WHERE id = 1
        ''', (
            data.get('full_name', 'Dennis Shem O. Limo').strip(),
            data.get('title', '').strip(),
            data.get('bio_short', '').strip(),
            data.get('bio_long', '').strip(),
            data.get('email', '').strip(),
            data.get('phone', '').strip(),
            data.get('location', '').strip(),
            data.get('status_text', '').strip()
        ))
        conn.commit()
        return jsonify({'success': True, 'message': 'Profile settings updated!'})

# ==============================================================================
# CONTACT & ANALYTICS
# ==============================================================================

@app.route('/api/contact', methods=['POST'])
def handle_contact():
    data = request.get_json(silent=True) or request.form.to_dict()
    if not data:
        return jsonify({'success': False, 'error': 'No data provided'}), 400

    name = str(data.get('name', '')).strip()
    email = str(data.get('email', '')).strip()
    phone = str(data.get('phone', '')).strip()
    message = str(data.get('message', '')).strip()

    if not name:
        return jsonify({'success': False, 'error': 'Full name is required'}), 400
    if not email or '@' not in email or '.' not in email:
        return jsonify({'success': False, 'error': 'A valid email address is required'}), 400
    if not message or len(message) < 5:
        return jsonify({'success': False, 'error': 'Please provide a message with at least 5 characters'}), 400

    ip_address = request.headers.get('X-Forwarded-For', request.remote_addr or '127.0.0.1')
    if ',' in ip_address:
        ip_address = ip_address.split(',')[0].strip()

    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO contacts (name, email, phone, message, ip_address)
                VALUES (?, ?, ?, ?, ?)
            ''', (name, email, phone, message, ip_address))

            cursor.execute('''
                INSERT INTO analytics (event_type, target_name, ip_address, user_agent)
                VALUES (?, ?, ?, ?)
            ''', ('contact_submission', email, ip_address, request.headers.get('User-Agent', '')[:200]))
            conn.commit()

        return jsonify({
            'success': True,
            'message': f'Thank you {name}! Dennis has received your message in the database and will get back to you promptly.'
        }), 201

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/track', methods=['POST'])
def track_event():
    data = request.get_json(silent=True) or {}
    event_type = str(data.get('event_type', 'page_view')).strip()[:50]
    target_name = str(data.get('target_name', '')).strip()[:100]

    ip_address = request.headers.get('X-Forwarded-For', request.remote_addr or '127.0.0.1')
    if ',' in ip_address:
        ip_address = ip_address.split(',')[0].strip()

    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO analytics (event_type, target_name, ip_address, user_agent)
                VALUES (?, ?, ?, ?)
            ''', (event_type, target_name, ip_address, request.headers.get('User-Agent', '')[:200]))
            conn.commit()
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM contacts')
            total_inquiries = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM analytics WHERE event_type = 'page_view'")
            page_views = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM analytics WHERE event_type = 'project_click'")
            project_clicks = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM analytics WHERE event_type = 'cv_view'")
            cv_views = cursor.fetchone()[0]

            cursor.execute('SELECT COUNT(*) FROM projects')
            total_projects = cursor.fetchone()[0]

            cursor.execute('SELECT COUNT(*) FROM blogs')
            total_blogs = cursor.fetchone()[0]

            return jsonify({
                'success': True,
                'stats': {
                    'total_inquiries': total_inquiries,
                    'page_views': page_views,
                    'project_clicks': project_clicks,
                    'cv_views': cv_views,
                    'total_projects': total_projects,
                    'total_blogs': total_blogs
                }
            })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ==============================================================================
# ADMIN AUTH & MESSAGES
# ==============================================================================

@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    data = request.get_json(silent=True) or {}
    key = data.get('passcode', '').strip()
    if key == ADMIN_PASSCODE:
        return jsonify({'success': True, 'token': ADMIN_PASSCODE})
    return jsonify({'success': False, 'error': 'Invalid admin passcode'}), 401

@app.route('/api/admin/messages', methods=['GET'])
def list_messages():
    if not verify_admin_auth():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401

    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, name, email, phone, message, created_at, is_read, ip_address
                FROM contacts
                ORDER BY created_at DESC
            ''')
            rows = cursor.fetchall()
            return jsonify({'success': True, 'messages': [dict(r) for r in rows]})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/admin/messages/<int:msg_id>/read', methods=['POST'])
def mark_message_read(msg_id):
    if not verify_admin_auth():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE contacts SET is_read = 1 WHERE id = ?', (msg_id,))
        conn.commit()
        return jsonify({'success': True})

@app.route('/api/admin/messages/<int:msg_id>', methods=['DELETE'])
def delete_message(msg_id):
    if not verify_admin_auth():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM contacts WHERE id = ?', (msg_id,))
        conn.commit()
        return jsonify({'success': True})

# ==============================================================================
# ENTRYPOINT
# ==============================================================================

if __name__ == '__main__':
    print(f'Starting Dennis Shem Limo Portfolio CMS on port {PORT}...')
    print(f'Database: {DATABASE_PATH}')
    app.run(host='0.0.0.0', port=PORT, debug=False)
