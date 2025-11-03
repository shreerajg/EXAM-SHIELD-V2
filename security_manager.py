"""
Security Manager for Exam Shield
Handles input blocking and security restrictions
FIXED: Proper manager initialization and integration
"""
import keyboard
import threading
import time
import psutil
from config import Config
from mouse_manager import MouseManager
from network_manager import NetworkManager
from window_manager import WindowManager

class SecurityManager:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.is_exam_mode = False
        self.blocked_keys = Config.BLOCKED_KEYS.copy()
        self.monitoring_thread = None
        self.hooks_active = False
        
        # NEW: Selective blocking flags
        self.selective_blocking = Config.SELECTIVE_BLOCKING.copy()
        
        # FIXED: Pass db_manager as logger to managers (they expect logger parameter)
        self.mouse_manager = MouseManager(logger=db_manager)
        self.network_manager = NetworkManager(logger=db_manager) 
        self.window_manager = WindowManager(logger=db_manager)
        
        # NEW: Admin panel reference for hotkey access
        self.admin_panel = None
        
        print("✅ Security Manager initialized with all components")
    
    def set_admin_panel(self, admin_panel):
        """Set reference to admin panel for hotkey access"""
        self.admin_panel = admin_panel
    
    def start_exam_mode(self, selective_options=None):
        """Start exam mode with optional selective blocking"""
        if self.is_exam_mode:
            return
            
        self.is_exam_mode = True
        
        # Update selective blocking if provided
        if selective_options:
            self.selective_blocking.update(selective_options)
        
        print(f"🔒 Starting selective exam mode with options: {selective_options}")
        
        # Start components based on selective blocking
        if self.selective_blocking.get('keyboard', True):
            print("🔤 Activating keyboard blocking...")
            self.setup_keyboard_hooks()
            
        if self.selective_blocking.get('processes', True):
            print("🔍 Activating process monitoring...")
            self.start_process_monitoring()
            
        if self.selective_blocking.get('mouse', True):
            print("🖱️ Activating mouse blocking...")
            success = self.mouse_manager.start_blocking()
            if success:
                print("✅ Mouse blocking activated successfully")
            else:
                print("❌ Mouse blocking failed to activate")
            
        if self.selective_blocking.get('internet', True) and Config.BLOCK_INTERNET:
            print("🌐 Activating internet blocking...")
            self.network_manager.start_blocking()
            
        if self.selective_blocking.get('windows', True):
            print("🪟 Activating window protection...")
            try:
                success = self.window_manager.start_window_protection()
                if success:
                    print("✅ Window protection activated successfully")
                else:
                    print("❌ Window protection failed to activate")
            except Exception as e:
                print(f"❌ Window protection error: {e}")
        
        # Log with selective options
        active_blocks = [k for k, v in self.selective_blocking.items() if v]
        self.db_manager.log_activity("EXAM_MODE_START", f"Selective restrictions: {', '.join(active_blocks)}")
        print(f"🔒 Selective exam mode activated - Active: {', '.join(active_blocks)}")

    def stop_exam_mode(self):
        """Stop exam mode and deactivate all security components"""
        if not self.is_exam_mode:
            return
            
        print("🔓 Stopping exam mode - Deactivating all components...")
        
        self.is_exam_mode = False
        
        # Stop all components safely
        try:
            self.remove_keyboard_hooks()
        except Exception as e:
            print(f"Error stopping keyboard hooks: {e}")
            
        try:
            self.stop_process_monitoring()
        except Exception as e:
            print(f"Error stopping process monitoring: {e}")
            
        try:
            self.mouse_manager.stop_blocking()
        except Exception as e:
            print(f"Error stopping mouse blocking: {e}")
            
        try:
            self.network_manager.stop_blocking()
        except Exception as e:
            print(f"Error stopping network blocking: {e}")
            
        try:
            self.window_manager.stop_window_protection()
        except Exception as e:
            print(f"Error stopping window protection: {e}")
        
        self.db_manager.log_activity("EXAM_MODE_STOP", "All security restrictions deactivated")
        print("🔓 Full exam mode deactivated - All restrictions removed")

    def setup_keyboard_hooks(self):
        """Setup keyboard hooks with proper error handling"""
        try:
            for key_combo in self.blocked_keys:
                keyboard.add_hotkey(key_combo, self.block_key_action, args=(key_combo,), suppress=True)
            
            # FIXED: Properly register admin access hotkey
            keyboard.add_hotkey(Config.ADMIN_ACCESS_KEY, self.admin_access_requested, suppress=False)
            
            self.hooks_active = True
            print("✅ Keyboard hooks activated")
        except Exception as e:
            print(f"❌ Error setting up keyboard hooks: {e}")
            self.hooks_active = False

    def remove_keyboard_hooks(self):
        """Remove keyboard hooks safely"""
        try:
            keyboard.unhook_all()
            self.hooks_active = False
            print("✅ Keyboard hooks removed")
        except Exception as e:
            print(f"❌ Error removing keyboard hooks: {e}")

    def block_key_action(self, key_combo):
        """Handle blocked key combinations"""
        if self.is_exam_mode:
            self.db_manager.log_activity("BLOCKED_KEY_ATTEMPT", f"Attempted to use: {key_combo}", blocked=True)
            print(f"🚫 Blocked key combination: {key_combo}")

    def admin_access_requested(self):
        """FIXED: Properly handle admin access request"""
        print("🔑 Admin access requested via hotkey")
        self.db_manager.log_activity("ADMIN_ACCESS_REQUEST", "Admin hotkey pressed")
        
        # Show admin panel if available
        if self.admin_panel:
            try:
                self.admin_panel.show()
                print("✅ Admin panel shown")
            except Exception as e:
                print(f"❌ Error showing admin panel: {e}")

    def start_process_monitoring(self):
        """Start process monitoring thread"""
        if self.monitoring_thread and self.monitoring_thread.is_alive():
            return
        self.monitoring_thread = threading.Thread(target=self._monitor_processes, daemon=True)
        self.monitoring_thread.start()
        print("✅ Process monitoring started")

    def stop_process_monitoring(self):
        """Stop process monitoring thread"""
        if self.monitoring_thread:
            self.monitoring_thread = None
            print("✅ Process monitoring stopped")

    def _monitor_processes(self):
        """Monitor for suspicious processes"""
        suspicious_processes = ['taskmgr.exe', 'cmd.exe', 'powershell.exe', 'regedit.exe', 'msconfig.exe']
        print("🔍 Process monitoring active")
        
        while self.is_exam_mode and self.monitoring_thread:
            try:
                for process in psutil.process_iter(['pid', 'name']):
                    try:
                        if process.info['name'].lower() in suspicious_processes:
                            self.db_manager.log_activity("SUSPICIOUS_PROCESS", f"Detected: {process.info['name']}", blocked=True)
                            try:
                                process.terminate()
                                print(f"🚫 Terminated suspicious process: {process.info['name']}")
                            except:
                                pass
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue
                time.sleep(2)
            except Exception as e:
                print(f"Process monitoring error: {e}")
                time.sleep(5)

    def add_blocked_key(self, key_combo):
        """Add a new blocked key combination"""
        if key_combo not in self.blocked_keys:
            self.blocked_keys.append(key_combo)
            if self.hooks_active:
                try:
                    keyboard.add_hotkey(key_combo, self.block_key_action, args=(key_combo,), suppress=True)
                    print(f"✅ Added blocked key: {key_combo}")
                except Exception as e:
                    print(f"❌ Error adding key {key_combo}: {e}")

    def remove_blocked_key(self, key_combo):
        """Remove a blocked key combination"""
        if key_combo in self.blocked_keys:
            self.blocked_keys.remove(key_combo)
            print(f"✅ Removed blocked key: {key_combo}")

    def get_system_info(self):
        """Get comprehensive system information for status display"""
        try:
            info = {
                'cpu_percent': psutil.cpu_percent(interval=0.1),
                'memory_percent': psutil.virtual_memory().percent,
                'active_processes': len(psutil.pids()),
                'exam_mode': self.is_exam_mode,
                'hooks_active': self.hooks_active,
                'mouse_blocking': self.mouse_manager.is_active if self.mouse_manager else False,
                'internet_blocked': self.network_manager.is_blocked if self.network_manager else False,
                'window_protection': self.window_manager.is_active if self.window_manager else False
            }
            return info
        except Exception as e:
            print(f"Error getting system info: {e}")
            return {
                'cpu_percent': 0,
                'memory_percent': 0,
                'active_processes': 0,
                'exam_mode': self.is_exam_mode,
                'hooks_active': self.hooks_active,
                'mouse_blocking': False,
                'internet_blocked': False,
                'window_protection': False
            }
    
    # NEW: Individual component controls for admin panel
    def toggle_mouse_blocking(self, enable):
        """Toggle mouse blocking on/off"""
        try:
            if enable:
                success = self.mouse_manager.start_blocking()
                print(f"🖱️ Mouse blocking {'enabled' if success else 'failed'}")
                return success
            else:
                success = self.mouse_manager.stop_blocking()
                print(f"🖱️ Mouse blocking {'disabled' if success else 'failed to disable'}")
                return success
        except Exception as e:
            print(f"❌ Mouse blocking toggle error: {e}")
            return False
    
    def toggle_window_protection(self, enable):
        """Toggle window protection on/off"""
        try:
            if enable:
                success = self.window_manager.start_window_protection()
                print(f"🪟 Window protection {'enabled' if success else 'failed'}")
                return success
            else:
                success = self.window_manager.stop_window_protection()
                print(f"🪟 Window protection {'disabled' if success else 'failed to disable'}")
                return success
        except Exception as e:
            print(f"❌ Window protection toggle error: {e}")
            return False
    
    def toggle_internet_blocking(self, enable):
        """Toggle internet blocking on/off"""
        try:
            if enable:
                success = self.network_manager.start_blocking()
                print(f"🌐 Internet blocking {'enabled' if success else 'failed'}")
                return success
            else:
                success = self.network_manager.stop_blocking()
                print(f"🌐 Internet blocking {'disabled' if success else 'failed to disable'}")
                return success
        except Exception as e:
            print(f"❌ Internet blocking toggle error: {e}")
            return False