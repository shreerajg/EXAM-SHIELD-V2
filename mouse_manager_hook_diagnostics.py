"""
Improve diagnostics for mouse hook installation failures
"""

from mouse_manager import MouseManager as _MM
import ctypes
from ctypes import windll

_user32 = windll.user32
_kernel32 = windll.kernel32

_original = _MM._install_low_level_hook


def _install_with_error_logging(self):
    try:
        ok = _original(self)
        if not ok:
            err = _kernel32.GetLastError()
            if self.logger:
                self.logger.log_activity("HOOK_INSTALL_ERROR", f"SetWindowsHookEx failed, GetLastError={err}")
            print(f"[MouseManager] SetWindowsHookEx failed, GetLastError={err}")
        return ok
    except Exception as e:
        if self.logger:
            self.logger.log_activity("HOOK_INSTALL_ERROR", f"Exception during hook install: {e}")
        print(f"[MouseManager] Exception during hook install: {e}")
        return False

_MM._install_low_level_hook = _install_with_error_logging
