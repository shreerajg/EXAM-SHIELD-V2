"""
Mouse Manager for Exam Shield Premium
Fixed version - Selective button blocking while allowing mouse movement
"""

import ctypes
from ctypes import wintypes, windll
import threading
import time
from pynput import mouse

# Windows API constants for low-level mouse hook
WH_MOUSE_LL = 14
WM_LBUTTONDOWN = 0x0201
WM_LBUTTONUP = 0x0202
WM_RBUTTONDOWN = 0x0204
WM_RBUTTONUP = 0x0205
WM_MBUTTONDOWN = 0x0207
WM_MBUTTONUP = 0x0208
WM_XBUTTONDOWN = 0x020B
WM_XBUTTONUP = 0x020C
HC_ACTION = 0

# Mouse button mappings
MOUSE_BUTTON_MAP = {
    'left': [WM_LBUTTONDOWN, WM_LBUTTONUP],
    'right': [WM_RBUTTONDOWN, WM_RBUTTONUP], 
    'middle': [WM_MBUTTONDOWN, WM_MBUTTONUP],
    'x1': [WM_XBUTTONDOWN, WM_XBUTTONUP],
    'x2': [WM_XBUTTONDOWN, WM_XBUTTONUP],
    'side': [WM_XBUTTONDOWN, WM_XBUTTONUP],
    'back': [WM_XBUTTONDOWN, WM_XBUTTONUP],
    'forward': [WM_XBUTTONDOWN, WM_XBUTTONUP]
}

class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]

class MSLLHOOKSTRUCT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long),
                ("y", ctypes.c_long), 
                ("mouseData", wintypes.DWORD),
                ("flags", wintypes.DWORD),
                ("time", wintypes.DWORD),
                ("dwExtraInfo", ctypes.POINTER(wintypes.ULONG))]

