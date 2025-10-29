"""
Admin Panel for Exam Shield - ENHANCED WITH SELECTIVE CONTROLS
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
        
        # NEW: Set admin panel reference in security manager
        self.security_manager.set_admin_panel(self)
        
        # NEW: Key/Mouse detection variables
        self.detecting_key = False
        self.detecting_mouse = False
        self.detected_key = None
        self.mouse_listener = None
        
        # Premium color scheme
        self.colors = {
            'primary': '#1e3d59',
            'secondary': '#17223b', 
            'accent': '#ffc947',
            'success': '#27ae60',
            'warning': '#f39c12',
            'danger': '#e74c3c',
            'info': '#3498db',
            'surface': '#f8f9fa',
            'card': '#ffffff',
            'text_primary': '#2c3e50',
            'text_secondary': '#7f8c8d',
            'border': '#dee2e6'
        }
        
        self.window = tk.Toplevel()
        self.window.title("Exam Shield Premium - Administrative Control Center")
        self.window.geometry("950x750")
        self.window.resizable(True, True)
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

    def setup_ui(self):
        # Create main container with premium header
        main_frame = tk.Frame(self.window, bg=self.colors['surface'])
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Premium Header Section
        header_frame = tk.Frame(main_frame, bg=self.colors['primary'], height=70)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        # Header content
        header_content = tk.Frame(header_frame, bg=self.colors['primary'])
        header_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        # Logo and title
        logo_label = tk.Label(header_content, text="🛡️", font=("Segoe UI", 20),
                            bg=self.colors['primary'], fg=self.colors['accent'])
        logo_label.pack(side=tk.LEFT, padx=(0, 15))
        
        title_frame = tk.Frame(header_content, bg=self.colors['primary'])
        title_frame.pack(side=tk.LEFT)
        
        main_title = tk.Label(title_frame, text="EXAM SHIELD PREMIUM", 
                            font=("Segoe UI", 16, "bold"),
                            bg=self.colors['primary'], fg=self.colors['card'])
        main_title.pack(anchor=tk.W)
        
        subtitle = tk.Label(title_frame, text="Administrative Control Center v1.1", 
                          font=("Segoe UI", 9),
                          bg=self.colors['primary'], fg='#ecf4ff')
        subtitle.pack(anchor=tk.W)
        
        # Status in header
        status_frame = tk.Frame(header_content, bg=self.colors['primary'])
        status_frame.pack(side=tk.RIGHT)
        
        self.header_status = tk.Label(status_frame, text="🔓 SYSTEM READY", 
                                    font=("Segoe UI", 10, "bold"),
                                    bg=self.colors['primary'], fg=self.colors['accent'])
        self.header_status.pack()

        # Create notebook with premium styling
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Style the notebook
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook', background=self.colors['surface'])
        style.configure('TNotebook.Tab', padding=[20, 10], font=('Segoe UI', 10, 'bold'))
        
        # Create tabs
        self.create_control_tab()
        self.create_monitor_tab()
        self.create_settings_tab()
        self.create_logs_tab()

    def create_control_tab(self):
        # Main Control Tab with premium design
        control_frame = ttk.Frame(self.notebook)
        self.notebook.add(control_frame, text="📊 Control Center")
        
        # Main container
        main_container = tk.Frame(control_frame, bg=self.colors['surface'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Status section with premium cards
        status_section = tk.Frame(main_container, bg=self.colors['surface'])
        status_section.pack(fill=tk.X, pady=(0, 20))
        
        # Status Card
        status_card = tk.Frame(status_section, bg=self.colors['card'], relief=tk.FLAT, bd=1)
        status_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Status card header
        status_header = tk.Frame(status_card, bg=self.colors['primary'], height=40)
        status_header.pack(fill=tk.X)
        status_header.pack_propagate(False)
        
        tk.Label(status_header, text="📊 System Status", font=("Segoe UI", 12, "bold"),
                bg=self.colors['primary'], fg=self.colors['card']).pack(pady=10)
        
        # Status content
        status_content = tk.Frame(status_card, bg=self.colors['card'])
        status_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        self.status_label = tk.Label(status_content, text="🔓 Lockdown Mode: INACTIVE", 
                                   font=("Segoe UI", 14, "bold"), bg=self.colors['card'], 
                                   fg=self.colors['success'])
        self.status_label.pack(anchor=tk.W, pady=(0, 10))
        
        self.system_info_label = tk.Label(status_content, text="Loading system information...",
                                        font=("Segoe UI", 9), bg=self.colors['card'], 
                                        fg=self.colors['text_secondary'])
        self.system_info_label.pack(anchor=tk.W)
        
        # Security Modules Card
        modules_card = tk.Frame(status_section, bg=self.colors['card'], relief=tk.FLAT, bd=1)
        modules_card.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # Modules card header
        modules_header = tk.Frame(modules_card, bg=self.colors['info'], height=40)
        modules_header.pack(fill=tk.X)
        modules_header.pack_propagate(False)
        
        tk.Label(modules_header, text="🔒 Security Modules", font=("Segoe UI", 12, "bold"),
                bg=self.colors['info'], fg=self.colors['card']).pack(pady=10)
        
        # Modules content
        modules_content = tk.Frame(modules_card, bg=self.colors['card'])
        modules_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        # Create module indicators
        self.module_indicators = {}
        modules = [
            ("keyboard", "🔤 Keyboard Guard"),
            ("mouse", "🖱️ Mouse Control"),
            ("network", "🌐 Network Shield"),
            ("windows", "🪟 Window Guardian")
        ]
        
        for key, name in modules:
            module_frame = tk.Frame(modules_content, bg=self.colors['card'])
            module_frame.pack(fill=tk.X, pady=2)
            
            indicator = tk.Label(module_frame, text="⚫", font=("Segoe UI", 10),
                               bg=self.colors['card'], fg=self.colors['text_secondary'])
            indicator.pack(side=tk.LEFT, padx=(0, 8))
            
            label = tk.Label(module_frame, text=name, font=("Segoe UI", 10),
                           bg=self.colors['card'], fg=self.colors['text_primary'])
            label.pack(side=tk.LEFT)
            
            self.module_indicators[key] = indicator

        # Control Buttons Section
        control_section = tk.Frame(main_container, bg=self.colors['surface'])
        control_section.pack(fill=tk.X, pady=(0, 20))
        
        # Control buttons card
        control_card = tk.Frame(control_section, bg=self.colors['card'], relief=tk.FLAT, bd=1)
        control_card.pack(fill=tk.X)
        
        # Control card header
        control_header = tk.Frame(control_card, bg=self.colors['warning'], height=40)
        control_header.pack(fill=tk.X)
        control_header.pack_propagate(False)
        
        tk.Label(control_header, text="🎯 Lockdown Controls", font=("Segoe UI", 12, "bold"),
                bg=self.colors['warning'], fg=self.colors['card']).pack(pady=10)
        
        # Buttons frame
        buttons_frame = tk.Frame(control_card, bg=self.colors['card'])
        buttons_frame.pack(fill=tk.X, padx=20, pady=20)
        
        # Premium styled buttons
        self.start_btn = tk.Button(buttons_frame, text="🚀 START SELECTIVE LOCKDOWN", 
                                 command=self.show_selective_lockdown_dialog,
                                 bg=self.colors['primary'], fg=self.colors['card'],
                                 font=("Segoe UI", 11, "bold"), relief=tk.FLAT, 
                                 cursor='hand2', padx=20, pady=10)
        self.start_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_btn = tk.Button(buttons_frame, text="🔓 END LOCKDOWN MODE", 
                                command=self.stop_exam_mode,
                                bg=self.colors['warning'], fg=self.colors['card'],
                                font=("Segoe UI", 11, "bold"), relief=tk.FLAT, 
                                cursor='hand2', padx=20, pady=10, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.emergency_btn = tk.Button(buttons_frame, text="🚨 EMERGENCY STOP", 
                                     command=self.emergency_stop,
                                     bg=self.colors['danger'], fg=self.colors['card'],
                                     font=("Segoe UI", 11, "bold"), relief=tk.FLAT, 
                                     cursor='hand2', padx=20, pady=10)
        self.emergency_btn.pack(side=tk.RIGHT)

        # Individual Controls Section
        individual_section = tk.Frame(main_container, bg=self.colors['surface'])
        individual_section.pack(fill=tk.BOTH, expand=True)
        
        individual_card = tk.Frame(individual_section, bg=self.colors['card'], relief=tk.FLAT, bd=1)
        individual_card.pack(fill=tk.BOTH, expand=True)
        
        # Individual card header
        individual_header = tk.Frame(individual_card, bg=self.colors['success'], height=40)
        individual_header.pack(fill=tk.X)
        individual_header.pack_propagate(False)
        
        tk.Label(individual_header, text="🛠️ Individual Security Controls", 
                font=("Segoe UI", 12, "bold"),
                bg=self.colors['success'], fg=self.colors['card']).pack(pady=10)
        
        # Individual controls grid
        controls_content = tk.Frame(individual_card, bg=self.colors['card'])
        controls_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Grid of control buttons
        controls_grid = tk.Frame(controls_content, bg=self.colors['card'])
        controls_grid.pack(fill=tk.X)
        
        # Row 1
        row1 = tk.Frame(controls_grid, bg=self.colors['card'])
        row1.pack(fill=tk.X, pady=(0, 10))
        
        tk.Button(row1, text="🖱️ Mouse Security", command=self.show_mouse_controls,
                 bg=self.colors['info'], fg=self.colors['card'],
                 font=("Segoe UI", 10, "bold"), relief=tk.FLAT, 
                 cursor='hand2', padx=15, pady=8).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(row1, text="🌐 Network Control", command=self.show_network_controls,
                 bg=self.colors['info'], fg=self.colors['card'],
                 font=("Segoe UI", 10, "bold"), relief=tk.FLAT, 
                 cursor='hand2', padx=15, pady=8).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(row1, text="🪟 Window Guardian", command=self.show_window_controls,
                 bg=self.colors['info'], fg=self.colors['card'],
                 font=("Segoe UI", 10, "bold"), relief=tk.FLAT, 
                 cursor='hand2', padx=15, pady=8).pack(side=tk.LEFT)
        
        # Row 2
        row2 = tk.Frame(controls_grid, bg=self.colors['card'])
        row2.pack(fill=tk.X)
        
        tk.Button(row2, text="📊 Live Monitor", command=self.switch_to_monitor,
                 bg=self.colors['secondary'], fg=self.colors['card'],
                 font=("Segoe UI", 10, "bold"), relief=tk.FLAT, 
                 cursor='hand2', padx=15, pady=8).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(row2, text="⚙️ Settings Panel", command=self.switch_to_settings,
                 bg=self.colors['secondary'], fg=self.colors['card'],
                 font=("Segoe UI", 10, "bold"), relief=tk.FLAT, 
                 cursor='hand2', padx=15, pady=8).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(row2, text="🔄 Refresh Status", command=self.refresh_status,
                 bg=self.colors['secondary'], fg=self.colors['card'],
                 font=("Segoe UI", 10, "bold"), relief=tk.FLAT, 
                 cursor='hand2', padx=15, pady=8).pack(side=tk.LEFT)

    def create_monitor_tab(self):
        # Monitor Tab
        monitor_frame = ttk.Frame(self.notebook)
        self.notebook.add(monitor_frame, text="📈 Live Monitor")
        
        # Monitor container
        monitor_container = tk.Frame(monitor_frame, bg=self.colors['surface'])
        monitor_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Monitor header
        monitor_header = tk.Frame(monitor_container, bg=self.colors['info'], height=50)
        monitor_header.pack(fill=tk.X)
        monitor_header.pack_propagate(False)
        
        tk.Label(monitor_header, text="📈 Real-time Security Monitor", 
                font=("Segoe UI", 14, "bold"),
                bg=self.colors['info'], fg=self.colors['card']).pack(pady=15)
        
        # Monitor content
        monitor_content = tk.Frame(monitor_container, bg=self.colors['card'])
        monitor_content.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # Create treeview for activity monitoring
        columns = ("Time", "Severity", "Module", "Event", "Details", "Status")
        self.activity_tree = ttk.Treeview(monitor_content, columns=columns, 
                                        show="headings", height=25)
        
        # Configure columns
        column_widths = {"Time": 120, "Severity": 80, "Module": 100, 
                        "Event": 150, "Details": 300, "Status": 100}
        
        for col in columns:
            self.activity_tree.heading(col, text=col)
            self.activity_tree.column(col, width=column_widths.get(col, 100))
        
        # Scrollbar
        scrollbar_monitor = ttk.Scrollbar(monitor_content, orient=tk.VERTICAL, 
                                        command=self.activity_tree.yview)
        self.activity_tree.configure(yscrollcommand=scrollbar_monitor.set)
        
        # Pack treeview and scrollbar
        self.activity_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)
        scrollbar_monitor.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 20), pady=20)

    def create_settings_tab(self):
        # Settings Tab
        settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(settings_frame, text="⚙️ Settings")
        
        # Settings container
        settings_container = tk.Frame(settings_frame, bg=self.colors['surface'])
        settings_container.pack(fill=tk.BOTH, expand=True)
        
        # Create canvas for scrolling
        canvas = tk.Canvas(settings_container, bg=self.colors['surface'], highlightthickness=0)
        scrollbar_settings = ttk.Scrollbar(settings_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['surface'])
        
        scrollable_frame.bind("<Configure>", 
                            lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar_settings.set)
        
        # Settings sections with premium design
        self.create_keyboard_settings(scrollable_frame)
        self.create_mouse_settings(scrollable_frame)
        self.create_network_settings(scrollable_frame)
        
        canvas.pack(side="left", fill="both", expand=True, padx=15, pady=15)
        scrollbar_settings.pack(side="right", fill="y", padx=(0, 15), pady=15)

    def create_logs_tab(self):
        # Logs Tab
        logs_frame = ttk.Frame(self.notebook)
        self.notebook.add(logs_frame, text="📋 Security Logs")
        
        # Logs container
        logs_container = tk.Frame(logs_frame, bg=self.colors['surface'])
        logs_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Logs header with controls
        logs_header = tk.Frame(logs_container, bg=self.colors['danger'], height=60)
        logs_header.pack(fill=tk.X)
        logs_header.pack_propagate(False)
        
        # Header content
        header_content = tk.Frame(logs_header, bg=self.colors['danger'])
        header_content.pack(fill=tk.X, padx=20, pady=15)
        
        tk.Label(header_content, text="📋 Security Event History", 
                font=("Segoe UI", 14, "bold"),
                bg=self.colors['danger'], fg=self.colors['card']).pack(side=tk.LEFT)
        
        # Control buttons in header
        controls_frame = tk.Frame(header_content, bg=self.colors['danger'])
        controls_frame.pack(side=tk.RIGHT)
        
        tk.Button(controls_frame, text="🔄 Refresh", command=self.refresh_logs,
                 bg=self.colors['card'], fg=self.colors['text_primary'],
                 font=("Segoe UI", 9, "bold"), relief=tk.FLAT, 
                 cursor='hand2', padx=10, pady=5).pack(side=tk.LEFT, padx=(0, 5))
        
        tk.Button(controls_frame, text="🗑️ Clear", command=self.clear_logs,
                 bg=self.colors['warning'], fg=self.colors['card'],
                 font=("Segoe UI", 9, "bold"), relief=tk.FLAT, 
                 cursor='hand2', padx=10, pady=5).pack(side=tk.LEFT, padx=(0, 5))
        
        tk.Button(controls_frame, text="💾 Export", command=self.export_logs,
                 bg=self.colors['success'], fg=self.colors['card'],
                 font=("Segoe UI", 9, "bold"), relief=tk.FLAT, 
                 cursor='hand2', padx=10, pady=5).pack(side=tk.LEFT)
        
        # Logs content
        logs_content = tk.Frame(logs_container, bg=self.colors['card'])
        logs_content.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        self.logs_text = scrolledtext.ScrolledText(logs_content, wrap=tk.WORD, 
                                                 height=30, font=("Consolas", 9),
                                                 bg=self.colors['surface'], 
                                                 fg=self.colors['text_primary'])
        self.logs_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    # Keep all the original methods exactly the same, just update the refresh_status method
    def refresh_status(self):
        """Update status with premium styling"""
        try:
            if hasattr(self, 'status_label') and self.status_label.winfo_exists():
                if self.security_manager.is_exam_mode:
                    self.status_label.config(text="🔒 LOCKDOWN MODE: ACTIVE", 
                                           fg=self.colors['danger'])
                    if hasattr(self, 'header_status') and self.header_status.winfo_exists():
                        self.header_status.config(text="🔒 LOCKDOWN ACTIVE")
                else:
                    self.status_label.config(text="🔓 LOCKDOWN MODE: INACTIVE", 
                                           fg=self.colors['success'])
                    if hasattr(self, 'header_status') and self.header_status.winfo_exists():
                        self.header_status.config(text="🔓 SYSTEM READY")
            
            # Update system information
            try:
                system_info = self.security_manager.get_system_info()
                if hasattr(self, 'system_info_label') and self.system_info_label.winfo_exists():
                    info_text = (f"CPU: {system_info.get('cpu_percent', 0):.1f}% | "
                                f"RAM: {system_info.get('memory_percent', 0):.1f}% | "
                                f"Processes: {system_info.get('active_processes', 0)}")
                    self.system_info_label.config(text=info_text)
                
                # Update module indicators
                modules_status = {
                    'keyboard': system_info.get('hooks_active', False),
                    'mouse': system_info.get('mouse_blocking', False),
                    'network': system_info.get('internet_blocked', False),
                    'windows': system_info.get('window_protection', False)
                }
                
                for module, active in modules_status.items():
                    if module in self.module_indicators:
                        indicator = self.module_indicators[module]
                        if hasattr(indicator, 'winfo_exists') and indicator.winfo_exists():
                            if active:
                                indicator.config(text="🟢", fg=self.colors['success'])
                            else:
                                indicator.config(text="⚫", fg=self.colors['text_secondary'])
                                
            except Exception as e:
                if hasattr(self, 'system_info_label') and self.system_info_label.winfo_exists():
                    self.system_info_label.config(text=f"Status update error: {str(e)}")
                
        except Exception as e:
            print(f"Error in refresh_status: {e}")

    # Keep all original methods exactly the same structure
    def show_selective_lockdown_dialog(self):
        """Show selective lockdown dialog"""
        dialog = tk.Toplevel(self.window)
        dialog.title("🔒 Configure Selective Lockdown")
        dialog.geometry("500x600")
        dialog.configure(bg=self.colors['surface'])
        dialog.transient(self.window)
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - 250
        y = (dialog.winfo_screenheight() // 2) - 300
        dialog.geometry(f"500x600+{x}+{y}")
        
        # Dialog header
        header = tk.Frame(dialog, bg=self.colors['primary'], height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(header, text="🔒 Selective Security Configuration", 
                font=("Segoe UI", 14, "bold"),
                bg=self.colors['primary'], fg=self.colors['card']).pack(pady=20)
        
        # Content
        content = tk.Frame(dialog, bg=self.colors['surface'])
        content.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Instructions
        tk.Label(content, 
                text="Select which security modules to activate during lockdown:",
                font=("Segoe UI", 11), bg=self.colors['surface'], 
                fg=self.colors['text_primary']).pack(pady=(0, 20))
        
        # Checkboxes for each security module
        self.selective_vars = {}
        
        modules = [
            ("keyboard", "🔤 Keyboard Protection", "Blocks keyboard shortcuts and dangerous keys"),
            ("mouse", "🖱️ Mouse Control", "Controls mouse buttons and prevents unwanted clicks"),
            ("internet", "🌐 Network Security", "Blocks internet access completely"),
            ("windows", "🪟 Window Guardian", "Prevents window manipulation and Alt+Tab"),
            ("processes", "🔍 Process Monitor", "Monitors and blocks unauthorized processes")
        ]
        
        for key, title, description in modules:
            # Module container
            module_frame = tk.Frame(content, bg=self.colors['card'], relief=tk.FLAT, bd=1)
            module_frame.pack(fill=tk.X, pady=(0, 10))
            
            # Module content
            module_content = tk.Frame(module_frame, bg=self.colors['card'])
            module_content.pack(fill=tk.X, padx=15, pady=12)
            
            # Checkbox and title
            header_frame = tk.Frame(module_content, bg=self.colors['card'])
            header_frame.pack(fill=tk.X, pady=(0, 5))
            
            var = tk.BooleanVar(value=True)
            self.selective_vars[key] = var
            
            check = tk.Checkbutton(header_frame, text=title, variable=var,
                                 font=("Segoe UI", 11, "bold"), bg=self.colors['card'],
                                 fg=self.colors['text_primary'], selectcolor=self.colors['card'],
                                 activebackground=self.colors['card'])
            check.pack(side=tk.LEFT)
            
            # Description
            desc_label = tk.Label(module_content, text=description, font=("Segoe UI", 9),
                                bg=self.colors['card'], fg=self.colors['text_secondary'],
                                wraplength=450, justify=tk.LEFT)
            desc_label.pack(anchor=tk.W)
        
        # Buttons
        button_frame = tk.Frame(content, bg=self.colors['surface'])
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        tk.Button(button_frame, text="🚀 START LOCKDOWN", 
                 command=lambda: self.start_selective_lockdown(dialog),
                 bg=self.colors['success'], fg=self.colors['card'],
                 font=("Segoe UI", 11, "bold"), relief=tk.FLAT, 
                 cursor='hand2', padx=20, pady=10).pack(side=tk.LEFT)
        
        tk.Button(button_frame, text="❌ Cancel", command=dialog.destroy,
                 bg=self.colors['danger'], fg=self.colors['card'],
                 font=("Segoe UI", 11, "bold"), relief=tk.FLAT, 
                 cursor='hand2', padx=20, pady=10).pack(side=tk.RIGHT)

    def start_selective_lockdown(self, dialog):
        """Start lockdown with selected options"""
        selected_options = {key: var.get() for key, var in self.selective_vars.items()}
        
        if not any(selected_options.values()):
            messagebox.showwarning("No Selection", 
                                 "Please select at least one security module to activate!")
            return
        
        selected_names = [key.title() for key, selected in selected_options.items() if selected]
        result = messagebox.askyesno("Confirm Selective Lockdown",
                                   f"Activate lockdown with these modules?\n\n" +
                                   "\n".join(f"✓ {name}" for name in selected_names))
        
        if result:
            dialog.destroy()
            try:
                self.security_manager.start_exam_mode(selected_options)
                self.start_btn.config(state=tk.DISABLED)
                self.stop_btn.config(state=tk.NORMAL)
                self.refresh_status()
                
                messagebox.showinfo("🔒 LOCKDOWN ACTIVATED",
                                  f"Selective lockdown active with:\n\n" +
                                  "\n".join(f"✅ {name}" for name in selected_names))
            except Exception as e:
                messagebox.showerror("Error", f"Failed to activate lockdown: {str(e)}")

    # Keep all other original methods exactly as they were
    def switch_to_monitor(self):
        self.notebook.select(1)
    
    def switch_to_settings(self):
        self.notebook.select(2)
    
    def stop_exam_mode(self):
        if messagebox.askyesno("Stop Exam Mode", 
                              "Are you sure you want to stop exam mode?\n\n"
                              "This will deactivate all security features."):
            try:
                self.security_manager.stop_exam_mode()
                self.start_btn.config(state=tk.NORMAL)
                self.stop_btn.config(state=tk.DISABLED)
                self.refresh_status()
                messagebox.showinfo("Success", "Exam mode has been deactivated.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to stop exam mode: {str(e)}")

    def emergency_stop(self):
        if messagebox.askyesno("Emergency Stop", 
                              "EMERGENCY STOP - This will immediately terminate all security features!\n\n"
                              "Are you absolutely sure?"):
            try:
                self.security_manager.emergency_stop()
                self.start_btn.config(state=tk.NORMAL)
                self.stop_btn.config(state=tk.DISABLED)
                self.refresh_status()
                messagebox.showinfo("Emergency Stop", "All security features have been emergency stopped.")
            except Exception as e:
                messagebox.showerror("Error", f"Emergency stop failed: {str(e)}")

    def show_mouse_controls(self):
        messagebox.showinfo("Mouse Controls", "Mouse controls dialog - Feature coming soon!")
    
    def show_network_controls(self):
        messagebox.showinfo("Network Controls", "Network controls dialog - Feature coming soon!")
    
    def show_window_controls(self):
        messagebox.showinfo("Window Controls", "Window controls dialog - Feature coming soon!")

    def create_keyboard_settings(self, parent):
        # Keyboard settings section
        kb_frame = tk.LabelFrame(parent, text="🔤 Keyboard Protection Settings", 
                               font=("Segoe UI", 12, "bold"),
                               bg=self.colors['surface'], fg=self.colors['text_primary'])
        kb_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(kb_frame, text="Configure keyboard blocking settings",
                bg=self.colors['surface'], fg=self.colors['text_secondary']).pack(pady=10)

    def create_mouse_settings(self, parent):
        # Mouse settings section
        mouse_frame = tk.LabelFrame(parent, text="🖱️ Mouse Control Settings", 
                                  font=("Segoe UI", 12, "bold"),
                                  bg=self.colors['surface'], fg=self.colors['text_primary'])
        mouse_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(mouse_frame, text="Configure mouse blocking settings",
                bg=self.colors['surface'], fg=self.colors['text_secondary']).pack(pady=10)

    def create_network_settings(self, parent):
        # Network settings section
        net_frame = tk.LabelFrame(parent, text="🌐 Network Security Settings", 
                                font=("Segoe UI", 12, "bold"),
                                bg=self.colors['surface'], fg=self.colors['text_primary'])
        net_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(net_frame, text="Configure network blocking settings",
                bg=self.colors['surface'], fg=self.colors['text_secondary']).pack(pady=10)

    def refresh_logs(self):
        """Refresh the logs display"""
        try:
            logs = self.db_manager.get_recent_logs(limit=100)
            self.logs_text.delete(1.0, tk.END)
            
            for log in logs:
                timestamp = log.get('timestamp', 'N/A')
                action = log.get('action', 'N/A')
                details = log.get('details', 'N/A')
                log_line = f"[{timestamp}] {action}: {details}\n"
                self.logs_text.insert(tk.END, log_line)
            
            self.logs_text.see(tk.END)
        except Exception as e:
            self.logs_text.delete(1.0, tk.END)
            self.logs_text.insert(tk.END, f"Error loading logs: {str(e)}")

    def clear_logs(self):
        if messagebox.askyesno("Clear Logs", "Clear all security logs?"):
            try:
                self.db_manager.clear_logs()
                self.logs_text.delete(1.0, tk.END)
                self.logs_text.insert(tk.END, "All logs cleared.\n")
                messagebox.showinfo("Success", "Logs cleared successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to clear logs: {str(e)}")

    def export_logs(self):
        messagebox.showinfo("Export", "Log export feature - Coming soon!")

    def start_auto_refresh(self):
        """Start automatic status refresh"""
        def refresh_loop():
            while hasattr(self, 'window') and self.window.winfo_exists():
                try:
                    self.window.after(0, self.refresh_status)
                    threading.Event().wait(2)
                except:
                    break
        
        refresh_thread = threading.Thread(target=refresh_loop, daemon=True)
        refresh_thread.start()

    def on_close(self):
        """Handle window close"""
        if messagebox.askyesno("Close Admin Panel", 
                              "Close the admin panel?\n\n"
                              "The system will continue running in the background."):
            self.window.withdraw()
