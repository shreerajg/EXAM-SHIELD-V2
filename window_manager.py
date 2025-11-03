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
        
        # Premium configuration - Updated to not force fullscreen
        self.config = {
            'prevent_minimize': True,
            'prevent_close': True,
            'prevent_alt_tab': False,  # Allow Alt+Tab for better user experience
            'force_topmost': False,    # Don't force topmost, just disable buttons
            'block_task_manager': True,
            'disable_system_menu': True  # Disable system menu (right-click on title bar)
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
                                       "Premium window protection activated - buttons disabled")
            return True
            
        except Exception as e:
            if self.logger:
                self.logger.log_activity("WINDOW_PROTECTION_ERROR", 
                                       f"Failed to start window protection: {str(e)}")
            return False

    def stop_window_protection(self):
        """Stop window protection and restore window functionality"""
        try:
            self.is_active = False
            self.stop_monitoring = True
            
            # Restore all protected windows
            self._restore_all_windows()
            
            if self.monitoring_thread:
                self.monitoring_thread.join(timeout=2)
            
            if self.logger:
                self.logger.log_activity("WINDOW_PROTECTION_STOPPED", 
                                       "Window protection deactivated - functionality restored")
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
                time.sleep(1.0)  # Check every 1 second (less frequent for better performance)
            except Exception as e:
                if self.logger:
                    self.logger.log_activity("WINDOW_MONITOR_ERROR", f"Window monitoring error: {str(e)}")
                time.sleep(2)

    def _enforce_window_rules(self):
        """Enforce window protection rules without forcing fullscreen"""
        try:
            # Get all visible windows
            def enum_windows_callback(hwnd, windows):
                if win32gui.IsWindowVisible(hwnd):
                    window_text = win32gui.GetWindowText(hwnd)
                    if window_text:
                        windows.append((hwnd, window_text))
                return True
            
            windows = []
            win32gui.EnumWindows(enum_windows_callback, windows)
            
            for hwnd, title in windows:
                if self._is_protected_window(title):
                    self._protect_window(hwnd, title)
                    
        except Exception as e:
            if self.logger:
                self.logger.log_activity("WINDOW_ENFORCEMENT_ERROR", f"Error enforcing rules: {str(e)}")

    def _protect_window(self, hwnd, title):
        """Apply protection to individual window - disable buttons only"""
        try:
            # Track protected windows
            window_info = {'hwnd': hwnd, 'title': title}
            if window_info not in self.protected_windows:
                self.protected_windows.append(window_info)
            
            # Get system menu handle
            menu = win32gui.GetSystemMenu(hwnd, False)
            if menu:
                # Disable close button if configured
                if self.config['prevent_close']:
                    win32gui.EnableMenuItem(menu, win32con.SC_CLOSE, 
                                          win32con.MF_BYCOMMAND | win32con.MF_GRAYED | win32con.MF_DISABLED)
                
                # Disable minimize button if configured
                if self.config['prevent_minimize']:
                    win32gui.EnableMenuItem(menu, win32con.SC_MINIMIZE, 
                                          win32con.MF_BYCOMMAND | win32con.MF_GRAYED | win32con.MF_DISABLED)
                    
                    # Also disable the minimize button on title bar
                    style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
                    style = style & ~win32con.WS_MINIMIZEBOX
                    win32gui.SetWindowLong(hwnd, win32con.GWL_STYLE, style)
                
                # Disable maximize/restore if needed (optional)
                if self.config.get('prevent_maximize', False):
                    win32gui.EnableMenuItem(menu, win32con.SC_MAXIMIZE, 
                                          win32con.MF_BYCOMMAND | win32con.MF_GRAYED | win32con.MF_DISABLED)
                    win32gui.EnableMenuItem(menu, win32con.SC_RESTORE, 
                                          win32con.MF_BYCOMMAND | win32con.MF_GRAYED | win32con.MF_DISABLED)
                    
                    # Also disable maximize button on title bar
                    style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
                    style = style & ~win32con.WS_MAXIMIZEBOX
                    win32gui.SetWindowLong(hwnd, win32con.GWL_STYLE, style)
                
                # Disable system menu entirely if configured
                if self.config['disable_system_menu']:
                    style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
                    style = style & ~win32con.WS_SYSMENU
                    win32gui.SetWindowLong(hwnd, win32con.GWL_STYLE, style)
            
            # Only set topmost if explicitly configured (not by default)
            if self.config.get('force_topmost', False):
                win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                                    win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_NOACTIVATE)
                    
        except Exception as e:
            if self.logger:
                self.logger.log_activity("WINDOW_PROTECTION_ERROR", 
                                       f"Error protecting window '{title}': {str(e)}")

    def _restore_all_windows(self):
        """Restore functionality to all protected windows"""
        for window_info in self.protected_windows:
            try:
                hwnd = window_info['hwnd']
                if win32gui.IsWindow(hwnd):
                    # Restore system menu
                    win32gui.GetSystemMenu(hwnd, True)  # Reset to default
                    
                    # Restore window style
                    style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
                    style = style | win32con.WS_MINIMIZEBOX | win32con.WS_MAXIMIZEBOX | win32con.WS_SYSMENU
                    win32gui.SetWindowLong(hwnd, win32con.GWL_STYLE, style)
                    
                    # Remove topmost if it was set
                    win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0,
                                        win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_NOACTIVATE)
            except:
                pass  # Window might have been closed
        
        self.protected_windows.clear()

    def _is_protected_window(self, title):
        """Determine if window should be protected"""
        protected_keywords = [
            'exam', 'test', 'quiz', 'assessment',
            'exam shield', 'browser', 'secure',
            'proctoring', 'monitoring'
        ]
        
        title_lower = title.lower()
        return any(keyword in title_lower for keyword in protected_keywords)

    def protect_specific_window(self, window_title):
        """Manually protect a specific window by title"""
        try:
            hwnd = win32gui.FindWindow(None, window_title)
            if hwnd:
                self._protect_window(hwnd, window_title)
                if self.logger:
                    self.logger.log_activity("MANUAL_PROTECTION", f"Protected window: {window_title}")
                return True
        except Exception as e:
            if self.logger:
                self.logger.log_activity("MANUAL_PROTECTION_ERROR", 
                                       f"Failed to protect '{window_title}': {str(e)}")
        return False

    def get_status(self):
        """Get window manager status"""
        return {
            'active': self.is_active,
            'protected_windows': len(self.protected_windows),
            'configuration': self.config,
            'monitoring': not self.stop_monitoring,
            'protection_mode': 'Button Disable Only' if not self.config.get('force_topmost', False) else 'Full Protection'
        }