class MouseManager:
    def __init__(self, logger=None):
        self.logger = logger
        self.is_active = False
        self.blocked_buttons = ['middle', 'x1', 'x2']  # Default blocked buttons
        self.hook_installed = False
        self.mouse_listener = None
        self.block_all = False
        
        # Windows API setup for low-level hook
        self.user32 = windll.user32
        self.kernel32 = windll.kernel32
        self.hook_proc = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_int, wintypes.WPARAM, wintypes.LPARAM)
        self.hook_procedure = None
        self.hook_id = None
        
        # Premium styling colors for any UI elements
        self.colors = {
            'primary': '#1e3d59',
            'success': '#27ae60',
            'warning': '#f39c12',
            'danger': '#e74c3c'
        }

    def start_blocking(self, buttons=None):
        """Start selective mouse button blocking with premium error handling"""
        if buttons:
            self.blocked_buttons = buttons
        
        try:
            self.is_active = True
            self._setup_low_level_hook()
            
            if self.logger:
                self.logger.log_activity("MOUSE_BLOCKING_STARTED", 
                                       f"Selective mouse blocking activated for buttons: {', '.join(self.blocked_buttons)}")
            print(f"✅ Mouse blocking started - Blocked buttons: {', '.join(self.blocked_buttons)}")
            print("ℹ️ Mouse movement is still allowed, only specific buttons are blocked")
            return True
            
        except Exception as e:
            if self.logger:
                self.logger.log_activity("MOUSE_BLOCKING_ERROR", f"Failed to start mouse blocking: {str(e)}")
            print(f"❌ Mouse blocking error: {e}")
            return False

    def stop_blocking(self):
        """Stop mouse button blocking"""
        try:
            self.is_active = False
            self._remove_low_level_hook()
            
            if self.logger:
                self.logger.log_activity("MOUSE_BLOCKING_STOPPED", "Mouse blocking deactivated")
            print("✅ Mouse blocking stopped - All buttons restored")
            return True
            
        except Exception as e:
            if self.logger:
                self.logger.log_activity("MOUSE_BLOCKING_ERROR", f"Error stopping mouse blocking: {str(e)}")
            print(f"❌ Error stopping mouse blocking: {e}")
            return False

    def _setup_low_level_hook(self):
        """FIXED: Setup low-level Windows mouse hook for selective blocking"""
        try:
            # Define the hook procedure
            def low_level_mouse_proc(nCode, wParam, lParam):
                if nCode >= HC_ACTION and self.is_active:
                    # Check if this is a blocked button event
                    if self._is_blocked_event(wParam, lParam):
                        if self.logger:
                            button_name = self._get_button_name_from_event(wParam)
                            coords = self._get_mouse_coords(lParam)
                            self.logger.log_activity("MOUSE_BLOCKED", 
                                                   f"Blocked {button_name} button at ({coords[0]}, {coords[1]})")
                        print(f"🙫 Blocked mouse button: {self._get_button_name_from_event(wParam)}")
                        return 1  # Block the event
                
                # Allow all other mouse events (movement, allowed buttons)
                return self.user32.CallNextHookExW(self.hook_id, nCode, wParam, lParam)
            
            # Convert to proper hook procedure type
            self.hook_procedure = self.hook_proc(low_level_mouse_proc)
            
            # Install the hook
            self.hook_id = self.user32.SetWindowsHookExW(
                WH_MOUSE_LL,
                self.hook_procedure,
                self.kernel32.GetModuleHandleW(None),
                0
            )
            
            if not self.hook_id:
                raise Exception("Failed to install mouse hook")
                
            self.hook_installed = True
            print("✅ Low-level mouse hook installed successfully")
            
        except Exception as e:
            if self.logger:
                self.logger.log_activity("MOUSE_HOOK_ERROR", f"Failed to install mouse hook: {str(e)}")
            raise e

    def _remove_low_level_hook(self):
        """Remove low-level mouse hook safely"""
        try:
            if self.hook_id:
                self.user32.UnhookWindowsHookExW(self.hook_id)
                self.hook_id = None
                self.hook_procedure = None
                self.hook_installed = False
                print("✅ Mouse hook removed successfully")
        except Exception as e:
            if self.logger:
                self.logger.log_activity("MOUSE_HOOK_ERROR", f"Error removing mouse hook: {str(e)}")
            print(f"❌ Error removing mouse hook: {e}")

    def _is_blocked_event(self, wParam, lParam):
        """Check if the mouse event should be blocked"""
        if self.block_all:
            # Block all clicks but allow movement
            return wParam in [WM_LBUTTONDOWN, WM_RBUTTONDOWN, WM_MBUTTONDOWN, WM_XBUTTONDOWN]
            
        # Check each blocked button
        for button in self.blocked_buttons:
            if button.lower() in MOUSE_BUTTON_MAP:
                blocked_events = MOUSE_BUTTON_MAP[button.lower()]
                if wParam in blocked_events:
                    return True
                    
        return False

    def _get_button_name_from_event(self, wParam):
        """Get button name from Windows message"""
        event_map = {
            WM_LBUTTONDOWN: 'left',
            WM_LBUTTONUP: 'left',
            WM_RBUTTONDOWN: 'right', 
            WM_RBUTTONUP: 'right',
            WM_MBUTTONDOWN: 'middle',
            WM_MBUTTONUP: 'middle',
            WM_XBUTTONDOWN: 'side',
            WM_XBUTTONUP: 'side'
        }
        return event_map.get(wParam, 'unknown')

    def _get_mouse_coords(self, lParam):
        """Extract mouse coordinates from lParam"""
        try:
            # Cast lParam to MSLLHOOKSTRUCT pointer and extract coordinates
            hook_struct = ctypes.cast(lParam, ctypes.POINTER(MSLLHOOKSTRUCT)).contents
            return (hook_struct.x, hook_struct.y)
        except:
            return (0, 0)

    def set_block_all_clicks(self, block_all):
        """Set whether to block all mouse clicks"""
        self.block_all = block_all
        if self.logger:
            mode = "all clicks" if block_all else "selective buttons"
            self.logger.log_activity("MOUSE_CONFIG", f"Mouse blocking mode changed to: {mode}")
        print(f"⚙️ Mouse blocking mode: {'All clicks blocked' if block_all else 'Selective blocking'}")

    def add_blocked_button(self, button):
        """Add a button to the blocked list"""
        button_lower = button.lower()
        if button_lower not in [b.lower() for b in self.blocked_buttons]:
            self.blocked_buttons.append(button)
            if self.logger:
                self.logger.log_activity("MOUSE_CONFIG", f"Added blocked button: {button}")
            print(f"➕ Added blocked button: {button}")

    def remove_blocked_button(self, button):
        """Remove a button from the blocked list"""
        # Case-insensitive removal
        for b in self.blocked_buttons.copy():
            if b.lower() == button.lower():
                self.blocked_buttons.remove(b)
                if self.logger:
                    self.logger.log_activity("MOUSE_CONFIG", f"Removed blocked button: {button}")
                print(f"➖ Removed blocked button: {button}")
                break

    def get_status(self):
        """Get current mouse manager status with detailed info"""
        return {
            'active': self.is_active,
            'blocked_buttons': self.blocked_buttons,
            'hook_installed': self.hook_installed,
            'total_blocked': len(self.blocked_buttons),
            'block_all_mode': self.block_all,
            'hook_id': self.hook_id is not None
        }

    def test_blocking(self):
        """Test method to verify blocking is working"""
        print("🎯 Testing mouse blocking...")
        print(f"Blocked buttons: {', '.join(self.blocked_buttons)}")
        print(f"Block all mode: {self.block_all}")
        print(f"Hook active: {self.hook_installed}")
        print("ℹ️ Try clicking different mouse buttons to test blocking")