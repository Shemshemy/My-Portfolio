import os

# Server socket
bind = f"0.0.0.0:{os.environ.get('PORT', '5000')}"
backlog = 2048

# Worker processes
workers = int(os.environ.get('WEB_CONCURRENCY', '2'))
threads = int(os.environ.get('GUNICORN_THREADS', '4'))
worker_class = 'gthread'
worker_connections = 1000
timeout = 120
keepalive = 5

# Logging
accesslog = '-'
errorlog = '-'
loglevel = os.environ.get('LOG_LEVEL', 'info')
capture_output = True

# Process naming
proc_name = 'dennis_portfolio_cms'
