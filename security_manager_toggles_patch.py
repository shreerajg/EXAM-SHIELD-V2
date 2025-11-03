"""
Security Manager for Exam Shield
Adds missing toggle methods used by AdminPanel
"""

from security_manager import SecurityManager as _SM

# Add missing toggle methods if not present

def _toggle_mouse_blocking(self, enable: bool):
    try:
        if enable:
            return bool(self.mouse_manager.start_blocking())
        else:
            return bool(self.mouse_manager.stop_blocking())
    except Exception as e:
        print(f"Mouse toggle error: {e}")
        return False


def _toggle_window_protection(self, enable: bool):
    try:
        if enable:
            return bool(self.window_manager.start_window_protection())
        else:
            return bool(self.window_manager.stop_window_protection())
    except Exception as e:
        print(f"Window toggle error: {e}")
        return False


def _toggle_internet_blocking(self, enable: bool):
    try:
        if enable:
            self.network_manager.start_blocking(); return True
        else:
            self.network_manager.stop_blocking(); return True
    except Exception as e:
        print(f"Network toggle error: {e}")
        return False

# Only attach if attributes are missing
if not hasattr(_SM, 'toggle_mouse_blocking'):
    _SM.toggle_mouse_blocking = _toggle_mouse_blocking
if not hasattr(_SM, 'toggle_window_protection'):
    _SM.toggle_window_protection = _toggle_window_protection
if not hasattr(_SM, 'toggle_internet_blocking'):
    _SM.toggle_internet_blocking = _toggle_internet_blocking
