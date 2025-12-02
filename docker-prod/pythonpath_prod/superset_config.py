#
# Superset Production Configuration
#

import os
from celery.schedules import crontab

# ============================================================
# GENERAL CONFIGURATION
# ============================================================
ROW_LIMIT = 5000
SECRET_KEY = os.environ.get("SUPERSET_SECRET_KEY", "CHANGE_ME_TO_A_COMPLEX_RANDOM_SECRET")

# ============================================================
# DATABASE CONFIGURATION
# ============================================================
SQLALCHEMY_DATABASE_URI = (
    f"{os.environ.get('DATABASE_DIALECT', 'postgresql')}://"
    f"{os.environ.get('DATABASE_USER', 'superset')}:"
    f"{os.environ.get('DATABASE_PASSWORD', 'superset')}@"
    f"{os.environ.get('DATABASE_HOST', 'db')}:"
    f"{os.environ.get('DATABASE_PORT', '5432')}/"
    f"{os.environ.get('DATABASE_DB', 'superset')}"
)

# ============================================================
# REDIS / CACHE CONFIGURATION
# ============================================================
REDIS_HOST = os.environ.get("REDIS_HOST", "redis")
REDIS_PORT = os.environ.get("REDIS_PORT", 6379)
REDIS_CELERY_DB = os.environ.get("REDIS_CELERY_DB", 0)
REDIS_RESULTS_DB = os.environ.get("REDIS_RESULTS_DB", 1)

CACHE_CONFIG = {
    "CACHE_TYPE": "RedisCache",
    "CACHE_DEFAULT_TIMEOUT": 300,
    "CACHE_KEY_PREFIX": "superset_",
    "CACHE_REDIS_HOST": REDIS_HOST,
    "CACHE_REDIS_PORT": REDIS_PORT,
    "CACHE_REDIS_DB": REDIS_RESULTS_DB,
}

DATA_CACHE_CONFIG = CACHE_CONFIG

# ============================================================
# CELERY CONFIGURATION
# ============================================================
class CeleryConfig:
    broker_url = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_CELERY_DB}"
    result_backend = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_RESULTS_DB}"
    imports = ("superset.sql_lab", "superset.tasks.scheduler")
    task_annotations = {
        "sql_lab.get_sql_results": {"rate_limit": "100/s"},
    }
    beat_schedule = {
        "reports.scheduler": {
            "task": "reports.scheduler",
            "schedule": crontab(minute="*", hour="*"),
        },
        "reports.prune_log": {
            "task": "reports.prune_log",
            "schedule": crontab(minute=10, hour=0),
        },
    }

CELERY_CONFIG = CeleryConfig

# ============================================================
# LANGUAGES (only EN and RU)
# ============================================================
LANGUAGES = {
    "en": {"flag": "us", "name": "English"},
    "ru": {"flag": "ru", "name": "Russian"},
}

# Default language
BABEL_DEFAULT_LOCALE = "en"

# ============================================================
# FEATURE FLAGS
# ============================================================
FEATURE_FLAGS = {
    "DASHBOARD_NATIVE_FILTERS": True,
    "DASHBOARD_CROSS_FILTERS": True,
    "DASHBOARD_NATIVE_FILTERS_SET": True,
    "ENABLE_TEMPLATE_PROCESSING": True,
    "EMBEDDED_SUPERSET": True,
    "ALERT_REPORTS": True,
    "ALLOW_ADHOC_SUBQUERY": True,
    "ENABLE_TEMPLATE_PROCESSING": True,
}

# ============================================================
# CSV/EXCEL UPLOAD CONFIGURATION
# ============================================================
# Enable CSV and Excel upload functionality
FEATURE_FLAGS["ALLOW_CSV_UPLOAD"] = True
FEATURE_FLAGS["ALLOW_EXCEL_UPLOAD"] = True

# CSV upload settings
CSV_EXTENSIONS = {"csv", "tsv", "txt"}
EXCEL_EXTENSIONS = {"xlsx", "xls"}
ALLOWED_EXTENSIONS = CSV_EXTENSIONS | EXCEL_EXTENSIONS

# Max file size for uploads (in bytes) - default 50MB
CSV_TO_HIVE_UPLOAD_S3_BUCKET = None
UPLOAD_FOLDER = "/app/superset_home/uploads/"
CSV_TO_HIVE_UPLOAD_DIRECTORY = UPLOAD_FOLDER

# Database for uploaded CSV/Excel files
# By default, will use the main database connection
UPLOADED_CSV_SCHEMA = None  # or specify a schema name like "uploads"

# ============================================================
# SECURITY
# ============================================================
# Talisman security
TALISMAN_ENABLED = True
TALISMAN_CONFIG = {
    "content_security_policy": None,
    "force_https": False,  # Set to True if using HTTPS
}

# CORS (configure as needed)
ENABLE_CORS = False

# ============================================================
# PRODUCTION SETTINGS
# ============================================================
# Disable debug mode
DEBUG = False
FLASK_USE_RELOAD = False

# Logging
LOG_LEVEL = os.environ.get("SUPERSET_LOG_LEVEL", "INFO")

# WebServer
SUPERSET_WEBSERVER_PORT = int(os.environ.get("SUPERSET_PORT", 8088))
SUPERSET_WEBSERVER_TIMEOUT = 300

# SQL Lab settings
SQLLAB_TIMEOUT = 300
SUPERSET_WEBSERVER_TIMEOUT = 300

# ============================================================
# OPTIONAL: SMTP CONFIGURATION (for alerts/reports)
# ============================================================
# EMAIL_NOTIFICATIONS = True
# SMTP_HOST = "smtp.example.com"
# SMTP_PORT = 587
# SMTP_STARTTLS = True
# SMTP_SSL = False
# SMTP_USER = "user@example.com"
# SMTP_PASSWORD = "password"
# SMTP_MAIL_FROM = "superset@example.com"

# ============================================================
# CUSTOM LOGO STYLING
# ============================================================
# Increase logo size in navbar
CUSTOM_CSS = """
.navbar-brand img {
    height: 80px !important;
    max-height: 80px !important;
    width: auto !important;
    max-width: 500px !important;
    object-fit: contain !important;
}
"""

# ============================================================
# CLICKHOUSE SUPPORT
# ============================================================
# ClickHouse driver is installed (clickhouse-connect)
#
# Connection string format:
# clickhousedb://username:password@host:port/database
#
# Example HTTP connection:
# clickhousedb://default:@clickhouse-server:8123/default
#
# Example HTTPS connection:
# clickhousedb://username:password@clickhouse-server:8443/database?protocol=https
#
# Common parameters:
# - secure=true/false       - use HTTPS
# - verify=true/false       - verify SSL certificate
# - compress=true/false     - enable compression
# - session_id=<string>     - session identifier
#
# To add ClickHouse database:
# 1. Go to Data → Databases → + Database
# 2. Select "ClickHouse Connect" from the list
# 3. Enter connection details:
#    - Host: clickhouse-server
#    - Port: 8123 (HTTP) or 8443 (HTTPS)
#    - Database name: default (or your database)
#    - Username: default
#    - Password: (if required)
#
# Refer to documentation:
# https://clickhouse.com/docs/en/integrations/superset

# ============================================================
# KAZAKHSTAN MAP
# ============================================================
# Kazakhstan map is available in Country Map visualization
# Use "Kazakhstan" or "Kazakhstan Districts" from the country selector

