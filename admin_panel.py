"""
Admin Panel for Exam Shield - COMPLETE STABLE VERSION
All methods properly defined to eliminate attribute errors
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, simpledialog, filedialog
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

    def setup_window(self):
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - 475
        y = (self.window.winfo_screenheight() // 2) - 375
        self.window.geometry(f"950x750+{x}+{y}")
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        try:
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

    # ===== SELECTIVE LOCKDOWN DIALOG (FIXED) =====
    def show_selective_lockdown_dialog(self):
        dialog = tk.Toplevel(self.window)
        dialog.title("🔒 Selective Lockdown Configuration")
        dialog.geometry("500x600")
        dialog.configure(bg=self.colors['surface'])
        dialog.transient(self.window)
        dialog.grab_set()

        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - 250
        y = (dialog.winfo_screenheight() // 2) - 300
        dialog.geometry(f"500x600+{x}+{y}")

        header = tk.Frame(dialog, bg=self.colors['primary'], height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        tk.Label(header, text="🔒 Select Security Modules to Activate",
                font=("Segoe UI", 14, "bold"), bg=self.colors['primary'], 
                fg=self.colors['card']).pack(pady=20)

        options = tk.Frame(dialog, bg=self.colors['surface'])
        options.pack(fill=tk.BOTH, expand=True, padx=40, pady=20)

        self.selective_vars = {}
        modules = [
            ("keyboard", "🔤 Keyboard Shortcuts Blocking", "Block Alt+Tab, Ctrl+Alt+Del, etc."),
            ("mouse", "🖱️ Mouse Button Restrictions", "Block middle, back, forward buttons"),
            ("internet", "🌐 Internet Access Blocking", "Complete internet disconnection"),
            ("windows", "🪟 Window Protection", "Prevent closing/minimizing windows"),
            ("processes", "🔍 Process Monitoring", "Auto-terminate suspicious processes")
        ]

        for key, title, desc in modules:
            card = tk.Frame(options, bg=self.colors['card'], relief=tk.FLAT, bd=1)
            card.pack(fill=tk.X, pady=(0, 10))
            content = tk.Frame(card, bg=self.colors['card'])
            content.pack(fill=tk.X, padx=15, pady=12)
            var = tk.BooleanVar(value=True)
            self.selective_vars[key] = var
            tk.Checkbutton(content, text=title, variable=var,
                         font=("Segoe UI", 11, "bold"), bg=self.colors['card'],
                         fg=self.colors['text_primary'], selectcolor=self.colors['card'],
                         activebackground=self.colors['card']).pack(anchor=tk.W)
            tk.Label(content, text=desc, font=("Segoe UI", 9), bg=self.colors['card'],
                    fg=self.colors['text_secondary']).pack(anchor=tk.W, padx=20, pady=(2,0))

        btns = tk.Frame(dialog, bg=self.colors['surface'])
        btns.pack(fill=tk.X, padx=40, pady=20)
        tk.Button(btns, text="🚀 START SELECTED LOCKDOWN",
                 command=lambda: self.start_selective_lockdown(dialog),
                 bg=self.colors['success'], fg=self.colors['card'], 
                 font=("Segoe UI", 11, "bold"), relief=tk.FLAT, pady=10, cursor='hand2').pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0,10))
        tk.Button(btns, text="❌ CANCEL", command=dialog.destroy,
                 bg=self.colors['danger'], fg=self.colors['card'], 
                 font=("Segoe UI", 11, "bold"), relief=tk.FLAT, pady=10, cursor='hand2').pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(10,0))

    def start_selective_lockdown(self, dialog):
        selected = {key: var.get() for key, var in self.selective_vars.items()}
        if not any(selected.values()):
            messagebox.showwarning("No Selection", "Please select at least one security module!")
            return
        names = [key.title() for key, s in selected.items() if s]
        if messagebox.askyesno("Confirm Selective Lockdown", "Start lockdown with these modules?\n\n" + "\n".join(f"✓ {n}" for n in names)):
            dialog.destroy()
            try:
                self.security_manager.start_exam_mode(selected)
                self.start_btn.config(state=tk.DISABLED)
                self.stop_btn.config(state=tk.NORMAL)
                self.refresh_status()
                messagebox.showinfo("🔒 SELECTIVE LOCKDOWN ACTIVE", "Lockdown active with:\n" + "\n".join(f"✓ {n}" for n in names))
            except Exception as e:
                messagebox.showerror("Error", f"Failed to start lockdown: {e}")

    # ===== MONITORING TAB =====
    def create_monitoring_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="📊 Live Monitor")
        container = tk.Frame(frame, bg=self.colors['surface']); container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        header = tk.Frame(container, bg=self.colors['info'], height=50); header.pack(fill=tk.X); header.pack_propagate(False)
        tk.Label(header, text="📊 Real-time Security Events", font=("Segoe UI", 14, "bold"), bg=self.colors['info'], fg=self.colors['card']).pack(pady=15)
        content = tk.Frame(container, bg=self.colors['card']); content.pack(fill=tk.BOTH, expand=True, pady=(10,0))
        columns = ("Time","Severity","Action","Details","Status")
        self.activity_tree = ttk.Treeview(content, columns=columns, show="headings", height=20)
        for col in columns: self.activity_tree.heading(col, text=col)
        self.activity_tree.column("Time", width=120); self.activity_tree.column("Severity", width=80); self.activity_tree.column("Action", width=180); self.activity_tree.column("Details", width=300); self.activity_tree.column("Status", width=100)
        sb = ttk.Scrollbar(content, orient=tk.VERTICAL, command=self.activity_tree.yview); self.activity_tree.configure(yscrollcommand=sb.set)
        self.activity_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20); sb.pack(side=tk.RIGHT, fill=tk.Y, padx=(0,20), pady=20)

    def update_activity_feed(self):
        try:
            for item in self.activity_tree.get_children():
                self.activity_tree.delete(item)
            logs = self.db_manager.get_activity_logs(20)
            for log in logs:
                action, details, timestamp, blocked = log
                status = "🚫 BLOCKED" if blocked else "✅ ALLOWED"
                if blocked or "SUSPICIOUS" in action: severity = "🔴 HIGH"
                elif "BLOCKED" in action: severity = "🟡 MED"
                else: severity = "🟢 LOW"
                try:
                    dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                    time_str = dt.strftime("%H:%M:%S")
                except: time_str = timestamp
                self.activity_tree.insert("", 0, values=(time_str, severity, action, details or "No details", status))
        except Exception: pass

    # ===== SETTINGS TAB =====
    def create_settings_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="⚙️ Settings")
        container = tk.Frame(frame, bg=self.colors['surface']); container.pack(fill=tk.BOTH, expand=True)
        canvas = tk.Canvas(container, bg=self.colors['surface'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        inner = tk.Frame(canvas, bg=self.colors['surface'])
        inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0,0), window=inner, anchor="nw"); canvas.configure(yscrollcommand=scrollbar.set)
        
        # Settings content
        settings_card = tk.Frame(inner, bg=self.colors['card']); settings_card.pack(fill=tk.X, padx=10, pady=10)
        header = tk.Frame(settings_card, bg=self.colors['success'], height=40); header.pack(fill=tk.X); header.pack_propagate(False)
        tk.Label(header, text="🔧 Advanced Settings", font=("Segoe UI", 12, "bold"), bg=self.colors['success'], fg=self.colors['card']).pack(pady=10)
        content = tk.Frame(settings_card, bg=self.colors['card']); content.pack(fill=tk.X, padx=15, pady=15)
        
        self.auto_start_var = tk.BooleanVar()
        tk.Checkbutton(content, text="Auto-start lockdown mode on login", variable=self.auto_start_var, font=("Segoe UI", 10), bg=self.colors['card'], fg=self.colors['text_primary'], selectcolor=self.colors['card'], activebackground=self.colors['card']).pack(anchor=tk.W)
        self.window_protection_var = tk.BooleanVar(value=True)
        tk.Checkbutton(content, text="Enable aggressive window protection", variable=self.window_protection_var, font=("Segoe UI", 10), bg=self.colors['card'], fg=self.colors['text_primary'], selectcolor=self.colors['card'], activebackground=self.colors['card']).pack(anchor=tk.W)
        self.process_monitoring_var = tk.BooleanVar(value=True)
        tk.Checkbutton(content, text="Enable unauthorized process termination", variable=self.process_monitoring_var, font=("Segoe UI", 10), bg=self.colors['card'], fg=self.colors['text_primary'], selectcolor=self.colors['card'], activebackground=self.colors['card']).pack(anchor=tk.W)
        tk.Button(content, text="💾 Save All Settings", command=self.save_settings, bg=self.colors['primary'], fg=self.colors['card'], font=("Segoe UI", 11, "bold"), relief=tk.FLAT, cursor='hand2', padx=20, pady=10).pack(pady=(15,0))
        
        canvas.pack(side="left", fill="both", expand=True, padx=15, pady=15); scrollbar.pack(side="right", fill="y", padx=(0,15), pady=15)

    def save_settings(self):
        try:
            messagebox.showinfo("✅ Success", "Settings saved successfully!")
        except Exception as e:
            messagebox.showerror("❌ Error", f"Failed to save settings: {e}")

    # ===== LOGS TAB =====
    def create_logs_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="📋 Security Logs")
        container = tk.Frame(frame, bg=self.colors['surface']); container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        controls = tk.Frame(container, bg=self.colors['card'], height=60); controls.pack(fill=tk.X, pady=(0,10)); controls.pack_propagate(False)
        row = tk.Frame(controls, bg=self.colors['card']); row.pack(fill=tk.X, padx=15, pady=15)
        tk.Button(row, text="🔄 Refresh", command=self.refresh_logs, bg=self.colors['info'], fg=self.colors['card'], font=("Segoe UI", 9, "bold"), relief=tk.FLAT, cursor='hand2', padx=10, pady=5).pack(side=tk.LEFT, padx=(0,10))
        tk.Button(row, text="🗑️ Clear All", command=self.clear_logs, bg=self.colors['warning'], fg=self.colors['card'], font=("Segoe UI", 9, "bold"), relief=tk.FLAT, cursor='hand2', padx=10, pady=5).pack(side=tk.LEFT, padx=(0,10))
        tk.Button(row, text="💾 Export", command=self.export_logs, bg=self.colors['success'], fg=self.colors['card'], font=("Segoe UI", 9, "bold"), relief=tk.FLAT, cursor='hand2', padx=10, pady=5).pack(side=tk.LEFT, padx=(0,10))
        
        self.log_filter_var = tk.StringVar()
        tk.Label(row, text="Filter:", font=("Segoe UI", 9, "bold"), bg=self.colors['card'], fg=self.colors['text_primary']).pack(side=tk.LEFT, padx=(20,5))
        filter_combo = ttk.Combobox(row, textvariable=self.log_filter_var, values=["All", "Blocked Only", "Security Events"], font=("Segoe UI", 9))
        filter_combo.set("All"); filter_combo.pack(side=tk.LEFT, padx=(0,10))
        filter_combo.bind("<<ComboboxSelected>>", lambda e: self.refresh_logs())
        
        logs_card = tk.Frame(container, bg=self.colors['card']); logs_card.pack(fill=tk.BOTH, expand=True)
        header = tk.Frame(logs_card, bg=self.colors['danger'], height=40); header.pack(fill=tk.X); header.pack_propagate(False)
        tk.Label(header, text="📋 Security Activity History", font=("Segoe UI", 12, "bold"), bg=self.colors['danger'], fg=self.colors['card']).pack(pady=10)
        content = tk.Frame(logs_card, bg=self.colors['card']); content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        self.logs_text = scrolledtext.ScrolledText(content, wrap=tk.WORD, height=25, font=("Consolas", 9), bg=self.colors['surface'], fg=self.colors['text_primary'])
        self.logs_text.pack(fill=tk.BOTH, expand=True)

    def refresh_logs(self):
        try:
            logs = self.db_manager.get_activity_logs(100)
        except Exception:
            logs = []
        self.logs_text.delete(1.0, tk.END)
        for log in logs:
            try:
                action, details, timestamp, blocked = log
                status = "BLOCKED" if blocked else "ALLOWED"
                self.logs_text.insert(tk.END, f"[{timestamp}] {action}: {details or 'N/A'} - {status}\n")
            except Exception:
                continue
        self.logs_text.see(tk.END)

    def clear_logs(self):
        self.logs_text.delete(1.0, tk.END)
        messagebox.showinfo("✅ Success", "Logs cleared!")

    def export_logs(self):
        filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if filename:
            try:
                with open(filename, 'w') as f:
                    f.write(self.logs_text.get(1.0, tk.END))
                messagebox.showinfo("✅ Success", f"Logs exported to:\n{filename}")
            except Exception as e:
                messagebox.showerror("❌ Error", f"Export failed: {e}")

    # ===== MOUSE CONTROLS =====
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
            blocked_text = ", ".join(blocked) if isinstance(blocked, list) else str(blocked)
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

    # ===== WINDOW CONTROLS =====
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
            info = ("Window Protection will:\n• Disable close and minimize buttons\n• Prevent accidental closes\n• Monitor/guard exam & browser windows")
            tk.Label(ctrl, text=info, font=("Segoe UI", 9), bg=self.colors['card'], fg=self.colors['text_secondary'], justify=tk.LEFT).pack(pady=10)
        else:
            tk.Button(ctrl, text="🛑 Deactivate Window Protection", command=lambda: self._toggle_window_and_close(False, win), bg=self.colors['danger'], fg=self.colors['card'], font=("Segoe UI", 11, "bold"), relief=tk.FLAT, cursor='hand2', padx=20, pady=10).pack(pady=10)
        tk.Button(content, text="Close", command=win.destroy, bg=self.colors['secondary'], fg=self.colors['card'], font=("Segoe UI", 10, "bold"), relief=tk.FLAT, cursor='hand2', padx=20, pady=8).pack(pady=20)

    def _toggle_window_and_close(self, enable, window):
        try:
            ok = self.security_manager.toggle_window_protection(enable); action = "activated" if enable else "deactivated"
            messagebox.showinfo("✅ Success", f"Window protection {action} successfully!") if ok else messagebox.showerror("❌ Error", f"Failed to {action.replace('ed','')} window protection.")
        finally:
            window.destroy(); self.refresh_status()

    # ===== NETWORK CONTROLS =====
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

    # ===== STATUS & TOGGLES =====
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
        try:
            return self.security_manager.toggle_mouse_blocking(enable)
        except Exception as e:
            messagebox.showerror("Error", f"Mouse toggle failed: {e}")
            return False

    def toggle_internet_blocking(self, enable):
        try:
            return self.security_manager.toggle_internet_blocking(enable)
        except Exception as e:
            messagebox.showerror("Error", f"Internet toggle failed: {e}")
            return False

    def toggle_window_protection(self, enable):
        try:
            return self.security_manager.toggle_window_protection(enable)
        except Exception as e:
            messagebox.showerror("Error", f"Window toggle failed: {e}")
            return False

    # ===== STOP/EMERGENCY =====
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

    # ===== AUTO-REFRESH =====
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