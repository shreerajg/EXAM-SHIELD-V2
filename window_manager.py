"""
Window Manager for Exam Shield Premium
Complete rewrite with aggressive window protection using Windows API
FIXED: Improved stability and crash prevention
"""

import win32gui
import win32con
import win32api
import win32process
import ctypes
from ctypes import wintypes, windll
import threading
import time
import psutil
import os

class WindowManager:
    def __init__(self, logger=None):
        self.logger = logger
        self.is_active = False
        self.protected_windows = {}
        self.monitoring_thread = None
        self.stop_monitoring = False
        
        # Windows API handles with error checking
        try:
            self.user32 = windll.user32
            self.kernel32 = windll.kernel32
        except Exception as e:
            print(f"❌ Failed to initialize Windows API: {e}")
            self.user32 = None
            self.kernel32 = None
        
        # Window message hook
        self.hook_id = None
        self.HOOKPROC = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_int, wintypes.WPARAM, wintypes.LPARAM)
        self.hook = None
        
        # IMPROVED: More conservative protection configuration
        self.config = {
            'prevent_minimize': True,
            'prevent_close': True,
            'prevent_maximize': False,  # Allow maximize for better user experience
            'block_alt_f4': False,     # DISABLED to prevent conflicts
            'block_alt_tab': False,     # Allow Alt+Tab for better experience
            'block_win_key': False,     # DISABLED to prevent system issues
            'force_focus': False,       # DISABLED to prevent focus stealing
            'disable_taskbar_access': False,  # DISABLED to prevent system issues
            'monitor_new_windows': True
        }
        
        # Protected process names (exam software, browsers, etc.)
        self.protected_processes = [
            'chrome.exe', 'firefox.exe', 'msedge.exe', 'iexplore.exe',
            'examsoft.exe', 'respondus.exe', 'proctorio.exe',
            'exam_shield.exe', 'python.exe', 'pythonw.exe'
        ]
        
        print("✅ Window Manager initialized with conservative settings")

    def start_window_protection(self, config=None):
        """Start window protection with improved error handling"""
        if self.is_active:
            print("⚠️ Window protection already active")
            return True
            
        if not self.user32 or not self.kernel32:
            print("❌ Cannot start window protection - Windows API not available")
            return False
            
        if config:
            self.config.update(config)
        
        try:
            self.is_active = True
            self.stop_monitoring = False
            
            # Start monitoring thread with error handling
            self.monitoring_thread = threading.Thread(target=self._safe_monitor, daemon=True)
            self.monitoring_thread.start()
            
            # Log success
            if self.logger:
                self.logger.log_activity("WINDOW_PROTECTION_STARTED", 
                                       "Window protection activated with conservative settings")
            
            print("✅ Window protection started successfully")
            return True
            
        except Exception as e:
            self.is_active = False
            if self.logger:
                self.logger.log_activity("WINDOW_PROTECTION_ERROR", 
                                       f"Failed to start window protection: {str(e)}")
            print(f"❌ Failed to start window protection: {e}")
            return False

    def stop_window_protection(self):
        """Stop window protection and restore all windows safely"""
        try:
            print("🔄 Stopping window protection...")
            self.is_active = False
            self.stop_monitoring = True
            
            # Restore all protected windows
            self._restore_all_windows()
            
            # Wait for monitoring thread to finish
            if self.monitoring_thread and self.monitoring_thread.is_alive():
                self.monitoring_thread.join(timeout=3)
            
            if self.logger:
                self.logger.log_activity("WINDOW_PROTECTION_STOPPED", 
                                       "Window protection deactivated - All windows restored")
            
            print("✅ Window protection stopped successfully")
            return True
            
        except Exception as e:
            if self.logger:
                self.logger.log_activity("WINDOW_PROTECTION_ERROR", 
                                       f"Error stopping window protection: {str(e)}")
            print(f"❌ Error stopping window protection: {e}")
            return False

    def _safe_monitor(self):
        """Safe monitoring wrapper to prevent crashes"""
        print("🔄 Window monitoring started")
        
        while not self.stop_monitoring and self.is_active:
            try:
                self._monitor_cycle()
                time.sleep(1.0)  # 1 second intervals for stability
                
            except Exception as e:
                print(f"⚠️ Monitor cycle error (continuing): {e}")
                if self.logger:
                    self.logger.log_activity("MONITOR_ERROR", f"Monitor cycle error: {str(e)}")
                time.sleep(2)  # Wait longer on error
        
        print("🔄 Window monitoring stopped")

    def _monitor_cycle(self):
        """Single monitoring cycle with error handling"""
        try:
            # Get all visible windows safely
            windows = self._get_windows_safely()
            
            # Process each window
            for hwnd in windows:
                try:
                    if self._should_protect_window_safely(hwnd):
                        self._apply_protection_safely(hwnd)
                except Exception as e:
                    # Skip problematic windows instead of crashing
                    continue
            
            # Clean up closed windows
            self._cleanup_closed_windows()
            
        except Exception as e:
            print(f"⚠️ Monitor cycle exception: {e}")
            raise  # Re-raise for safe_monitor to handle

    def _get_windows_safely(self):
        """Get windows list with error handling"""
        windows = []
        
        def enum_callback(hwnd, windows_list):
            try:
                if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd):
                    windows_list.append(hwnd)
            except:
                pass  # Skip problematic windows
            return True
        
        try:
            win32gui.EnumWindows(enum_callback, windows)
        except Exception as e:
            print(f"⚠️ Error enumerating windows: {e}")
        
        return windows

    def _should_protect_window_safely(self, hwnd):
        """Determine if a window should be protected (with error handling)"""
        try:
            # Check if window is valid
            if not win32gui.IsWindow(hwnd):
                return False
                
            title = win32gui.GetWindowText(hwnd)
            if not title:
                return False
            
            # Get process info safely
            try:
                _, pid = win32process.GetWindowThreadProcessId(hwnd)
                process = psutil.Process(pid)
                process_name = process.name().lower()
                
                # Protect based on process name
                if any(proc in process_name for proc in self.protected_processes):
                    return True
                
            except (psutil.NoSuchProcess, psutil.AccessDenied, Exception):
                pass  # Continue with title-based check
            
            # Protect based on window title keywords
            title_lower = title.lower()
            protected_keywords = [
                'exam', 'test', 'quiz', 'assessment', 'proctoring',
                'browser', 'chrome', 'firefox', 'edge',
                'secure', 'lockdown'
            ]
            
            return any(keyword in title_lower for keyword in protected_keywords)
            
        except Exception as e:
            # If we can't determine, don't protect (safer)
            return False

    def _apply_protection_safely(self, hwnd):
        """Apply protection to a window with comprehensive error handling"""
        try:
            # Check if already protected
            if hwnd in self.protected_windows:
                self._maintain_protection_safely(hwnd)
                return
            
            # Get window info before modification
            title = win32gui.GetWindowText(hwnd)
            if not title:
                return
            
            try:
                original_style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
                original_ex_style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
            except Exception as e:
                print(f"⚠️ Could not get window styles for '{title}': {e}")
                return
            
            # Store window info
            self.protected_windows[hwnd] = {
                'title': title,
                'original_style': original_style,
                'original_ex_style': original_ex_style,
                'protection_applied': False
            }
            
            # Apply protection
            self._modify_window_safely(hwnd, title)
            
        except Exception as e:
            print(f"⚠️ Error applying protection to window: {e}")
            # Remove from protected list if protection failed
            if hwnd in self.protected_windows:
                del self.protected_windows[hwnd]

    def _modify_window_safely(self, hwnd, title):
        """Modify window properties safely"""
        try:
            window_info = self.protected_windows[hwnd]
            
            if window_info['protection_applied']:
                return
            
            # Get current style
            current_style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
            new_style = current_style
            
            # Remove window control buttons
            if self.config['prevent_minimize']:
                new_style = new_style & ~win32con.WS_MINIMIZEBOX
            
            if self.config['prevent_close']:
                new_style = new_style & ~win32con.WS_SYSMENU
            
            if self.config['prevent_maximize']:
                new_style = new_style & ~win32con.WS_MAXIMIZEBOX
            
            # Apply new style
            if new_style != current_style:
                win32gui.SetWindowLong(hwnd, win32con.GWL_STYLE, new_style)
                
                # Force window to redraw to show changes
                win32gui.SetWindowPos(hwnd, 0, 0, 0, 0, 0,
                                    win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | 
                                    win32con.SWP_NOZORDER | win32con.SWP_FRAMECHANGED)
            
            # Disable system menu items
            try:
                menu = win32gui.GetSystemMenu(hwnd, False)
                if menu:
                    menu_items = [win32con.SC_CLOSE, win32con.SC_MINIMIZE, win32con.SC_MAXIMIZE]
                    for item in menu_items:
                        win32gui.EnableMenuItem(menu, item, 
                                              win32con.MF_BYCOMMAND | win32con.MF_GRAYED)
            except Exception as e:
                print(f"⚠️ Could not modify system menu for '{title}': {e}")
            
            window_info['protection_applied'] = True
            
            if self.logger:
                self.logger.log_activity("WINDOW_PROTECTED", f"Applied protection to: {title}")
            
            print(f"✅ Protected window: {title}")
            
        except Exception as e:
            print(f"⚠️ Error modifying window '{title}': {e}")
            raise

    def _maintain_protection_safely(self, hwnd):
        """Maintain protection on already protected window"""
        try:
            if not win32gui.IsWindow(hwnd):
                return
            
            # Check if window is minimized and restore if needed
            if self.config['prevent_minimize'] and win32gui.IsIconic(hwnd):
                win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                
                title = self.protected_windows[hwnd]['title']
                if self.logger:
                    self.logger.log_activity("WINDOW_RESTORED", f"Restored minimized window: {title}")
                print(f"🔄 Restored minimized window: {title}")
        
        except Exception as e:
            # Don't crash on maintenance errors, just log
            pass

    def _cleanup_closed_windows(self):
        """Remove closed windows from protection list"""
        closed_windows = []
        
        for hwnd in list(self.protected_windows.keys()):
            try:
                if not win32gui.IsWindow(hwnd):
                    closed_windows.append(hwnd)
            except:
                closed_windows.append(hwnd)
        
        for hwnd in closed_windows:
            del self.protected_windows[hwnd]

    def _restore_all_windows(self):
        """Restore all protected windows to their original state"""
        print(f"🔄 Restoring {len(self.protected_windows)} protected windows...")
        
        for hwnd, window_info in list(self.protected_windows.items()):
            try:
                if win32gui.IsWindow(hwnd):
                    # Restore original window style
                    win32gui.SetWindowLong(hwnd, win32con.GWL_STYLE, window_info['original_style'])
                    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, window_info['original_ex_style'])
                    
                    # Reset system menu to default
                    win32gui.GetSystemMenu(hwnd, True)
                    
                    # Force redraw
                    win32gui.SetWindowPos(hwnd, 0, 0, 0, 0, 0,
                                        win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | 
                                        win32con.SWP_NOZORDER | win32con.SWP_FRAMECHANGED)
                    
                    if self.logger:
                        self.logger.log_activity("WINDOW_RESTORED", f"Restored window: {window_info['title']}")
                    
                    print(f"✅ Restored window: {window_info['title']}")
                    
            except Exception as e:
                print(f"⚠️ Error restoring window '{window_info.get('title', 'Unknown')}': {e}")
        
        self.protected_windows.clear()
        print("✅ All windows restored")

    def protect_specific_window(self, window_title_or_handle):
        """Manually protect a specific window"""
        try:
            if isinstance(window_title_or_handle, int):
                hwnd = window_title_or_handle
                title = win32gui.GetWindowText(hwnd)
            else:
                hwnd = win32gui.FindWindow(None, window_title_or_handle)
                title = window_title_or_handle
            
            if hwnd and win32gui.IsWindow(hwnd):
                self._apply_protection_safely(hwnd)
                return True
        except Exception as e:
            if self.logger:
                self.logger.log_activity("MANUAL_PROTECTION_ERROR", 
                                       f"Failed to protect window: {str(e)}")
            print(f"❌ Failed to protect window: {e}")
        return False

    def get_status(self):
        """Get detailed window manager status"""
        return {
            'active': self.is_active,
            'protected_windows_count': len(self.protected_windows),
            'protected_windows': {hwnd: info['title'] for hwnd, info in self.protected_windows.items()},
            'configuration': self.config,
            'monitoring_active': not self.stop_monitoring,
            'protection_level': 'CONSERVATIVE',
            'api_available': self.user32 is not None and self.kernel32 is not None
        }