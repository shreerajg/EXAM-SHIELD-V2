"""
Configuration settings for Exam Shield
"""

import os

class Config:
    # Application settings
    APP_NAME = "Exam Shield"
    VERSION = "1.1.0"
    
    # Database settings
    DATABASE_NAME = "exam_shield.db"
    DATABASE_PATH = os.path.join(os.path.dirname(__file__), DATABASE_NAME)
    
    # Security settings - KEEPING ORIGINAL NAMES
    DEFAULT_ADMIN_USERNAME = "admin"
    DEFAULT_ADMIN_PASSWORD = "admin"
    
    # Blocked keys
    BLOCKED_KEYS = [
        'alt+tab', 'alt+f4', 'win+d', 'win+l', 'win+r',
        'ctrl+alt+del', 'ctrl+shift+esc', 'f11', 'alt+space',
        'win+tab', 'ctrl+alt+t'
    ]
    
    # Blocked mouse buttons
    BLOCKED_MOUSE_BUTTONS = [
        'middle', 'x1', 'x2', 'side'
    ]
    
    # Admin access key
    ADMIN_ACCESS_KEY = 'ctrl+shift+y'
    
    # Individual blocking control flags
    SELECTIVE_BLOCKING = {
        'keyboard': True,
        'mouse': True,
        'internet': True,
        'windows': True,
        'processes': True
    }
    
    # Network blocking settings
    BLOCK_INTERNET = True
    BLOCKED_WEBSITES = [
        'google.com', 'facebook.com', 'youtube.com', 'twitter.com',
        'instagram.com', 'tiktok.com', 'reddit.com', 'discord.com'
    ]
    
    # Premium UI Colors - UPDATED FOR PREMIUM LOOK
    COLORS = {
        'primary': '#1e3d59',      # Deep navy blue
        'secondary': '#17223b',     # Darker navy
        'accent': '#ffc947',       # Premium gold
        'success': '#27ae60',      # Professional green
        'danger': '#e74c3c',       # Professional red
        'warning': '#f39c12',      # Premium orange
        'info': '#3498db',         # Professional blue
        'surface': '#f8f9fa',      # Light surface
        'card': '#ffffff',         # White cards
        'text_primary': '#2c3e50', # Dark text
        'text_secondary': '#7f8c8d', # Gray text
        'border': '#dee2e6',       # Light borders
        'light_blue': '#ecf4ff',   # Very light blue
        'light_green': '#e8f5e8',  # Very light green
        'light_yellow': '#fff8e1', # Very light yellow
        'light_red': '#ffebee'     # Very light red
    }
    
    # Logging settings
    LOG_RETENTION_DAYS = 30
    MAX_LOG_ENTRIES = 10000
