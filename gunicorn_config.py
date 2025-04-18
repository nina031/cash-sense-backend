import os

# Bind to the port specified by the environment variable PORT
port = os.environ.get('PORT', 5000)
bind = f"0.0.0.0:{port}"

# Number of worker processes
workers = 4

# Worker timeout in seconds
timeout = 120

# Log level
loglevel = 'info'

# Access log format
accesslog = '-'  # Log to stdout
errorlog = '-'   # Log to stderr

# Enable threading
threads = 2

# Preload the application
preload_app = True