import os

# Database configuration
DB_CONFIG = {
    "user": os.environ.get("PGUSER"),
    "password": os.environ.get("PGPASSWORD"),
    "host": os.environ.get("PGHOST"),
    "port": os.environ.get("PGPORT"),
    "database": os.environ.get("PGDATABASE")
}

# App configuration
APP_TITLE = "ArcTecFox"
APP_SUBTITLE = "Secure Synthetic Data Platform"

# Color scheme
COLORS = {
    "primary": "#1E3D59",    # Deep blue
    "secondary": "#75B9BE",  # Light blue
    "accent": "#E8F1F2",    # Ice white
    "background": "#F0F4F8", # Light grey
    "text": "#2C3E50"       # Dark grey
}

# File upload settings
ALLOWED_EXTENSIONS = ['.csv', '.xlsx', '.json']
MAX_FILE_SIZE = 200 * 1024 * 1024  # 200MB
