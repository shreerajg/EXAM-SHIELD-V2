"""
Mouse Manager for Exam Shield Premium
Enhanced with premium error handling and logging
"""

import win32api
import win32con
import win32gui
from pynput import mouse
import threading
import time

class MouseManager:
    def __init__(self, logger=None):
        self.logger = logger
        self.is_active = False
        self.blocked_buttons = ['middle', 'x1', 'x2']  # Default blocked buttons
        self.hook_installed = False
        self.mouse_listener = None
        self.block_all = False
        
        # Premium styling colors for any UI elements
        self.colors = {
            'primary': '#1e3d59',
            'success': '#27ae60',
            'warning': '#f39c12',
            'danger': '#e74c3c'
        }

    def start_blocking(self, buttons=None):
        """Start mouse button blocking with premium error handling"""
        if buttons:
            self.blocked_buttons = buttons
        
        try:
            self.is_active = True
            self._setup_mouse_hook()
            
            if self.logger:
                self.logger.log_activity("MOUSE_BLOCKING_STARTED", 
                                       f"Mouse blocking activated for buttons: {', '.join(self.blocked_buttons)}")
            return True
            
        except Exception as e:
            if self.logger:
                self.logger.log_activity("MOUSE_BLOCKING_ERROR", f"Failed to start mouse blocking: {str(e)}")
            return False

    def stop_blocking(self):
        """Stop mouse button blocking"""
        try:
            self.is_active = False
            self._remove_mouse_hook()
            
            if self.logger:
                self.logger.log_activity("MOUSE_BLOCKING_STOPPED", "Mouse blocking deactivated")
            return True
            
        except Exception as e:
            if self.logger:
                self.logger.log_activity("MOUSE_BLOCKING_ERROR", f"Error stopping mouse blocking: {str(e)}")
            return False

    def _setup_mouse_hook(self):
        """Setup low-level mouse hook with premium error handling"""
        try:
            if not self.mouse_listener:
                self.mouse_listener = mouse.Listener(
                    on_click=self._on_mouse_click,
                    suppress=False
                )
                self.mouse_listener.start()
                self.hook_installed = True
        except Exception as e:
            if self.logger:
                self.logger.log_activity("MOUSE_HOOK_ERROR", f"Failed to install mouse hook: {str(e)}")

    def _remove_mouse_hook(self):
        """Remove mouse hook safely"""
        try:
            if self.mouse_listener:
                self.mouse_listener.stop()
                self.mouse_listener = None
                self.hook_installed = False
        except Exception as e:
            if self.logger:
                self.logger.log_activity("MOUSE_HOOK_ERROR", f"Error removing mouse hook: {str(e)}")

    def _on_mouse_click(self, x, y, button, pressed):
        """Handle mouse click events with premium logging"""
        if not self.is_active:
            return True
        
        button_name = str(button).replace('Button.', '').lower()
        
        if button_name in self.blocked_buttons or self.block_all:
            if self.logger:
                self.logger.log_activity("MOUSE_BLOCKED", 
                                       f"Blocked {button_name} button click at ({x}, {y})")
            return False  # Block the click
        
        return True  # Allow the click

    def add_blocked_button(self, button):
        """Add a button to the blocked list"""
        if button not in self.blocked_buttons:
            self.blocked_buttons.append(button)
            if self.logger:
                self.logger.log_activity("MOUSE_CONFIG", f"Added blocked button: {button}")

    def remove_blocked_button(self, button):
        """Remove a button from the blocked list"""
        if button in self.blocked_buttons:
            self.blocked_buttons.remove(button)
            if self.logger:
                self.logger.log_activity("MOUSE_CONFIG", f"Removed blocked button: {button}")

    def get_status(self):
        """Get current mouse manager status"""
        return {
            'active': self.is_active,
            'blocked_buttons': self.blocked_buttons,
            'hook_installed': self.hook_installed,
            'total_blocked': len(self.blocked_buttons)
        }
