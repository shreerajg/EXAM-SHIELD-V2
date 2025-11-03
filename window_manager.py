"""
Window Manager for Exam Shield Premium
Complete rewrite with aggressive window protection using Windows API
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
        
        # Windows API handles
        self.user32 = windll.user32
        self.kernel32 = windll.kernel32
        
        # Window message hook
        self.hook_id = None
        self.HOOKPROC = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_int, wintypes.WPARAM, wintypes.LPARAM)
        self.hook = None
        
        # Aggressive protection configuration
        self.config = {
            'prevent_minimize': True,
            'prevent_close': True,
            'prevent_maximize': False,  # Allow maximize for better user experience
            'block_alt_f4': True,
            'block_alt_tab': False,     # Allow Alt+Tab but monitor it
            'block_win_key': True,
            'force_focus': True,        # Force focus back to protected windows
            'disable_taskbar_access': True,
            'monitor_new_windows': True
        }
        
        # Protected process names (exam software, browsers, etc.)
        self.protected_processes = [
            'chrome.exe', 'firefox.exe', 'msedge.exe', 'iexplore.exe',
            'examsoft.exe', 'respondus.exe', 'proctorio.exe',
            'exam_shield.exe', 'python.exe', 'pythonw.exe'
        ]

    def start_window_protection(self, config=None):
        """Start aggressive window protection"""
        if config:
            self.config.update(config)
        
        try:
            self.is_active = True
            self.stop_monitoring = False
            
            # Start aggressive monitoring thread
            self.monitoring_thread = threading.Thread(target=self._aggressive_monitor, daemon=True)
            self.monitoring_thread.start()
            
            # Install window procedure hook
            self._install_window_hook()
            
            if self.logger:
                self.logger.log_activity("WINDOW_PROTECTION_STARTED", 
                                       "AGGRESSIVE window protection activated - All controls disabled")
            return True
            
        except Exception as e:
            if self.logger:
                self.logger.log_activity("WINDOW_PROTECTION_ERROR", 
                                       f"Failed to start window protection: {str(e)}")
            return False

    def stop_window_protection(self):
        """Stop window protection and restore all windows"""
        try:
            self.is_active = False
            self.stop_monitoring = True
            
            # Remove hooks
            self._remove_window_hook()
            
            # Restore all protected windows to normal state
            self._restore_all_windows()
            
            if self.monitoring_thread and self.monitoring_thread.is_alive():
                self.monitoring_thread.join(timeout=3)
            
            if self.logger:
                self.logger.log_activity("WINDOW_PROTECTION_STOPPED", 
                                       "Window protection deactivated - All windows restored")
            return True
            
        except Exception as e:
            if self.logger:
                self.logger.log_activity("WINDOW_PROTECTION_ERROR", 
                                       f"Error stopping window protection: {str(e)}")
            return False

    def _aggressive_monitor(self):
        """Aggressive monitoring loop that enforces window rules every 100ms"""
        while not self.stop_monitoring and self.is_active:
            try:
                # Get all visible windows
                self._scan_and_protect_windows()
                
                # Enforce protection on existing windows
                self._enforce_aggressive_protection()
                
                # Monitor for new windows
                if self.config['monitor_new_windows']:
                    self._detect_new_windows()
                
                # Very frequent checks for maximum protection
                time.sleep(0.1)  # 100ms intervals
                
            except Exception as e:
                if self.logger:
                    self.logger.log_activity("MONITOR_ERROR", f"Monitoring error: {str(e)}")
                time.sleep(0.5)

    def _scan_and_protect_windows(self):
        """Scan for windows that need protection and apply it"""
        def enum_callback(hwnd, windows):
            if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd):
                windows.append(hwnd)
            return True
        
        windows = []
        win32gui.EnumWindows(enum_callback, windows)
        
        for hwnd in windows:
            try:
                window_title = win32gui.GetWindowText(hwnd)
                if self._should_protect_window(hwnd, window_title):
                    self._apply_aggressive_protection(hwnd, window_title)
            except:
                continue  # Skip windows that can't be processed

    def _should_protect_window(self, hwnd, title):
        """Determine if a window should be aggressively protected"""
        if not title:
            return False
        
        # Get process info
        try:
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            process = psutil.Process(pid)
            process_name = process.name().lower()
            
            # Protect based on process name
            if any(proc in process_name for proc in self.protected_processes):
                return True
            
            # Protect based on window title keywords
            title_lower = title.lower()
            protected_keywords = [
                'exam', 'test', 'quiz', 'assessment', 'proctoring',
                'browser', 'chrome', 'firefox', 'edge',
                'secure', 'lockdown', 'kiosk'
            ]
            
            return any(keyword in title_lower for keyword in protected_keywords)
            
        except:
            return False

    def _apply_aggressive_protection(self, hwnd, title):
        """Apply aggressive protection to a window"""
        try:
            # Store window info if not already protected
            if hwnd not in self.protected_windows:
                # Get original window properties before modification
                original_style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
                original_ex_style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
                
                self.protected_windows[hwnd] = {
                    'title': title,
                    'original_style': original_style,
                    'original_ex_style': original_ex_style,
                    'protection_applied': False
                }
            
            window_info = self.protected_windows[hwnd]
            
            # Apply protection if not already done
            if not window_info['protection_applied']:
                # Completely disable system menu (removes all title bar buttons)
                current_style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
                
                # Remove minimize box, maximize box, and system menu
                new_style = current_style & ~win32con.WS_MINIMIZEBOX
                new_style = new_style & ~win32con.WS_MAXIMIZEBOX
                new_style = new_style & ~win32con.WS_SYSMENU
                
                win32gui.SetWindowLong(hwnd, win32con.GWL_STYLE, new_style)
                
                # Disable all system menu items
                menu = win32gui.GetSystemMenu(hwnd, False)
                if menu:
                    # Disable every possible system menu item
                    menu_items = [win32con.SC_CLOSE, win32con.SC_MINIMIZE, 
                                win32con.SC_MAXIMIZE, win32con.SC_RESTORE,
                                win32con.SC_MOVE, win32con.SC_SIZE]
                    
                    for item in menu_items:
                        win32gui.EnableMenuItem(menu, item, 
                                              win32con.MF_BYCOMMAND | win32con.MF_GRAYED | win32con.MF_DISABLED)
                
                # Make window stay on top if configured
                if self.config.get('force_topmost', False):
                    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                                        win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_NOACTIVATE)
                
                window_info['protection_applied'] = True
                
                if self.logger:
                    self.logger.log_activity("WINDOW_PROTECTED", 
                                           f"Applied aggressive protection to: {title}")
            
            # Continuous enforcement
            self._enforce_window_state(hwnd)
            
        except Exception as e:
            if self.logger:
                self.logger.log_activity("PROTECTION_ERROR", 
                                       f"Error protecting window '{title}': {str(e)}")

    def _enforce_window_state(self, hwnd):
        """Continuously enforce window state (prevent minimize, etc.)"""
        try:
            if not win32gui.IsWindow(hwnd):
                return
            
            # Check if window is minimized and restore it
            if win32gui.IsIconic(hwnd):
                win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                if self.logger:
                    title = win32gui.GetWindowText(hwnd)
                    self.logger.log_activity("WINDOW_RESTORED", f"Forced restore of minimized window: {title}")
            
            # Force focus if configured
            if self.config['force_focus']:
                current_foreground = win32gui.GetForegroundWindow()
                if current_foreground != hwnd and current_foreground not in self.protected_windows:
                    # Only force focus if current window is not protected
                    try:
                        win32gui.SetForegroundWindow(hwnd)
                    except:
                        pass  # Might fail due to system restrictions
        
        except Exception as e:
            pass  # Silently handle errors in continuous enforcement

    def _enforce_aggressive_protection(self):
        """Enforce protection on all registered windows"""
        windows_to_remove = []
        
        for hwnd, window_info in self.protected_windows.items():
            try:
                if win32gui.IsWindow(hwnd):
                    self._enforce_window_state(hwnd)
                else:
                    windows_to_remove.append(hwnd)
            except:
                windows_to_remove.append(hwnd)
        
        # Clean up closed windows
        for hwnd in windows_to_remove:
            del self.protected_windows[hwnd]

    def _detect_new_windows(self):
        """Detect and immediately protect new windows"""
        def enum_callback(hwnd, param):
            if hwnd not in self.protected_windows:
                try:
                    title = win32gui.GetWindowText(hwnd)
                    if win32gui.IsWindowVisible(hwnd) and title:
                        if self._should_protect_window(hwnd, title):
                            self._apply_aggressive_protection(hwnd, title)
                except:
                    pass
            return True
        
        win32gui.EnumWindows(enum_callback, None)

    def _install_window_hook(self):
        """Install window message hook to intercept close/minimize attempts"""
        try:
            # This would require more complex implementation
            # For now, rely on aggressive monitoring
            pass
        except Exception as e:
            if self.logger:
                self.logger.log_activity("HOOK_ERROR", f"Failed to install window hook: {str(e)}")

    def _remove_window_hook(self):
        """Remove window message hook"""
        try:
            if self.hook_id:
                self.user32.UnhookWindowsHookExW(self.hook_id)
                self.hook_id = None
        except:
            pass

    def _restore_all_windows(self):
        """Restore all protected windows to their original state"""
        for hwnd, window_info in self.protected_windows.items():
            try:
                if win32gui.IsWindow(hwnd):
                    # Restore original window style
                    win32gui.SetWindowLong(hwnd, win32con.GWL_STYLE, window_info['original_style'])
                    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, window_info['original_ex_style'])
                    
                    # Reset system menu to default
                    win32gui.GetSystemMenu(hwnd, True)
                    
                    # Remove topmost flag
                    win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0,
                                        win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_NOACTIVATE)
                    
                    if self.logger:
                        self.logger.log_activity("WINDOW_RESTORED", f"Restored window: {window_info['title']}")
            except Exception as e:
                if self.logger:
                    self.logger.log_activity("RESTORE_ERROR", f"Error restoring window: {str(e)}")
        
        self.protected_windows.clear()

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
                self._apply_aggressive_protection(hwnd, title)
                return True
        except Exception as e:
            if self.logger:
                self.logger.log_activity("MANUAL_PROTECTION_ERROR", 
                                       f"Failed to protect window: {str(e)}")
        return False

    def kill_dangerous_processes(self):
        """Kill processes that could be used to bypass protection"""
        dangerous_processes = [
            'taskmgr.exe', 'cmd.exe', 'powershell.exe', 'regedit.exe',
            'msconfig.exe', 'control.exe', 'explorer.exe'
        ]
        
        killed_count = 0
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if proc.info['name'].lower() in dangerous_processes:
                    proc.kill()
                    killed_count += 1
                    if self.logger:
                        self.logger.log_activity("PROCESS_KILLED", 
                                               f"Terminated dangerous process: {proc.info['name']}")
            except:
                continue
        
        return killed_count

    def get_status(self):
        """Get detailed window manager status"""
        return {
            'active': self.is_active,
            'protected_windows_count': len(self.protected_windows),
            'protected_windows': {hwnd: info['title'] for hwnd, info in self.protected_windows.items()},
            'configuration': self.config,
            'monitoring_active': not self.stop_monitoring,
            'protection_level': 'AGGRESSIVE',
            'hook_installed': self.hook_id is not None
        }