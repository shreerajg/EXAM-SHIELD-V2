"""
Mouse Manager for Exam Shield Premium
Complete rewrite with proper Windows API low-level hooks
"""

import win32api
import win32con
import win32gui
import ctypes
from ctypes import wintypes, windll
import threading
import time

class MouseManager:
    def __init__(self, logger=None):
        self.logger = logger
        self.is_active = False
        # Block middle mouse and custom buttons, allow left/right for basic interaction
        self.blocked_buttons = [win32con.WM_MBUTTONDOWN, win32con.WM_MBUTTONUP,
                               win32con.WM_XBUTTONDOWN, win32con.WM_XBUTTONUP]
        self.hook = None
        self.hook_id = None
        
        # Windows API constants
        self.WH_MOUSE_LL = 14
        self.WM_LBUTTONDOWN = 0x0201
        self.WM_LBUTTONUP = 0x0202
        self.WM_RBUTTONDOWN = 0x0204
        self.WM_RBUTTONUP = 0x0205
        self.WM_MBUTTONDOWN = 0x0207
        self.WM_MBUTTONUP = 0x0208
        self.WM_XBUTTONDOWN = 0x020B
        self.WM_XBUTTONUP = 0x020C
        
        # Setup Windows API types
        self.user32 = windll.user32
        self.kernel32 = windll.kernel32
        
        # Hook procedure type
        self.HOOKPROC = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_int, wintypes.WPARAM, wintypes.LPARAM)
        
        # Premium styling colors
        self.colors = {
            'primary': '#1e3d59',
            'success': '#27ae60',
            'warning': '#f39c12',
            'danger': '#e74c3c'
        }

    def start_blocking(self, buttons=None):
        """Start mouse button blocking with proper Windows API hooks"""
        if buttons:
            # Convert string button names to Windows message constants
            self.blocked_buttons = self._convert_button_names(buttons)
        
        try:
            self.is_active = True
            success = self._install_low_level_hook()
            
            if success:
                if self.logger:
                    button_names = self._get_blocked_button_names()
                    self.logger.log_activity("MOUSE_BLOCKING_STARTED", 
                                           f"Low-level mouse hook installed - Blocking: {', '.join(button_names)}")
                return True
            else:
                self.is_active = False
                if self.logger:
                    self.logger.log_activity("MOUSE_BLOCKING_ERROR", "Failed to install low-level mouse hook")
                return False
            
        except Exception as e:
            self.is_active = False
            if self.logger:
                self.logger.log_activity("MOUSE_BLOCKING_ERROR", f"Failed to start mouse blocking: {str(e)}")
            return False

    def stop_blocking(self):
        """Stop mouse button blocking and remove hooks"""
        try:
            self.is_active = False
            self._remove_low_level_hook()
            
            if self.logger:
                self.logger.log_activity("MOUSE_BLOCKING_STOPPED", "Low-level mouse hook removed - Mouse blocking deactivated")
            return True
            
        except Exception as e:
            if self.logger:
                self.logger.log_activity("MOUSE_BLOCKING_ERROR", f"Error stopping mouse blocking: {str(e)}")
            return False

    def _install_low_level_hook(self):
        """Install low-level mouse hook using Windows API"""
        try:
            # Create the hook procedure
            self.hook = self.HOOKPROC(self._low_level_mouse_proc)
            
            # Get module handle
            module_handle = self.kernel32.GetModuleHandleW(None)
            
            # Install the hook
            self.hook_id = self.user32.SetWindowsHookExW(
                self.WH_MOUSE_LL,  # Low-level mouse hook
                self.hook,         # Hook procedure
                module_handle,     # Module handle
                0                  # Thread ID (0 = all threads)
            )
            
            return self.hook_id is not None and self.hook_id != 0
            
        except Exception as e:
            if self.logger:
                self.logger.log_activity("HOOK_INSTALL_ERROR", f"Failed to install hook: {str(e)}")
            return False

    def _remove_low_level_hook(self):
        """Remove the low-level mouse hook"""
        try:
            if self.hook_id:
                result = self.user32.UnhookWindowsHookExW(self.hook_id)
                self.hook_id = None
                self.hook = None
                return result != 0
            return True
        except Exception as e:
            if self.logger:
                self.logger.log_activity("HOOK_REMOVE_ERROR", f"Error removing hook: {str(e)}")
            return False

    def _low_level_mouse_proc(self, nCode, wParam, lParam):
        """Low-level mouse hook procedure - this is where the actual blocking happens"""
        try:
            if nCode >= 0 and self.is_active:
                # Check if this is a blocked button message
                if wParam in self.blocked_buttons:
                    # Log the blocked action
                    if self.logger:
                        button_name = self._get_button_name_from_message(wParam)
                        self.logger.log_activity("MOUSE_BLOCKED", 
                                               f"Blocked {button_name} button action (Message: {hex(wParam)})")
                    
                    # Return 1 to block the message (don't pass it on)
                    return 1
            
            # Call next hook in chain for allowed messages
            return self.user32.CallNextHookEx(self.hook_id, nCode, wParam, lParam)
            
        except Exception as e:
            if self.logger:
                self.logger.log_activity("HOOK_PROC_ERROR", f"Error in hook procedure: {str(e)}")
            # On error, allow the message to pass through
            return self.user32.CallNextHookEx(self.hook_id, nCode, wParam, lParam)

    def _convert_button_names(self, button_names):
        """Convert button name strings to Windows message constants"""
        button_map = {
            'left': [self.WM_LBUTTONDOWN, self.WM_LBUTTONUP],
            'right': [self.WM_RBUTTONDOWN, self.WM_RBUTTONUP],
            'middle': [self.WM_MBUTTONDOWN, self.WM_MBUTTONUP],
            'x1': [self.WM_XBUTTONDOWN, self.WM_XBUTTONUP],
            'x2': [self.WM_XBUTTONDOWN, self.WM_XBUTTONUP],
            'custom': [self.WM_XBUTTONDOWN, self.WM_XBUTTONUP]
        }
        
        messages = []
        for button_name in button_names:
            if button_name.lower() in button_map:
                messages.extend(button_map[button_name.lower()])
        
        return messages

    def _get_blocked_button_names(self):
        """Get human-readable names of blocked buttons"""
        names = []
        if self.WM_LBUTTONDOWN in self.blocked_buttons:
            names.append('Left Click')
        if self.WM_RBUTTONDOWN in self.blocked_buttons:
            names.append('Right Click')
        if self.WM_MBUTTONDOWN in self.blocked_buttons:
            names.append('Middle Click')
        if self.WM_XBUTTONDOWN in self.blocked_buttons:
            names.append('Side Buttons (X1/X2)')
        return names

    def _get_button_name_from_message(self, message):
        """Get button name from Windows message constant"""
        message_map = {
            self.WM_LBUTTONDOWN: 'Left Button Down',
            self.WM_LBUTTONUP: 'Left Button Up',
            self.WM_RBUTTONDOWN: 'Right Button Down',
            self.WM_RBUTTONUP: 'Right Button Up',
            self.WM_MBUTTONDOWN: 'Middle Button Down',
            self.WM_MBUTTONUP: 'Middle Button Up',
            self.WM_XBUTTONDOWN: 'Side Button Down',
            self.WM_XBUTTONUP: 'Side Button Up'
        }
        return message_map.get(message, f'Unknown ({hex(message)})')

    def add_blocked_button(self, button):
        """Add a button to the blocked list"""
        new_messages = self._convert_button_names([button])
        for msg in new_messages:
            if msg not in self.blocked_buttons:
                self.blocked_buttons.append(msg)
        
        if self.logger:
            self.logger.log_activity("MOUSE_CONFIG", f"Added blocked button: {button}")

    def remove_blocked_button(self, button):
        """Remove a button from the blocked list"""
        messages_to_remove = self._convert_button_names([button])
        for msg in messages_to_remove:
            if msg in self.blocked_buttons:
                self.blocked_buttons.remove(msg)
        
        if self.logger:
            self.logger.log_activity("MOUSE_CONFIG", f"Removed blocked button: {button}")

    def block_all_buttons(self):
        """Block all mouse buttons"""
        self.blocked_buttons = [
            self.WM_LBUTTONDOWN, self.WM_LBUTTONUP,
            self.WM_RBUTTONDOWN, self.WM_RBUTTONUP,
            self.WM_MBUTTONDOWN, self.WM_MBUTTONUP,
            self.WM_XBUTTONDOWN, self.WM_XBUTTONUP
        ]
        if self.logger:
            self.logger.log_activity("MOUSE_CONFIG", "Blocked all mouse buttons")

    def allow_basic_clicks(self):
        """Allow left and right clicks, block others"""
        self.blocked_buttons = [
            self.WM_MBUTTONDOWN, self.WM_MBUTTONUP,
            self.WM_XBUTTONDOWN, self.WM_XBUTTONUP
        ]
        if self.logger:
            self.logger.log_activity("MOUSE_CONFIG", "Allowing basic clicks (left/right), blocking middle and side buttons")

    def get_status(self):
        """Get current mouse manager status with detailed information"""
        return {
            'active': self.is_active,
            'hook_installed': self.hook_id is not None,
            'hook_id': self.hook_id,
            'blocked_buttons': self._get_blocked_button_names(),
            'total_blocked_messages': len(self.blocked_buttons),
            'allows_left_click': self.WM_LBUTTONDOWN not in self.blocked_buttons,
            'allows_right_click': self.WM_RBUTTONDOWN not in self.blocked_buttons,
            'blocks_middle_click': self.WM_MBUTTONDOWN in self.blocked_buttons,
            'blocks_side_buttons': self.WM_XBUTTONDOWN in self.blocked_buttons
        }