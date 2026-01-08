"""
Configuration settings for the application.
Generated: 2026-01-08 13:42:05 UTC
"""

# Application Settings
DEBUG = True
ENVIRONMENT = "development"
VERSION = "1.0.0"

# Server Configuration
HOST = "localhost"
PORT = 5000
TIMEOUT = 30

# Database Configuration
DATABASE = {
    "driver": "sqlite",
    "host": "localhost",
    "port": 5432,
    "name": "app_db",
    "user": "admin",
    "password": "change_me",
}

# Logging Configuration
LOGGING = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file": "app.log",
}

# API Configuration
API = {
    "base_url": "http://localhost:5000/api",
    "version": "v1",
    "timeout": 30,
}

# Security Configuration
SECURITY = {
    "secret_key": "your-secret-key-here",
    "jwt_secret": "your-jwt-secret-here",
    "cors_origins": ["http://localhost:3000"],
}

# Feature Flags
FEATURES = {
    "enable_caching": True,
    "enable_notifications": False,
    "enable_analytics": True,
}
