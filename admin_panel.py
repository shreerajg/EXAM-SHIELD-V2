"""
Admin Panel for Exam Shield - ENHANCED WITH SELECTIVE CONTROLS
Stable build: fixes on_close and control dialogs
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, simpledialog
import threading
import json
from datetime import datetime
import keyboard
from pynput import mouse

class AdminPanel:
    def __init__(self, db_manager, security_manager, parent_window):
        self.db_manager = db_manager
        self.security_manager = security_manager
        self.parent_window = parent_window
        self.security_manager.set_admin_panel(self)

        self.detecting_key = False
        self.detecting_mouse = False
        self.detected_key = None
        self.mouse_listener = None

        self.window = tk.Toplevel()
        self.window.title("Exam Shield Premium - Admin Panel v2.0")
        self.window.geometry("950x750")
        self.window.resizable(True, True)

        self.colors = {
            'primary': '#1e3d59','secondary': '#17223b','accent': '#ffc947','success': '#27ae60',
            'warning': '#f39c12','danger': '#e74c3c','info': '#3498db','surface': '#f8f9fa',
            'card': '#ffffff','text_primary': '#2c3e50','text_secondary': '#7f8c8d'
        }
        self.window.configure(bg=self.colors['surface'])

        self.setup_window()
        self.setup_ui()
        self.start_auto_refresh()

    # ===== Window lifecycle =====
    def setup_window(self):
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - 475
        y = (self.window.winfo_screenheight() // 2) - 375
        self.window.geometry(f"950x750+{x}+{y}")
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        try:
            # Keep app running, just hide panel
            self.window.withdraw()
        except Exception as e:
            try:
                messagebox.showerror("Error", f"Failed to close panel: {e}")
            finally:
                self.window.withdraw()

    def show(self):
        self.window.deiconify()
        self.window.lift()
        self.refresh_status()

    # ===== UI =====
    def setup_ui(self):
        style = ttk.Style(); style.theme_use('clam')
        style.configure('TNotebook', background=self.colors['surface'])
        style.configure('TNotebook.Tab', padding=[15, 8], font=('Segoe UI', 10, 'bold'))

        header_frame = tk.Frame(self.window, bg=self.colors['primary'], height=60)
        header_frame.pack(fill=tk.X); header_frame.pack_propagate(False)
        hc = tk.Frame(header_frame, bg=self.colors['primary']); hc.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        tk.Label(hc, text="🛡️ EXAM SHIELD PREMIUM", font=("Segoe UI", 16, "bold"), bg=self.colors['primary'], fg=self.colors['card']).pack(side=tk.LEFT)
        tk.Label(hc, text="v2.0 Administrative Control Center", font=("Segoe UI", 9), bg=self.colors['primary'], fg=self.colors['accent']).pack(side=tk.RIGHT)

        self.notebook = ttk.Notebook(self.window); self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.create_control_tab(); self.create_monitoring_tab(); self.create_settings_tab(); self.create_logs_tab()

    def create_control_tab(self):
        frame = ttk.Frame(self.notebook); self.notebook.add(frame, text="📋 Control Center")
        main = tk.Frame(frame, bg=self.colors['surface']); main.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Status
        status_card = tk.Frame(main, bg=self.colors['card']); status_card.pack(fill=tk.X, pady=(0,10))
        sh = tk.Frame(status_card, bg=self.colors['info'], height=40); sh.pack(fill=tk.X); sh.pack_propagate(False)
        tk.Label(sh, text="📊 System Status", font=("Segoe UI", 12, "bold"), bg=self.colors['info'], fg=self.colors['card']).pack(pady=10)
        sc = tk.Frame(status_card, bg=self.colors['card']); sc.pack(fill=tk.X, padx=15, pady=15)
        self.status_label = tk.Label(sc, text="🔓 Exam Mode: INACTIVE", font=("Segoe UI", 14, "bold"), bg=self.colors['card'], fg=self.colors['success']); self.status_label.pack(anchor=tk.W)
        self.system_info_label = tk.Label(sc, text="System Info Loading...", font=("Segoe UI", 10), bg=self.colors['card'], fg=self.colors['text_secondary']); self.system_info_label.pack(anchor=tk.W, pady=(5,0))
        ind = tk.Frame(sc, bg=self.colors['card']); ind.pack(anchor=tk.W, pady=(5,0), fill=tk.X)
        tk.Label(ind, text="Security Modules:", font=("Segoe UI", 10, "bold"), bg=self.colors['card'], fg=self.colors['text_primary']).pack(anchor=tk.W)
        row = tk.Frame(ind, bg=self.colors['card']); row.pack(anchor=tk.W, pady=(2,0))
        self.keyboard_status = tk.Label(row, text="⚫ Keyboard", font=("Segoe UI", 9), bg=self.colors['card'], fg=self.colors['text_secondary']); self.keyboard_status.pack(side=tk.LEFT, padx=(0,15))
        self.mouse_status = tk.Label(row, text="⚫ Mouse", font=("Segoe UI", 9), bg=self.colors['card'], fg=self.colors['text_secondary']); self.mouse_status.pack(side=tk.LEFT, padx=(0,15))
        self.network_status = tk.Label(row, text="⚫ Network", font=("Segoe UI", 9), bg=self.colors['card'], fg=self.colors['text_secondary']); self.network_status.pack(side=tk.LEFT, padx=(0,15))
        self.window_status = tk.Label(row, text="⚫ Windows", font=("Segoe UI", 9), bg=self.colors['card'], fg=self.colors['text_secondary']); self.window_status.pack(side=tk.LEFT, padx=(0,15))

        # Controls
        card = tk.Frame(main, bg=self.colors['card']); card.pack(fill=tk.X, pady=(0,10))
        ch = tk.Frame(card, bg=self.colors['primary'], height=40); ch.pack(fill=tk.X); ch.pack_propagate(False)
        tk.Label(ch, text="🎯 Exam Controls", font=("Segoe UI", 12, "bold"), bg=self.colors['primary'], fg=self.colors['card']).pack(pady=10)
        btns = tk.Frame(card, bg=self.colors['card']); btns.pack(fill=tk.X, padx=15, pady=15)
        self.start_btn = tk.Button(btns, text="🔒 START SELECTIVE LOCKDOWN", command=self.show_selective_lockdown_dialog, bg=self.colors['primary'], fg=self.colors['card'], font=("Segoe UI", 11, "bold"), relief=tk.FLAT, cursor='hand2', padx=20, pady=10); self.start_btn.pack(side=tk.LEFT, padx=(0,10))
        self.stop_btn = tk.Button(btns, text="🔓 END LOCKDOWN MODE", command=self.stop_exam_mode, state=tk.DISABLED, bg=self.colors['warning'], fg=self.colors['card'], font=("Segoe UI", 11, "bold"), relief=tk.FLAT, cursor='hand2', padx=20, pady=10); self.stop_btn.pack(side=tk.LEFT, padx=(0,10))
        tk.Button(btns, text="🚨 EMERGENCY STOP", command=self.emergency_stop, bg=self.colors['danger'], fg=self.colors['card'], font=("Segoe UI", 11, "bold"), relief=tk.FLAT, cursor='hand2', padx=20, pady=10).pack(side=tk.RIGHT)

        self.create_individual_controls(main)

    def create_individual_controls(self, parent):
        card = tk.Frame(parent, bg=self.colors['card']); card.pack(fill=tk.X, pady=(0,10))
        ch = tk.Frame(card, bg=self.colors['secondary'], height=40); ch.pack(fill=tk.X); ch.pack_propagate(False)
        tk.Label(ch, text="🛠️ Individual Security Controls", font=("Segoe UI", 12, "bold"), bg=self.colors['secondary'], fg=self.colors['card']).pack(pady=10)
        cont = tk.Frame(card, bg=self.colors['card']); cont.pack(fill=tk.X, padx=15, pady=15)
        row1 = tk.Frame(cont, bg=self.colors['card']); row1.pack(fill=tk.X, pady=(0,5))
        tk.Button(row1, text="🖱️ Mouse Blocker", command=self.show_mouse_controls, bg=self.colors['info'], fg=self.colors['card'], font=("Segoe UI", 10, "bold"), relief=tk.FLAT, cursor='hand2', padx=15, pady=8).pack(side=tk.LEFT, padx=(0,10))
        tk.Button(row1, text="🌐 Internet Blocker", command=self.show_network_controls, bg=self.colors['info'], fg=self.colors['card'], font=("Segoe UI", 10, "bold"), relief=tk.FLAT, cursor='hand2', padx=15, pady=8).pack(side=tk.LEFT, padx=(0,10))
        tk.Button(row1, text="🪟 Window Guardian", command=self.show_window_controls, bg=self.colors['info'], fg=self.colors['card'], font=("Segoe UI", 10, "bold"), relief=tk.FLAT, cursor='hand2', padx=15, pady=8).pack(side=tk.LEFT)

    # ===== Mouse Controls (stable) =====
    def show_mouse_controls(self):
        win = tk.Toplevel(self.window); win.title("🖱️ Mouse Security Controls"); win.geometry("600x500"); win.configure(bg=self.colors['surface']); win.transient(self.window)
        win.update_idletasks(); x = (win.winfo_screenwidth() // 2) - 300; y = (win.winfo_screenheight() // 2) - 250; win.geometry(f"600x500+{x}+{y}")
        header = tk.Frame(win, bg=self.colors['info'], height=60); header.pack(fill=tk.X); header.pack_propagate(False)
        tk.Label(header, text="🖱️ Mouse Button Blocking System", font=("Segoe UI", 14, "bold"), bg=self.colors['info'], fg=self.colors['card']).pack(pady=20)
        content = tk.Frame(win, bg=self.colors['surface']); content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        status_frame = tk.Frame(content, bg=self.colors['card'], pady=15); status_frame.pack(fill=tk.X, pady=(0,20))
        is_active = self.security_manager.mouse_manager.is_active; status_text = "🟢 ACTIVE" if is_active else "🔴 INACTIVE"; status_color = self.colors['success'] if is_active else self.colors['danger']
        tk.Label(status_frame, text=f"Status: {status_text}", font=("Segoe UI", 12, "bold"), bg=self.colors['card'], fg=status_color).pack(pady=10)
        try:
            info = self.security_manager.mouse_manager.get_status(); blocked = info.get('blocked_buttons', [])
            if isinstance(blocked, list):
                blocked_text = ", ".join(blocked)
            else:
                blocked_text = str(blocked)
        except Exception:
            blocked_text = "Unavailable"
        tk.Label(status_frame, text=f"Blocked Buttons: {blocked_text}", font=("Segoe UI", 10), bg=self.colors['card'], fg=self.colors['text_primary']).pack(pady=5)
        ctrl = tk.Frame(content, bg=self.colors['card'], pady=20); ctrl.pack(fill=tk.X, pady=(0,20))
        if not is_active:
            tk.Button(ctrl, text="🚀 Activate Mouse Blocking", command=lambda: self._toggle_mouse_and_close(True, win), bg=self.colors['success'], fg=self.colors['card'], font=("Segoe UI", 11, "bold"), relief=tk.FLAT, cursor='hand2', padx=20, pady=10).pack(pady=10)
        else:
            tk.Button(ctrl, text="🛑 Deactivate Mouse Blocking", command=lambda: self._toggle_mouse_and_close(False, win), bg=self.colors['danger'], fg=self.colors['card'], font=("Segoe UI", 11, "bold"), relief=tk.FLAT, cursor='hand2', padx=20, pady=10).pack(pady=10)
        settings = tk.Frame(content, bg=self.colors['card'], pady=15); settings.pack(fill=tk.BOTH, expand=True)
        tk.Label(settings, text="Quick Settings:", font=("Segoe UI", 11, "bold"), bg=self.colors['card'], fg=self.colors['text_primary']).pack(anchor=tk.W, pady=(0,10))
        btns = tk.Frame(settings, bg=self.colors['card']); btns.pack(fill=tk.X, pady=5)
        tk.Button(btns, text="Allow Basic Clicks Only", command=lambda: self._apply_mouse_setting('basic'), bg=self.colors['primary'], fg=self.colors['card'], font=("Segoe UI", 9, "bold"), relief=tk.FLAT, cursor='hand2', padx=15, pady=8).pack(side=tk.LEFT, padx=(0,10))
        tk.Button(btns, text="Block All Buttons", command=lambda: self._apply_mouse_setting('all'), bg=self.colors['warning'], fg=self.colors['card'], font=("Segoe UI", 9, "bold"), relief=tk.FLAT, cursor='hand2', padx=15, pady=8).pack(side=tk.LEFT, padx=(0,10))
        tk.Button(content, text="Close", command=win.destroy, bg=self.colors['secondary'], fg=self.colors['card'], font=("Segoe UI", 10, "bold"), relief=tk.FLAT, cursor='hand2', padx=20, pady=8).pack(pady=20)

    def _toggle_mouse_and_close(self, enable, window):
        try:
            ok = self.security_manager.toggle_mouse_blocking(enable); action = "activated" if enable else "deactivated"
            messagebox.showinfo("✅ Success", f"Mouse blocking {action} successfully!") if ok else messagebox.showerror("❌ Error", f"Failed to {action.replace('ed','')} mouse blocking.")
        finally:
            window.destroy(); self.refresh_status()

    def _apply_mouse_setting(self, t):
        try:
            if t == 'basic': self.security_manager.mouse_manager.allow_basic_clicks(); messagebox.showinfo("✅ Applied", "Mouse set to allow basic clicks only (blocks middle/side buttons)")
            elif t == 'all': self.security_manager.mouse_manager.block_all_buttons(); messagebox.showinfo("✅ Applied", "Mouse set to block all buttons")
        finally:
            self.refresh_status()

    # ===== Window Controls (stable) =====
    def show_window_controls(self):
        win = tk.Toplevel(self.window); win.title("🪟 Window Guardian Controls"); win.geometry("600x500"); win.configure(bg=self.colors['surface']); win.transient(self.window)
        win.update_idletasks(); x = (win.winfo_screenwidth() // 2) - 300; y = (win.winfo_screenheight() // 2) - 250; win.geometry(f"600x500+{x}+{y}")
        header = tk.Frame(win, bg=self.colors['primary'], height=60); header.pack(fill=tk.X); header.pack_propagate(False)
        tk.Label(header, text="🪟 Window Protection System", font=("Segoe UI", 14, "bold"), bg=self.colors['primary'], fg=self.colors['card']).pack(pady=20)
        content = tk.Frame(win, bg=self.colors['surface']); content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        status_frame = tk.Frame(content, bg=self.colors['card'], pady=15); status_frame.pack(fill=tk.X, pady=(0,20))
        is_active = self.security_manager.window_manager.is_active; status_text = "🟢 ACTIVE" if is_active else "🔴 INACTIVE"; status_color = self.colors['success'] if is_active else self.colors['danger']
        tk.Label(status_frame, text=f"Status: {status_text}", font=("Segoe UI", 12, "bold"), bg=self.colors['card'], fg=status_color).pack(pady=10)
        try:
            st = self.security_manager.window_manager.get_status(); count = st.get('protected_windows_count', 0); level = st.get('protection_level','Unknown')
        except Exception:
            count = 0; level = 'Unavailable'
        tk.Label(status_frame, text=f"Protected Windows: {count}", font=("Segoe UI", 10), bg=self.colors['card'], fg=self.colors['text_primary']).pack(pady=2)
        tk.Label(status_frame, text=f"Protection Level: {level}", font=("Segoe UI", 10), bg=self.colors['card'], fg=self.colors['text_primary']).pack(pady=2)
        ctrl = tk.Frame(content, bg=self.colors['card'], pady=20); ctrl.pack(fill=tk.X, pady=(0,20))
        if not is_active:
            tk.Button(ctrl, text="🚀 Activate Window Protection", command=lambda: self._toggle_window_and_close(True, win), bg=self.colors['success'], fg=self.colors['card'], font=("Segoe UI", 11, "bold"), relief=tk.FLAT, cursor='hand2', padx=20, pady=10).pack(pady=10)
            info = ("Window Protection will:\n"
                    "• Disable close and minimize buttons\n"
                    "• Prevent accidental closes\n"
                    "• Monitor/guard exam & browser windows")
            tk.Label(ctrl, text=info, font=("Segoe UI", 9), bg=self.colors['card'], fg=self.colors['text_secondary'], justify=tk.LEFT).pack(pady=10)
        else:
            tk.Button(ctrl, text="🛑 Deactivate Window Protection", command=lambda: self._toggle_window_and_close(False, win), bg=self.colors['danger'], fg=self.colors['card'], font=("Segoe UI", 11, "bold"), relief=tk.FLAT, cursor='hand2', padx=20, pady=10).pack(pady=10)
            if count:
                try:
                    protected = st.get('protected_windows', {})
                    tk.Label(ctrl, text="Currently Protected Windows:", font=("Segoe UI", 10, "bold"), bg=self.colors['card'], fg=self.colors['text_primary']).pack(anchor=tk.W, pady=(10,5))
                    txt = "\n".join([f"• {title}" for title in list(protected.values())[:5]])
                    if len(protected) > 5: txt += f"\n... and {len(protected)-5} more"
                    tk.Label(ctrl, text=txt, font=("Segoe UI", 9), bg=self.colors['card'], fg=self.colors['text_secondary'], justify=tk.LEFT).pack(anchor=tk.W, pady=5)
                except Exception:
                    pass
        tk.Button(content, text="Close", command=win.destroy, bg=self.colors['secondary'], fg=self.colors['card'], font=("Segoe UI", 10, "bold"), relief=tk.FLAT, cursor='hand2', padx=20, pady=8).pack(pady=20)

    def _toggle_window_and_close(self, enable, window):
        try:
            ok = self.security_manager.toggle_window_protection(enable); action = "activated" if enable else "deactivated"
            messagebox.showinfo("✅ Success", f"Window protection {action} successfully!") if ok else messagebox.showerror("❌ Error", f"Failed to {action.replace('ed','')} window protection.")
        finally:
            window.destroy(); self.refresh_status()

    # ===== Network & other existing UI =====
    def show_network_controls(self):
        win = tk.Toplevel(self.window); win.title("🌐 Network Security Controls"); win.geometry("500x400"); win.configure(bg=self.colors['surface']); win.transient(self.window)
        win.update_idletasks(); x = (win.winfo_screenwidth() // 2) - 250; y = (win.winfo_screenheight() // 2) - 200; win.geometry(f"500x400+{x}+{y}")
        header = tk.Frame(win, bg=self.colors['warning'], height=60); header.pack(fill=tk.X); header.pack_propagate(False)
        tk.Label(header, text="🌐 Internet Blocking System", font=("Segoe UI", 14, "bold"), bg=self.colors['warning'], fg=self.colors['card']).pack(pady=20)
        content = tk.Frame(win, bg=self.colors['surface']); content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        status = "🟢 BLOCKED" if self.security_manager.network_manager.is_blocked else "🔴 ALLOWED"
        tk.Label(content, text=f"Internet Access: {status}", font=("Segoe UI", 12, "bold"), bg=self.colors['surface'], fg=self.colors['text_primary']).pack(pady=10)
        ctrl = tk.Frame(content, bg=self.colors['card']); ctrl.pack(pady=20, fill=tk.BOTH, expand=True)
        if not self.security_manager.network_manager.is_blocked:
            tk.Button(ctrl, text="🚀 Activate Internet Blocking", command=lambda: [self.toggle_internet_blocking(True), win.destroy()], bg=self.colors['success'], fg=self.colors['card'], font=("Segoe UI", 11, "bold"), relief=tk.FLAT, cursor='hand2', padx=20, pady=10).pack(pady=20)
        else:
            tk.Button(ctrl, text="🛑 Restore Internet Access", command=lambda: [self.toggle_internet_blocking(False), win.destroy()], bg=self.colors['danger'], fg=self.colors['card'], font=("Segoe UI", 11, "bold"), relief=tk.FLAT, cursor='hand2', padx=20, pady=10).pack(pady=20)

    # ===== Selective Lockdown, Settings, Logs, Detection (existing from your file) =====
    # Keep your existing implementations of: create_monitoring_tab, create_settings_tab,
    # create_logs_tab, detect_key_combination, add_detected_key, cancel_key_detection,
    # detect_mouse_button, add_detected_mouse, cancel_mouse_detection, etc.

    # ===== Status & Toggles =====
    def refresh_status(self):
        info = self.security_manager.get_system_info() or {}
        if self.security_manager.is_exam_mode:
            self.status_label.config(text="🔒 LOCKDOWN MODE: ACTIVE", fg=self.colors['danger'])
        else:
            self.status_label.config(text="🔓 LOCKDOWN MODE: INACTIVE", fg=self.colors['success'])
        cpu = info.get('cpu_percent', 0.0); mem = info.get('memory_percent', 0.0); procs = info.get('active_processes', 0)
        self.system_info_label.config(text=f"CPU: {cpu:.1f}% | RAM: {mem:.1f}% | Processes: {procs}")
        self.keyboard_status.config(text=("✅ Keyboard" if info.get('hooks_active') else "⚫ Keyboard"), fg=(self.colors['success'] if info.get('hooks_active') else self.colors['text_secondary']))
        self.mouse_status.config(text=("✅ Mouse" if info.get('mouse_blocking') else "⚫ Mouse"), fg=(self.colors['success'] if info.get('mouse_blocking') else self.colors['text_secondary']))
        self.network_status.config(text=("✅ Network" if info.get('internet_blocked') else "⚫ Network"), fg=(self.colors['success'] if info.get('internet_blocked') else self.colors['text_secondary']))
        self.window_status.config(text=("✅ Windows" if info.get('window_protection') else "⚫ Windows"), fg=(self.colors['success'] if info.get('window_protection') else self.colors['text_secondary']))

    def toggle_mouse_blocking(self, enable):
        return self.security_manager.toggle_mouse_blocking(enable)
    def toggle_internet_blocking(self, enable):
        return self.security_manager.toggle_internet_blocking(enable)
    def toggle_window_protection(self, enable):
        return self.security_manager.toggle_window_protection(enable)

    # ===== Stop/Emergency =====
    def stop_exam_mode(self):
        pwd = simpledialog.askstring("🔐 SECURITY VERIFICATION", "Enter admin password to DISABLE lockdown:", show="*")
        if not pwd: return
        import hashlib; h = hashlib.sha256(pwd.encode()).hexdigest()
        if self.db_manager.verify_admin("admin", h):
            self.security_manager.stop_exam_mode(); self.start_btn.config(state=tk.NORMAL); self.stop_btn.config(state=tk.DISABLED); self.refresh_status(); messagebox.showinfo("🔓 LOCKDOWN DISABLED", "All security restrictions have been removed.")
        else:
            messagebox.showerror("❌ ACCESS DENIED", "Invalid admin password!")

    def emergency_stop(self):
        if not messagebox.askyesno("🚨 EMERGENCY STOP", "This is an EMERGENCY STOP procedure.\n\nAre you sure?"): return
        if not messagebox.askyesno("⚠️ FINAL WARNING", "This will IMMEDIATELY disable ALL security.\n\nCONFIRM?"): return
        pwd = simpledialog.askstring("🔐 EMERGENCY AUTH", "Enter admin password for EMERGENCY STOP:", show="*")
        if not pwd: return
        import hashlib; h = hashlib.sha256(pwd.encode()).hexdigest()
        if self.db_manager.verify_admin("admin", h):
            try:
                self.security_manager.stop_exam_mode(); self.start_btn.config(state=tk.NORMAL); self.stop_btn.config(state=tk.DISABLED); self.refresh_status(); messagebox.showwarning("🚨 EMERGENCY STOP EXECUTED", "Emergency stop completed.\nAll security systems disabled.")
            except Exception as e:
                messagebox.showerror("Error", f"Emergency stop failed: {e}")
        else:
            messagebox.showerror("❌ ACCESS DENIED", "Invalid admin password!")

    # ===== Auto-refresh =====
    def start_auto_refresh(self):
        def loop():
            while True:
                try:
                    if self.window.winfo_exists():
                        self.window.after(0, self.refresh_status)
                        threading.Event().wait(2)
                    else:
                        break
                except:
                    break
        threading.Thread(target=loop, daemon=True).start()
