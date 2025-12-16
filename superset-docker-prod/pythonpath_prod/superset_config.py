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
# LANGUAGES (only RU - Russian interface)
# ============================================================
LANGUAGES = {
    "ru": {"flag": "ru", "name": "Русский"},
}

# Default language - Russian
BABEL_DEFAULT_LOCALE = "ru"

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
# CUSTOM CSS STYLING
# ============================================================
CUSTOM_CSS = """
/* ПОДКЛЮЧЕНИЕ ШРИФТА MONTSERRAT */
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800;900&display=swap');

/* БАЗОВЫЕ СТИЛИ */
body {
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%) !important;
  font-family: 'Montserrat', sans-serif !important;
  color: #16355A !important;
  margin: 0;
  padding: 20px;
  min-height: 100vh;
}

/* ЛОГОТИП В НАВБАРЕ */
.navbar-brand img {
    height: 80px !important;
    max-height: 80px !important;
    width: auto !important;
    max-width: 500px !important;
    object-fit: contain !important;
}

/* ОСНОВНОЙ КОНТЕЙНЕР ДАШБОРДА */
.css-1db2tta {
  background: linear-gradient(135deg, #e3f2fd 0%, #f3e5f5 100%) !important;
  border-radius: 24px !important;
  padding: 20px !important;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08), inset 0 1px 0 rgba(255, 255, 255, 0.6) !important;
}

/* ЗАГОЛОВОК ДАШБОРДА */
.dashboard-header,
.dashboard-component-header,
.css-1xz3a8f h4 {
  text-align: center !important;
  justify-content: center !important;
  margin: 0 auto 20px !important;
  width: 100% !important;
  color: #fff !important;
  font-weight: 700 !important;
  font-size: 32px !important;
  background: linear-gradient(135deg, #3b82f6 0%, #10b981 100%) !important;
  padding: 20px !important;
  border-radius: 20px !important;
  border: 3px solid rgba(255, 255, 255, 0.3) !important;
  box-shadow: 0 8px 25px rgba(59, 130, 246, 0.3), 0 4px 6px rgba(0, 0, 0, 0.1) !important;
  position: relative;
  overflow: hidden;
}

.dashboard-header::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: linear-gradient(45deg, transparent, rgba(255, 255, 255, 0.1), transparent);
  transform: rotate(45deg);
  animation: shimmer 3s infinite;
}

@keyframes shimmer {
  0% { transform: rotate(45deg) translateX(-100%); }
  100% { transform: rotate(45deg) translateX(100%); }
}

/* ВИДЖЕТЫ И КАРТОЧКИ */
.dashboard-component {
  border-radius: 20px !important;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08), inset 0 1px 0 rgba(255, 255, 255, 0.8) !important;
  background: white !important;
  border: 1px solid rgba(255, 255, 255, 0.9) !important;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
  overflow: hidden;
}

.dashboard-component:hover {
  transform: translateY(-5px) !important;
  box-shadow: 0 12px 35px rgba(0, 0, 0, 0.15), inset 0 1px 0 rgba(255, 255, 255, 0.9) !important;
}

/* ФОН ДЛЯ СЕКЦИЙ */
.css-14pwj7q, .css-dljexb {
  background: linear-gradient(135deg, #d8e2f3 0%, #e8edf8 100%) !important;
  border-radius: 16px !important;
  padding: 15px !important;
  margin: 10px 0 !important;
}

/* ГРАФИКИ - ОБЩИЕ СТИЛИ */
.dashboard-component-chart-holder {
  border-radius: 16px !important;
  background: linear-gradient(135deg, #dbeafe 0%, #e0f2fe 100%) !important;
  padding: 15px !important;
  border: 1px solid rgba(59, 130, 246, 0.1) !important;
}

/* УВЕЛИЧЕНИЕ ВСЕХ ТЕКСТОВ НА ГРАФИКАХ */
.dashboard-component-chart-holder svg text {
  font-size: 18px !important;
  font-weight: 700 !important;
  font-family: 'Montserrat', sans-serif !important;
  fill: #16355A !important;
}

/* ПРИНУДИТЕЛЬНОЕ УВЕЛИЧЕНИЕ ВСЕХ ТЕКСТОВ В SVG */
svg text {
  font-size: 18px !important;
  font-weight: 700 !important;
  font-family: 'Montserrat', sans-serif !important;
}

/* Оси X и Y */
.dashboard-component-chart-holder .nv-x text,
.dashboard-component-chart-holder .nv-y text {
  font-size: 16px !important;
  font-weight: 600 !important;
}

/* Числовые значения на графиках */
.dashboard-component-chart-holder .nv-bar .value,
.dashboard-component-chart-holder .nv-pie .value,
.dashboard-component-chart-holder .nv-line .value {
  font-size: 20px !important;
  font-weight: 800 !important;
}

/* Легенда */
.dashboard-component-chart-holder .nv-legend text {
  font-size: 16px !important;
  font-weight: 600 !important;
}

/* Заголовки графиков */
.dashboard-component-chart-holder .chart-title {
  font-size: 22px !important;
  font-weight: 800 !important;
}

/* ГРАФИК ПЛОСКОЕ ДЕРЕВО - УВЕЛИЧЕННЫЕ ШРИФТЫ */
.dashboard-component-chart-holder .treemap text,
.dashboard-component-chart-holder .nv-treemap text {
  font-size: 20px !important;
  font-weight: 800 !important;
  font-family: 'Montserrat', sans-serif !important;
}

/* Подписи в плоском дереве */
.dashboard-component-chart-holder .nv-treemap .nv-label,
.dashboard-component-chart-holder .treemap .label,
.dashboard-component-chart-holder .nv-treemap text.nv-label,
.dashboard-component-chart-holder .treemap text.label {
  font-size: 22px !important;
  font-weight: 800 !important;
  fill: white !important;
  text-shadow: 2px 2px 4px rgba(0,0,0,0.7) !important;
}

/* Значения в плоском дереве */
.dashboard-component-chart-holder .nv-treemap .nv-value,
.dashboard-component-chart-holder .treemap .value,
.dashboard-component-chart-holder .nv-treemap text.nv-value,
.dashboard-component-chart-holder .treemap text.value {
  font-size: 24px !important;
  font-weight: 900 !important;
  fill: white !important;
  text-shadow: 2px 2px 6px rgba(0,0,0,0.8) !important;
}

/* УНИВЕРСАЛЬНЫЕ СЕЛЕКТОРЫ ДЛЯ ЛЮБЫХ ПОДПИСЕЙ */
.nv-label,
.nv-value,
.chart-label,
.data-label,
.value,
.label {
  font-size: 20px !important;
  font-weight: 800 !important;
}

/* КНОПКИ И ЭЛЕМЕНТЫ УПРАВЛЕНИЯ */
.css-1vhmipf svg {
  border-radius: 12px !important;
  background: linear-gradient(135deg, #4a76a8 0%, #5a86b8 100%) !important;
  color: white;
  border: 2px solid #3a5e8c !important;
  box-shadow: 0 4px 8px rgba(74, 118, 168, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
  transition: all 0.3s ease !important;
}

.css-1vhmipf:hover svg {
  transform: scale(1.05) !important;
  box-shadow: 0 6px 15px rgba(74, 118, 168, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.3) !important;
}

.css-1xf2vnm {
  background: linear-gradient(135deg, #4a76a8 0%, #5a86b8 100%) !important;
  color: white !important;
  box-shadow: 0 4px 8px rgba(74, 118, 168, 0.3) !important;
  padding: 12px 20px !important;
  border-radius: 12px !important;
  border: 1px solid rgba(255, 255, 255, 0.2) !important;
}

/* МЕНЮ И ВЫПАДАЮЩИЕ СПИСКИ */
.css-1xj2cxp, .css-1pypwot {
  background: linear-gradient(135deg, #4a76a8 0%, #5a86b8 100%) !important;
  color: white !important;
  box-shadow: 0 6px 15px rgba(74, 118, 168, 0.3) !important;
  border-radius: 12px !important;
  border: 1px solid rgba(255, 255, 255, 0.2) !important;
}

/* ПОЛЯ ВВОДА И ФИЛЬТРЫ */
.css-1f1pobk {
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%) !important;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05), inset 0 1px 0 rgba(255, 255, 255, 0.8) !important;
  border-radius: 12px !important;
  border: 1px solid #e2e8f0 !important;
}

.css-1f1pobk::placeholder {
  color: #64748b !important;
}

/* ПУХЛЫЕ KPI-КАРТОЧКИ */
.dashboard-component.kpi {
  font-size: 28px !important;
  background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%) !important;
  border-radius: 20px !important;
  padding: 25px !important;
  border: 3px solid #e2e8f0 !important;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1), inset 0 1px 0 rgba(255, 255, 255, 0.9) !important;
  transition: all 0.3s ease !important;
  min-height: 140px !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  text-align: center !important;
  position: relative !important;
  overflow: hidden !important;
}

.dashboard-component.kpi:hover {
  transform: translateY(-5px) scale(1.02) !important;
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15), inset 0 1px 0 rgba(255, 255, 255, 0.95) !important;
  border-color: #3b82f6 !important;
}

.dashboard-component.kpi::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(135deg, #3b82f6 0%, #10b981 100%) !important;
}

/* ТЕКСТ И ШРИФТЫ */
.css-1xz3a8f h4 {
  color: white !important;
  font-weight: 600 !important;
}

.css-1vhmipf {
  color: white !important;
}

.css-6szfdn, .css-15voufr {
  color: #16355A !important;
  font-weight: 600 !important;
}

/* ВСЕ ТЕКСТОВЫЕ ЭЛЕМЕНТЫ */
.dashboard-component * {
  color: #16355A !important;
  font-family: 'Montserrat', sans-serif !important;
}

/* Заголовки внутри виджетов */
.dashboard-component h1,
.dashboard-component h2,
.dashboard-component h3,
.dashboard-component h4,
.dashboard-component h5,
.dashboard-component h6 {
  color: #16355A !important;
}

/* Текст в таблицах и графиках */
.dashboard-component table,
.dashboard-component td,
.dashboard-component th,
.dashboard-component span,
.dashboard-component div {
  color: #16355A !important;
}

/* Легенды графиков и подписи */
.dashboard-component .legend,
.dashboard-component .axis text,
.dashboard-component .label {
  color: #16355A !important;
}

/* ДОПОЛНИТЕЛЬНЫЕ ЭЛЕМЕНТЫ */
.css-d0k8zk, .css-1jh84qf, .css-1e88phb, .css-1f5gi03 {
  background: linear-gradient(135deg, #4a76a8 0%, #5a86b8 100%) !important;
  color: white !important;
  box-shadow: 0 4px 8px rgba(74, 118, 168, 0.3) !important;
  border-radius: 10px !important;
}

.css-13f5axy svg {
  color: #16355A !important;
}

.css-1t4ixh1 svg {
  color: white !important;
}

/* СКРЫТИЕ ЛИШНИХ ЭЛЕМЕНТОВ ГРАФИКОВ */
.dashboard-chart-id-539 .css-xojzyz,
.dashboard-chart-id-540 .css-xojzyz,
.dashboard-chart-id-541 .css-xojzyz {
  display: none !important;
}

/* БОЛЬШИЕ ТУЛТИПЫ ГРАФИКОВ */
div[style*="z-index: 9999999"] {
  font-size: 18px !important;
  font-weight: 600 !important;
  padding: 20px !important;
  min-width: 300px !important;
  background: white !important;
  border: 2px solid #3b82f6 !important;
  border-radius: 12px !important;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2) !important;
}

div[style*="z-index: 9999999"] span[style*="opacity: 0.7"] {
  font-size: 16px !important;
  font-weight: 500 !important;
  margin-bottom: 10px !important;
  display: block !important;
}

div[style*="z-index: 9999999"] span[style*="font-weight: 700"] {
  font-size: 18px !important;
  font-weight: 700 !important;
}

div[style*="z-index: 9999999"] span[style*="border-radius:10px"] {
  width: 16px !important;
  height: 16px !important;
  margin-right: 8px !important;
}

/* АДАПТИВНОСТЬ */
@media (max-width: 768px) {
  body {
    padding: 10px !important;
  }

  .dashboard-header {
    font-size: 24px !important;
    padding: 15px !important;
  }

  .dashboard-component {
    border-radius: 16px !important;
  }

  .dashboard-component-chart-holder svg text {
    font-size: 16px !important;
  }
}

/* Улучшенная читаемость */
.dashboard-component {
  font-weight: 500 !important;
  line-height: 1.6 !important;
}

.dashboard-component.kpi {
  font-weight: 700 !important;
}

.dashboard-header {
  font-weight: 800 !important;
  letter-spacing: 0.5px !important;
}

/* УНИВЕРСАЛЬНОЕ ПРИМЕНЕНИЕ MONTSERRAT */
* {
  font-family: 'Montserrat', sans-serif !important;
}

/* СИЛЬНЫЕ СЕЛЕКТОРЫ ДЛЯ ГРАФИКОВ */
svg text {
  font-size: 20px !important;
  font-weight: 700 !important;
}

.nv-node text {
  font-size: 22px !important;
  font-weight: 800 !important;
}

rect + text {
  font-size: 24px !important;
  font-weight: 900 !important;
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

