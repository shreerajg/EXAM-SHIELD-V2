"""
Window Manager for Exam Shield Premium
Enhanced window protection with premium design elements
"""

import win32gui
import win32con
import win32api
import threading
import time
import psutil

class WindowManager:
    def __init__(self, logger=None):
        self.logger = logger
        self.is_active = False
        self.protected_windows = []
        self.monitoring_thread = None
        self.stop_monitoring = False
        
        # Premium configuration
        self.config = {
            'prevent_minimize': True,
            'prevent_close': True,
            'prevent_alt_tab': True,
            'force_topmost': True,
            'block_task_manager': True
        }

    def start_window_protection(self, config=None):
        """Start comprehensive window protection"""
        if config:
            self.config.update(config)
        
        try:
            self.is_active = True
            self.stop_monitoring = False
            
            # Start monitoring thread
            self.monitoring_thread = threading.Thread(target=self._monitor_windows, daemon=True)
            self.monitoring_thread.start()
            
            if self.logger:
                self.logger.log_activity("WINDOW_PROTECTION_STARTED", 
                                       "Premium window protection activated")
            return True
            
        except Exception as e:
            if self.logger:
                self.logger.log_activity("WINDOW_PROTECTION_ERROR", 
                                       f"Failed to start window protection: {str(e)}")
            return False

    def stop_window_protection(self):
        """Stop window protection"""
        try:
            self.is_active = False
            self.stop_monitoring = True
            
            if self.monitoring_thread:
                self.monitoring_thread.join(timeout=2)
            
            if self.logger:
                self.logger.log_activity("WINDOW_PROTECTION_STOPPED", 
                                       "Window protection deactivated")
            return True
            
        except Exception as e:
            if self.logger:
                self.logger.log_activity("WINDOW_PROTECTION_ERROR", 
                                       f"Error stopping window protection: {str(e)}")
            return False

    def _monitor_windows(self):
        """Monitor and protect windows continuously"""
        while not self.stop_monitoring and self.is_active:
            try:
                self._enforce_window_rules()
                time.sleep(0.5)  # Check every 500ms
            except Exception as e:
                if self.logger:
                    self.logger.log_activity("WINDOW_MONITOR_ERROR", f"Window monitoring error: {str(e)}")
                time.sleep(1)

    def _enforce_window_rules(self):
        """Enforce window protection rules"""
        try:
            # Get all windows
            def enum_windows_callback(hwnd, windows):
                if win32gui.IsWindowVisible(hwnd):
                    window_text = win32gui.GetWindowText(hwnd)
                    if window_text:
                        windows.append((hwnd, window_text))
                return True
            
            windows = []
            win32gui.EnumWindows(enum_windows_callback, windows)
            
            for hwnd, title in windows:
                self._protect_window(hwnd, title)
                
        except Exception as e:
            if self.logger:
                self.logger.log_activity("WINDOW_ENFORCEMENT_ERROR", f"Error enforcing rules: {str(e)}")

    def _protect_window(self, hwnd, title):
        """Apply protection to individual window"""
        try:
            # Check if this is a system critical window or exam software
            if self._is_protected_window(title):
                if self.config['force_topmost']:
                    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                                        win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
                
                # Disable close button if needed
                if self.config['prevent_close']:
                    self._disable_close_button(hwnd)
                    
        except Exception as e:
            pass  # Silently handle window protection errors

    def _is_protected_window(self, title):
        """Determine if window should be protected"""
        protected_keywords = [
            'exam', 'test', 'quiz', 'assessment',
            'exam shield', 'browser', 'secure'
        ]
        
        title_lower = title.lower()
        return any(keyword in title_lower for keyword in protected_keywords)

    def _disable_close_button(self, hwnd):
        """Disable window close button"""
        try:
            menu = win32gui.GetSystemMenu(hwnd, False)
            if menu:
                win32gui.EnableMenuItem(menu, win32con.SC_CLOSE, 
                                      win32con.MF_BYCOMMAND | win32con.MF_GRAYED)
        except:
            pass

    def get_status(self):
        """Get window manager status"""
        return {
            'active': self.is_active,
            'protected_windows': len(self.protected_windows),
            'configuration': self.config,
            'monitoring': not self.stop_monitoring
        }
