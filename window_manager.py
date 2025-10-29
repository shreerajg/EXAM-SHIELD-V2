"""
Window Manager for Exam Shield Premium
Fixed version - Properly disables window buttons instead of fullscreen toggling
"""

import win32gui
import win32con
import win32api
import ctypes
from ctypes import wintypes, windll
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
            'prevent_maximize': True,
            'prevent_alt_tab': True,
            'block_task_manager': True,
            'disable_window_buttons': True  # NEW: Focus on button disabling
        }
        
        # Windows API constants for proper button disabling
        self.SC_MINIMIZE = 0xF020
        self.SC_MAXIMIZE = 0xF030
        self.SC_CLOSE = 0xF060
        self.MF_BYCOMMAND = 0x00000000
        self.MF_GRAYED = 0x00000001
        self.MF_DISABLED = 0x00000002

    def start_window_protection(self, config=None):
        """Start comprehensive window protection with proper button disabling"""
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
                                       "Premium window protection activated with button disabling")
            print("✅ Window protection started - Buttons will be disabled, not fullscreen")
            return True
            
        except Exception as e:
            if self.logger:
                self.logger.log_activity("WINDOW_PROTECTION_ERROR", 
                                       f"Failed to start window protection: {str(e)}")
            print(f"❌ Window protection error: {e}")
            return False

    def stop_window_protection(self):
        """Stop window protection and restore window functionality"""
        try:
            self.is_active = False
            self.stop_monitoring = True
            
            # Restore all previously protected windows
            self._restore_all_windows()
            
            if self.monitoring_thread:
                self.monitoring_thread.join(timeout=2)
            
            if self.logger:
                self.logger.log_activity("WINDOW_PROTECTION_STOPPED", 
                                       "Window protection deactivated, buttons restored")
            print("✅ Window protection stopped - Window buttons restored")
            return True
            
        except Exception as e:
            if self.logger:
                self.logger.log_activity("WINDOW_PROTECTION_ERROR", 
                                       f"Error stopping window protection: {str(e)}")
            print(f"❌ Error stopping window protection: {e}")
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
        """Enforce window protection rules - FIXED to disable buttons properly"""
        try:
            # Get all visible windows
            def enum_windows_callback(hwnd, windows):
                if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd):
                    window_text = win32gui.GetWindowText(hwnd)
                    if window_text and len(window_text.strip()) > 0:
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
        """Apply protection to individual window - FIXED implementation"""
        try:
            # Check if this window should be protected
            if self._is_protected_window(title):
                
                # FIXED: Disable window buttons instead of making topmost
                if self.config['disable_window_buttons']:
                    self._disable_window_buttons(hwnd)
                    
                # Keep track of protected windows
                if hwnd not in self.protected_windows:
                    self.protected_windows.append(hwnd)
                    if self.logger:
                        self.logger.log_activity("WINDOW_PROTECTED", 
                                               f"Window protected: {title}")
                    print(f"🛡️ Protected window: {title}")
                    
        except Exception as e:
            pass  # Silently handle individual window protection errors

    def _disable_window_buttons(self, hwnd):
        """FIXED: Properly disable minimize, maximize, and close buttons"""
        try:
            # Get the system menu for the window
            hmenu = win32gui.GetSystemMenu(hwnd, False)
            if not hmenu:
                return
                
            # Disable minimize button
            if self.config['prevent_minimize']:
                win32gui.EnableMenuItem(hmenu, self.SC_MINIMIZE, 
                                      self.MF_BYCOMMAND | self.MF_GRAYED | self.MF_DISABLED)
                
            # Disable maximize button  
            if self.config['prevent_maximize']:
                win32gui.EnableMenuItem(hmenu, self.SC_MAXIMIZE, 
                                      self.MF_BYCOMMAND | self.MF_GRAYED | self.MF_DISABLED)
                
            # Disable close button
            if self.config['prevent_close']:
                win32gui.EnableMenuItem(hmenu, self.SC_CLOSE, 
                                      self.MF_BYCOMMAND | self.MF_GRAYED | self.MF_DISABLED)
                
            # Remove minimize and maximize from window style (additional protection)
            style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
            if self.config['prevent_minimize']:
                style &= ~win32con.WS_MINIMIZEBOX
            if self.config['prevent_maximize']:
                style &= ~win32con.WS_MAXIMIZEBOX
            win32gui.SetWindowLong(hwnd, win32con.GWL_STYLE, style)
            
            # Force window redraw to show changes
            win32gui.SetWindowPos(hwnd, 0, 0, 0, 0, 0, 
                                win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | 
                                win32con.SWP_NOZORDER | win32con.SWP_FRAMECHANGED)
                                
        except Exception as e:
            print(f"Warning: Could not disable buttons for window: {e}")

    def _restore_all_windows(self):
        """Restore functionality to all previously protected windows"""
        for hwnd in self.protected_windows.copy():
            try:
                self._restore_window_buttons(hwnd)
            except:
                pass
        self.protected_windows.clear()

    def _restore_window_buttons(self, hwnd):
        """Restore window buttons to normal functionality"""
        try:
            # Restore system menu
            win32gui.GetSystemMenu(hwnd, True)  # True = restore original menu
            
            # Restore window style
            style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
            style |= win32con.WS_MINIMIZEBOX | win32con.WS_MAXIMIZEBOX
            win32gui.SetWindowLong(hwnd, win32con.GWL_STYLE, style)
            
            # Force redraw
            win32gui.SetWindowPos(hwnd, 0, 0, 0, 0, 0, 
                                win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | 
                                win32con.SWP_NOZORDER | win32con.SWP_FRAMECHANGED)
                                
        except Exception as e:
            print(f"Warning: Could not restore window: {e}")

    def _is_protected_window(self, title):
        """Determine if window should be protected - EXPANDED criteria"""
        protected_keywords = [
            'exam', 'test', 'quiz', 'assessment', 'exam shield', 'browser', 'secure',
            'chrome', 'firefox', 'edge', 'safari', 'opera',  # Browsers
            'notepad', 'wordpad', 'word', 'excel', 'powerpoint',  # Office apps
            'calculator', 'paint', 'cmd', 'powershell',  # System apps that should be controlled
            'visual studio', 'code', 'sublime', 'notepad++',  # Code editors
            'adobe', 'photoshop', 'illustrator',  # Creative apps
        ]
        
        # Exclude system windows that should not be protected
        excluded_keywords = [
            'taskbar', 'desktop', 'start menu', 'system tray', 'notification',
            'windows security', 'task manager', 'system configuration',
            'device manager', 'control panel', 'settings'
        ]
        
        title_lower = title.lower()
        
        # Don't protect excluded windows
        if any(excluded in title_lower for excluded in excluded_keywords):
            return False
            
        # Protect windows with protected keywords
        return any(keyword in title_lower for keyword in protected_keywords)

    def get_status(self):
        """Get window manager status with detailed info"""
        return {
            'active': self.is_active,
            'protected_windows': len(self.protected_windows),
            'configuration': self.config,
            'monitoring': not self.stop_monitoring,
            'protected_window_titles': [win32gui.GetWindowText(hwnd) for hwnd in self.protected_windows if win32gui.IsWindow(hwnd)]
        }