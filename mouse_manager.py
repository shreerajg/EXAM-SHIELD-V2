"""
Mouse Manager for Exam Shield Premium
Fixed version with proper low-level Windows mouse hook for actual button blocking
"""

import ctypes
from ctypes import wintypes, windll, Structure, POINTER, byref
import threading
import time

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
WM_MOUSEWHEEL = 0x020A
WM_MOUSEHWHEEL = 0x020E
HC_ACTION = 0

# Mouse data constants
XBUTTON1 = 0x0001
XBUTTON2 = 0x0002

class POINT(Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]

class MSLLHOOKSTRUCT(Structure):
    _fields_ = [("x", ctypes.c_long),
                ("y", ctypes.c_long), 
                ("mouseData", wintypes.DWORD),
                ("flags", wintypes.DWORD),
                ("time", wintypes.DWORD),
                ("dwExtraInfo", POINTER(wintypes.ULONG))]

class MouseManager:
    def __init__(self, logger=None):
        self.logger = logger
        self.is_active = False
        self.blocked_buttons = ['middle', 'x1', 'x2']  # Default blocked buttons
        self.hook_installed = False
        self.block_all_clicks = False
        
        # Windows API setup
        self.user32 = windll.user32
        self.kernel32 = windll.kernel32
        self.hook_proc = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_int, wintypes.WPARAM, wintypes.LPARAM)
        self.hook_procedure = None
        self.hook_id = None
        
        # Button mapping for easier reference
        self.button_map = {
            'left': [WM_LBUTTONDOWN, WM_LBUTTONUP],
            'right': [WM_RBUTTONDOWN, WM_RBUTTONUP], 
            'middle': [WM_MBUTTONDOWN, WM_MBUTTONUP],
            'x1': [WM_XBUTTONDOWN, WM_XBUTTONUP],
            'x2': [WM_XBUTTONDOWN, WM_XBUTTONUP],
            'side': [WM_XBUTTONDOWN, WM_XBUTTONUP],
            'back': [WM_XBUTTONDOWN, WM_XBUTTONUP],
            'forward': [WM_XBUTTONDOWN, WM_XBUTTONUP]
        }
        
        # Premium styling colors
        self.colors = {
            'primary': '#1e3d59',
            'success': '#27ae60',
            'warning': '#f39c12',
            'danger': '#e74c3c'
        }

    def start_blocking(self, buttons=None):
        """Start mouse button blocking with low-level Windows hook"""
        if buttons:
            self.blocked_buttons = [btn.lower() for btn in buttons]
        
        try:
            self.is_active = True
            self._install_mouse_hook()
            
            if self.logger:
                self.logger.log_activity("MOUSE_BLOCKING_STARTED", 
                                       f"Low-level mouse blocking activated for: {', '.join(self.blocked_buttons)}")
            print(f"🔒 Mouse blocking activated for buttons: {', '.join(self.blocked_buttons)}")
            print("ℹ️ Mouse movement and scrolling remain unaffected")
            return True
            
        except Exception as e:
            if self.logger:
                self.logger.log_activity("MOUSE_BLOCKING_ERROR", f"Failed to start mouse blocking: {str(e)}")
            print(f"❌ Mouse blocking failed: {e}")
            return False

    def stop_blocking(self):
        """Stop mouse button blocking"""
        try:
            self.is_active = False
            self._uninstall_mouse_hook()
            
            if self.logger:
                self.logger.log_activity("MOUSE_BLOCKING_STOPPED", "Mouse blocking deactivated")
            print("✅ Mouse blocking stopped - All buttons restored")
            return True
            
        except Exception as e:
            if self.logger:
                self.logger.log_activity("MOUSE_BLOCKING_ERROR", f"Error stopping mouse blocking: {str(e)}")
            print(f"❌ Error stopping mouse blocking: {e}")
            return False

    def _install_mouse_hook(self):
        """Install Windows low-level mouse hook"""
        try:
            # Define the hook procedure
            def low_level_mouse_proc(nCode, wParam, lParam):
                if nCode >= HC_ACTION and self.is_active:
                    try:
                        # Get mouse event information
                        hook_struct = ctypes.cast(lParam, POINTER(MSLLHOOKSTRUCT)).contents
                        x, y = hook_struct.x, hook_struct.y
                        
                        # Check if this event should be blocked
                        if self._should_block_event(wParam, hook_struct):
                            button_name = self._get_button_name(wParam, hook_struct)
                            if self.logger:
                                self.logger.log_activity("MOUSE_BLOCKED", 
                                                       f"Blocked {button_name} at ({x}, {y})")
                            print(f"🚫 Blocked {button_name} mouse button at ({x}, {y})")
                            return 1  # Block the event
                    except Exception as e:
                        print(f"Hook procedure error: {e}")
                        pass
                
                # Allow all other events (movement, allowed buttons, etc.)
                return self.user32.CallNextHookExW(self.hook_id, nCode, wParam, lParam)
            
            # Set up the hook
            self.hook_procedure = self.hook_proc(low_level_mouse_proc)
            
            # Install the hook
            self.hook_id = self.user32.SetWindowsHookExW(
                WH_MOUSE_LL,
                self.hook_procedure,
                self.kernel32.GetModuleHandleW(None),
                0
            )
            
            if not self.hook_id:
                error = self.kernel32.GetLastError()
                raise Exception(f"SetWindowsHookExW failed with error code: {error}")
            
            self.hook_installed = True
            print("✅ Low-level mouse hook installed successfully")
            
        except Exception as e:
            print(f"❌ Failed to install mouse hook: {e}")
            raise e

    def _uninstall_mouse_hook(self):
        """Uninstall the mouse hook"""
        try:
            if self.hook_id:
                result = self.user32.UnhookWindowsHookExW(self.hook_id)
                if not result:
                    print("⚠️ Warning: UnhookWindowsHookExW returned False")
                self.hook_id = None
                self.hook_procedure = None
                self.hook_installed = False
                print("✅ Mouse hook uninstalled successfully")
        except Exception as e:
            print(f"❌ Error uninstalling mouse hook: {e}")

    def _should_block_event(self, wParam, hook_struct):
        """Check if the mouse event should be blocked"""
        # If block all clicks is enabled, block all click events but allow movement
        if self.block_all_clicks:
            click_events = [WM_LBUTTONDOWN, WM_RBUTTONDOWN, WM_MBUTTONDOWN, WM_XBUTTONDOWN]
            return wParam in click_events
        
        # Check specific button blocking
        for button in self.blocked_buttons:
            button_lower = button.lower()
            
            if button_lower == 'left' and wParam in [WM_LBUTTONDOWN, WM_LBUTTONUP]:
                return True
            elif button_lower == 'right' and wParam in [WM_RBUTTONDOWN, WM_RBUTTONUP]:
                return True
            elif button_lower == 'middle' and wParam in [WM_MBUTTONDOWN, WM_MBUTTONUP]:
                return True
            elif button_lower in ['x1', 'side', 'back'] and wParam in [WM_XBUTTONDOWN, WM_XBUTTONUP]:
                # Check if it's specifically X1 button
                mouse_data = hook_struct.mouseData >> 16
                if mouse_data == XBUTTON1:
                    return True
            elif button_lower in ['x2', 'forward'] and wParam in [WM_XBUTTONDOWN, WM_XBUTTONUP]:
                # Check if it's specifically X2 button
                mouse_data = hook_struct.mouseData >> 16
                if mouse_data == XBUTTON2:
                    return True
        
        return False

    def _get_button_name(self, wParam, hook_struct):
        """Get the name of the button from the event"""
        if wParam in [WM_LBUTTONDOWN, WM_LBUTTONUP]:
            return "left"
        elif wParam in [WM_RBUTTONDOWN, WM_RBUTTONUP]:
            return "right"
        elif wParam in [WM_MBUTTONDOWN, WM_MBUTTONUP]:
            return "middle"
        elif wParam in [WM_XBUTTONDOWN, WM_XBUTTONUP]:
            mouse_data = hook_struct.mouseData >> 16
            if mouse_data == XBUTTON1:
                return "x1/back"
            elif mouse_data == XBUTTON2:
                return "x2/forward"
            else:
                return "side"
        else:
            return "unknown"

    def set_block_all_clicks(self, block_all):
        """Enable or disable blocking all mouse clicks"""
        self.block_all_clicks = block_all
        if self.logger:
            status = "enabled" if block_all else "disabled"
            self.logger.log_activity("MOUSE_CONFIG", f"Block all clicks: {status}")
        print(f"🔧 Block all clicks: {'enabled' if block_all else 'disabled'}")

    def add_blocked_button(self, button):
        """Add a button to the blocked list"""
        button_lower = button.lower()
        if button_lower not in self.blocked_buttons:
            self.blocked_buttons.append(button_lower)
            if self.logger:
                self.logger.log_activity("MOUSE_CONFIG", f"Added blocked button: {button_lower}")
            print(f"➕ Added blocked button: {button_lower}")

    def remove_blocked_button(self, button):
        """Remove a button from the blocked list"""
        button_lower = button.lower()
        if button_lower in self.blocked_buttons:
            self.blocked_buttons.remove(button_lower)
            if self.logger:
                self.logger.log_activity("MOUSE_CONFIG", f"Removed blocked button: {button_lower}")
            print(f"➖ Removed blocked button: {button_lower}")

    def test_blocking(self):
        """Test the mouse blocking functionality"""
        if not self.is_active:
            print("⚠️ Mouse blocking is not active. Start blocking first.")
            return
        
        print("\n🧪 MOUSE BLOCKING TEST")
        print("=" * 40)
        print(f"Active: {self.is_active}")
        print(f"Hook installed: {self.hook_installed}")
        print(f"Block all clicks: {self.block_all_clicks}")
        print(f"Blocked buttons: {', '.join(self.blocked_buttons)}")
        print("\n📝 Test Instructions:")
        print("- Mouse movement should work normally")
        print("- Mouse wheel scrolling should work normally")
        print(f"- These buttons should be BLOCKED: {', '.join(self.blocked_buttons)}")
        print("- Other buttons should work normally")
        print("\n🎯 Try clicking different mouse buttons to test!")

    def get_status(self):
        """Get current mouse manager status"""
        return {
            'active': self.is_active,
            'blocked_buttons': self.blocked_buttons,
            'hook_installed': self.hook_installed,
            'block_all_clicks': self.block_all_clicks,
            'total_blocked': len(self.blocked_buttons),
            'hook_id': self.hook_id is not None
        }

    def __del__(self):
        """Cleanup when object is destroyed"""
        try:
            if self.hook_id:
                self._uninstall_mouse_hook()
        except:
            pass