"""
Mouse Manager: ensure low-level hook stays active with a message pump thread
"""

from mouse_manager import MouseManager as _MM
import threading
import time
import ctypes
from ctypes import windll

_user32 = windll.user32


def _ensure_message_pump(self):
    # Run a minimal message loop so WH_MOUSE_LL stays alive
    msg = ctypes.wintypes.MSG()
    while self.is_active and self.hook_id:
        _user32.PeekMessageW(ctypes.byref(msg), 0, 0, 0, 1)
        time.sleep(0.01)


def _install_low_level_hook_with_pump(self):
    ok = self.__original_install_hook__()
    if ok and (self._pump_thread is None or not self._pump_thread.is_alive()):
        self._pump_thread = threading.Thread(target=self._message_pump, daemon=True)
        self._pump_thread.start()
    return ok

# Attach pump helpers if not present
if not hasattr(_MM, '_message_pump'):
    _MM._message_pump = _ensure_message_pump
    _MM._pump_thread = None
    _MM.__original_install_hook__ = _MM._install_low_level_hook
    _MM._install_low_level_hook = _install_low_level_hook_with_pump
