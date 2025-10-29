"""
Enhanced Controls Module for Exam Shield Premium
Provides granular control over window and mouse protection features
"""

import tkinter as tk
from tkinter import messagebox, simpledialog
import threading
from datetime import datetime

class EnhancedControls:
    def __init__(self, parent, security_manager, db_manager):
        self.parent = parent
        self.security_manager = security_manager
        self.db_manager = db_manager
        
        # Premium colors matching admin panel
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
            'text_secondary': '#7f8c8d'
        }

    def show_enhanced_window_controls(self):
        """Show enhanced window protection controls"""
        window = tk.Toplevel(self.parent)
        window.title("🏠 Enhanced Window Protection Controls")
        window.geometry("600x500")
        window.configure(bg=self.colors['surface'])
        window.transient(self.parent)
        window.resizable(True, False)
        
        # Center window
        window.update_idletasks()
        x = (window.winfo_screenwidth() // 2) - 300
        y = (window.winfo_screenheight() // 2) - 250
        window.geometry(f"600x500+{x}+{y}")
        
        # Header
        header = tk.Frame(window, bg=self.colors['primary'], height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(header, text="🏠 Enhanced Window Protection System", 
                font=("Segoe UI", 14, "bold"), bg=self.colors['primary'], 
                fg=self.colors['card']).pack(pady=20)
        
        # Content frame
        content = tk.Frame(window, bg=self.colors['surface'])
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Current status card
        status_card = tk.Frame(content, bg=self.colors['card'], relief=tk.FLAT, bd=1)
        status_card.pack(fill=tk.X, pady=(0, 15))
        
        status_header = tk.Frame(status_card, bg=self.colors['info'], height=35)
        status_header.pack(fill=tk.X)
        status_header.pack_propagate(False)
        
        tk.Label(status_header, text="📊 Current Status", font=("Segoe UI", 11, "bold"),
                bg=self.colors['info'], fg=self.colors['card']).pack(pady=8)
        
        status_content = tk.Frame(status_card, bg=self.colors['card'])
        status_content.pack(fill=tk.X, padx=15, pady=10)
        
        # Status display
        is_active = self.security_manager.window_manager.is_active
        status_text = "🔄 ACTIVE" if is_active else "⚫ INACTIVE"
        status_color = self.colors['success'] if is_active else self.colors['text_secondary']
        
        tk.Label(status_content, text=f"Protection Status: {status_text}", 
                font=("Segoe UI", 10, "bold"), bg=self.colors['card'], 
                fg=status_color).pack(anchor=tk.W)
        
        if is_active:
            protected_count = len(self.security_manager.window_manager.protected_windows)
            tk.Label(status_content, text=f"Protected Windows: {protected_count}", 
                    font=("Segoe UI", 9), bg=self.colors['card'], 
                    fg=self.colors['text_primary']).pack(anchor=tk.W, pady=(2, 0))
        
        # Configuration card
        config_card = tk.Frame(content, bg=self.colors['card'], relief=tk.FLAT, bd=1)
        config_card.pack(fill=tk.X, pady=(0, 15))
        
        config_header = tk.Frame(config_card, bg=self.colors['warning'], height=35)
        config_header.pack(fill=tk.X)
        config_header.pack_propagate(False)
        
        tk.Label(config_header, text="⚙️ Protection Configuration", font=("Segoe UI", 11, "bold"),
                bg=self.colors['warning'], fg=self.colors['card']).pack(pady=8)
        
        config_content = tk.Frame(config_card, bg=self.colors['card'])
        config_content.pack(fill=tk.X, padx=15, pady=15)
        
        # Configuration options
        current_config = self.security_manager.window_manager.config
        
        self.prevent_close_var = tk.BooleanVar(value=current_config.get('prevent_close', True))
        tk.Checkbutton(config_content, text="❌ Disable Close Button", 
                      variable=self.prevent_close_var, font=("Segoe UI", 10),
                      bg=self.colors['card'], fg=self.colors['text_primary'],
                      selectcolor=self.colors['card'], activebackground=self.colors['card']).pack(anchor=tk.W)
        
        self.prevent_minimize_var = tk.BooleanVar(value=current_config.get('prevent_minimize', True))
        tk.Checkbutton(config_content, text="➖ Disable Minimize Button", 
                      variable=self.prevent_minimize_var, font=("Segoe UI", 10),
                      bg=self.colors['card'], fg=self.colors['text_primary'],
                      selectcolor=self.colors['card'], activebackground=self.colors['card']).pack(anchor=tk.W)
        
        self.prevent_maximize_var = tk.BooleanVar(value=current_config.get('prevent_maximize', True))
        tk.Checkbutton(config_content, text="⬜ Disable Maximize Button", 
                      variable=self.prevent_maximize_var, font=("Segoe UI", 10),
                      bg=self.colors['card'], fg=self.colors['text_primary'],
                      selectcolor=self.colors['card'], activebackground=self.colors['card']).pack(anchor=tk.W)
        
        # Controls card
        controls_card = tk.Frame(content, bg=self.colors['card'], relief=tk.FLAT, bd=1)
        controls_card.pack(fill=tk.X, pady=(0, 15))
        
        controls_header = tk.Frame(controls_card, bg=self.colors['success'], height=35)
        controls_header.pack(fill=tk.X)
        controls_header.pack_propagate(False)
        
        tk.Label(controls_header, text="🎮 Control Actions", font=("Segoe UI", 11, "bold"),
                bg=self.colors['success'], fg=self.colors['card']).pack(pady=8)
        
        controls_content = tk.Frame(controls_card, bg=self.colors['card'])
        controls_content.pack(fill=tk.X, padx=15, pady=15)
        
        # Action buttons
        btn_frame = tk.Frame(controls_content, bg=self.colors['card'])
        btn_frame.pack(fill=tk.X)
        
        if not is_active:
            tk.Button(btn_frame, text="🚀 Start Protection",
                     command=lambda: self.start_window_protection(window),
                     bg=self.colors['success'], fg=self.colors['card'],
                     font=("Segoe UI", 10, "bold"), relief=tk.FLAT, 
                     cursor='hand2', padx=15, pady=8).pack(side=tk.LEFT, padx=(0, 10))
        else:
            tk.Button(btn_frame, text="🛑 Stop Protection",
                     command=lambda: self.stop_window_protection(window),
                     bg=self.colors['danger'], fg=self.colors['card'],
                     font=("Segoe UI", 10, "bold"), relief=tk.FLAT, 
                     cursor='hand2', padx=15, pady=8).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(btn_frame, text="⚙️ Apply Config",
                 command=lambda: self.apply_window_config(window),
                 bg=self.colors['warning'], fg=self.colors['card'],
                 font=("Segoe UI", 10, "bold"), relief=tk.FLAT, 
                 cursor='hand2', padx=15, pady=8).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(btn_frame, text="🔄 Refresh",
                 command=lambda: [window.destroy(), self.show_enhanced_window_controls()],
                 bg=self.colors['info'], fg=self.colors['card'],
                 font=("Segoe UI", 10, "bold"), relief=tk.FLAT, 
                 cursor='hand2', padx=15, pady=8).pack(side=tk.RIGHT)

    def show_enhanced_mouse_controls(self):
        """Show enhanced mouse protection controls"""
        window = tk.Toplevel(self.parent)
        window.title("🕰 Enhanced Mouse Protection Controls")
        window.geometry("650x550")
        window.configure(bg=self.colors['surface'])
        window.transient(self.parent)
        window.resizable(True, False)
        
        # Center window
        window.update_idletasks()
        x = (window.winfo_screenwidth() // 2) - 325
        y = (window.winfo_screenheight() // 2) - 275
        window.geometry(f"650x550+{x}+{y}")
        
        # Header
        header = tk.Frame(window, bg=self.colors['info'], height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(header, text="🕰 Enhanced Mouse Protection System", 
                font=("Segoe UI", 14, "bold"), bg=self.colors['info'], 
                fg=self.colors['card']).pack(pady=20)
        
        # Content frame
        content = tk.Frame(window, bg=self.colors['surface'])
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Status card
        status_card = tk.Frame(content, bg=self.colors['card'], relief=tk.FLAT, bd=1)
        status_card.pack(fill=tk.X, pady=(0, 15))
        
        status_header = tk.Frame(status_card, bg=self.colors['primary'], height=35)
        status_header.pack(fill=tk.X)
        status_header.pack_propagate(False)
        
        tk.Label(status_header, text="📊 Current Status", font=("Segoe UI", 11, "bold"),
                bg=self.colors['primary'], fg=self.colors['card']).pack(pady=8)
        
        status_content = tk.Frame(status_card, bg=self.colors['card'])
        status_content.pack(fill=tk.X, padx=15, pady=10)
        
        # Status display
        mouse_status = self.security_manager.mouse_manager.get_status()
        is_active = mouse_status['active']
        status_text = "🔄 ACTIVE" if is_active else "⚫ INACTIVE"
        status_color = self.colors['success'] if is_active else self.colors['text_secondary']
        
        tk.Label(status_content, text=f"Protection Status: {status_text}", 
                font=("Segoe UI", 10, "bold"), bg=self.colors['card'], 
                fg=status_color).pack(anchor=tk.W)
        
        if is_active:
            blocked_buttons = ', '.join(mouse_status['blocked_buttons'])
            tk.Label(status_content, text=f"Blocked Buttons: {blocked_buttons}", 
                    font=("Segoe UI", 9), bg=self.colors['card'], 
                    fg=self.colors['text_primary']).pack(anchor=tk.W, pady=(2, 0))
            
            block_mode = "All Clicks" if mouse_status.get('block_all_mode', False) else "Selective"
            tk.Label(status_content, text=f"Blocking Mode: {block_mode}", 
                    font=("Segoe UI", 9), bg=self.colors['card'], 
                    fg=self.colors['text_primary']).pack(anchor=tk.W, pady=(2, 0))
        
        # Configuration card
        config_card = tk.Frame(content, bg=self.colors['card'], relief=tk.FLAT, bd=1)
        config_card.pack(fill=tk.X, pady=(0, 15))
        
        config_header = tk.Frame(config_card, bg=self.colors['warning'], height=35)
        config_header.pack(fill=tk.X)
        config_header.pack_propagate(False)
        
        tk.Label(config_header, text="⚙️ Blocking Configuration", font=("Segoe UI", 11, "bold"),
                bg=self.colors['warning'], fg=self.colors['card']).pack(pady=8)
        
        config_content = tk.Frame(config_card, bg=self.colors['card'])
        config_content.pack(fill=tk.X, padx=15, pady=15)
        
        # Blocking mode selection
        tk.Label(config_content, text="Blocking Mode:", font=("Segoe UI", 10, "bold"),
                bg=self.colors['card'], fg=self.colors['text_primary']).pack(anchor=tk.W)
        
        self.block_mode_var = tk.StringVar(value="selective")
        if mouse_status.get('block_all_mode', False):
            self.block_mode_var.set("all")
        
        mode_frame = tk.Frame(config_content, bg=self.colors['card'])
        mode_frame.pack(anchor=tk.W, pady=(5, 10))
        
        tk.Radiobutton(mode_frame, text="🎯 Selective Button Blocking", 
                      variable=self.block_mode_var, value="selective",
                      font=("Segoe UI", 9), bg=self.colors['card'], 
                      fg=self.colors['text_primary'], selectcolor=self.colors['card'],
                      activebackground=self.colors['card']).pack(anchor=tk.W)
        
        tk.Radiobutton(mode_frame, text="🙫 Block All Mouse Clicks", 
                      variable=self.block_mode_var, value="all",
                      font=("Segoe UI", 9), bg=self.colors['card'], 
                      fg=self.colors['text_primary'], selectcolor=self.colors['card'],
                      activebackground=self.colors['card']).pack(anchor=tk.W)
        
        # Button selection (for selective mode)
        tk.Label(config_content, text="Buttons to Block (Selective Mode):", font=("Segoe UI", 10, "bold"),
                bg=self.colors['card'], fg=self.colors['text_primary']).pack(anchor=tk.W, pady=(10, 0))
        
        button_frame = tk.Frame(config_content, bg=self.colors['card'])
        button_frame.pack(anchor=tk.W, pady=(5, 0))
        
        # Button checkboxes
        current_blocked = mouse_status['blocked_buttons']
        self.button_vars = {}
        
        buttons = ['left', 'right', 'middle', 'x1', 'x2', 'side', 'back', 'forward']
        for i, button in enumerate(buttons):
            var = tk.BooleanVar(value=button in [b.lower() for b in current_blocked])
            self.button_vars[button] = var
            
            row = i // 4
            col = i % 4
            
            if col == 0:
                row_frame = tk.Frame(button_frame, bg=self.colors['card'])
                row_frame.pack(anchor=tk.W, pady=1)
            
            tk.Checkbutton(row_frame, text=button.title(), variable=var,
                          font=("Segoe UI", 9), bg=self.colors['card'],
                          fg=self.colors['text_primary'], selectcolor=self.colors['card'],
                          activebackground=self.colors['card']).pack(side=tk.LEFT, padx=(0, 20))
        
        # Controls card
        controls_card = tk.Frame(content, bg=self.colors['card'], relief=tk.FLAT, bd=1)
        controls_card.pack(fill=tk.X)
        
        controls_header = tk.Frame(controls_card, bg=self.colors['success'], height=35)
        controls_header.pack(fill=tk.X)
        controls_header.pack_propagate(False)
        
        tk.Label(controls_header, text="🎮 Control Actions", font=("Segoe UI", 11, "bold"),
                bg=self.colors['success'], fg=self.colors['card']).pack(pady=8)
        
        controls_content = tk.Frame(controls_card, bg=self.colors['card'])
        controls_content.pack(fill=tk.X, padx=15, pady=15)
        
        # Action buttons
        btn_frame1 = tk.Frame(controls_content, bg=self.colors['card'])
        btn_frame1.pack(fill=tk.X, pady=(0, 5))
        
        if not is_active:
            tk.Button(btn_frame1, text="🚀 Start Protection",
                     command=lambda: self.start_mouse_protection(window),
                     bg=self.colors['success'], fg=self.colors['card'],
                     font=("Segoe UI", 10, "bold"), relief=tk.FLAT, 
                     cursor='hand2', padx=15, pady=8).pack(side=tk.LEFT, padx=(0, 10))
        else:
            tk.Button(btn_frame1, text="🛑 Stop Protection",
                     command=lambda: self.stop_mouse_protection(window),
                     bg=self.colors['danger'], fg=self.colors['card'],
                     font=("Segoe UI", 10, "bold"), relief=tk.FLAT, 
                     cursor='hand2', padx=15, pady=8).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(btn_frame1, text="⚙️ Apply Config",
                 command=lambda: self.apply_mouse_config(window),
                 bg=self.colors['warning'], fg=self.colors['card'],
                 font=("Segoe UI", 10, "bold"), relief=tk.FLAT, 
                 cursor='hand2', padx=15, pady=8).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(btn_frame1, text="🎯 Test Blocking",
                 command=self.test_mouse_blocking,
                 bg=self.colors['accent'], fg=self.colors['text_primary'],
                 font=("Segoe UI", 10, "bold"), relief=tk.FLAT, 
                 cursor='hand2', padx=15, pady=8).pack(side=tk.LEFT)
        
        tk.Button(btn_frame1, text="🔄 Refresh",
                 command=lambda: [window.destroy(), self.show_enhanced_mouse_controls()],
                 bg=self.colors['info'], fg=self.colors['card'],
                 font=("Segoe UI", 10, "bold"), relief=tk.FLAT, 
                 cursor='hand2', padx=15, pady=8).pack(side=tk.RIGHT)

    def start_window_protection(self, window):
        """Start window protection with current config"""
        self.apply_window_config(window, start_after=True)

    def stop_window_protection(self, window):
        """Stop window protection"""
        self.security_manager.window_manager.stop_window_protection()
        messagebox.showinfo("✅ Success", "Window protection has been stopped.\nAll window buttons restored.")
        window.destroy()
        self.show_enhanced_window_controls()

    def apply_window_config(self, window, start_after=False):
        """Apply window protection configuration"""
        new_config = {
            'prevent_close': self.prevent_close_var.get(),
            'prevent_minimize': self.prevent_minimize_var.get(), 
            'prevent_maximize': self.prevent_maximize_var.get(),
            'disable_window_buttons': True
        }
        
        self.security_manager.window_manager.config.update(new_config)
        
        if start_after:
            self.security_manager.window_manager.start_window_protection(new_config)
        
        messagebox.showinfo("✅ Success", "Window protection configuration applied successfully!")
        window.destroy()
        self.show_enhanced_window_controls()

    def start_mouse_protection(self, window):
        """Start mouse protection with current config"""
        self.apply_mouse_config(window, start_after=True)

    def stop_mouse_protection(self, window):
        """Stop mouse protection"""
        self.security_manager.mouse_manager.stop_blocking()
        messagebox.showinfo("✅ Success", "Mouse protection has been stopped.\nAll mouse buttons restored.")
        window.destroy()
        self.show_enhanced_mouse_controls()

    def apply_mouse_config(self, window, start_after=False):
        """Apply mouse protection configuration"""
        # Set blocking mode
        block_all = self.block_mode_var.get() == "all"
        self.security_manager.mouse_manager.set_block_all_clicks(block_all)
        
        # Set blocked buttons for selective mode
        if not block_all:
            selected_buttons = [button for button, var in self.button_vars.items() if var.get()]
            self.security_manager.mouse_manager.blocked_buttons = selected_buttons
        
        if start_after:
            self.security_manager.mouse_manager.start_blocking()
        
        mode_text = "all clicks" if block_all else f"selective buttons: {', '.join(self.security_manager.mouse_manager.blocked_buttons)}"
        messagebox.showinfo("✅ Success", f"Mouse protection configured to block {mode_text}")
        
        window.destroy()
        self.show_enhanced_mouse_controls()

    def test_mouse_blocking(self):
        """Test mouse blocking functionality"""
        if not self.security_manager.mouse_manager.is_active:
            messagebox.showwarning("⚠️ Warning", "Mouse protection is not active. Start protection first to test blocking.")
            return
            
        test_window = tk.Toplevel(self.parent)
        test_window.title("🎯 Mouse Blocking Test")
        test_window.geometry("400x300")
        test_window.configure(bg=self.colors['surface'])
        test_window.transient(self.parent)
        
        # Center test window
        test_window.update_idletasks()
        x = (test_window.winfo_screenwidth() // 2) - 200
        y = (test_window.winfo_screenheight() // 2) - 150
        test_window.geometry(f"400x300+{x}+{y}")
        
        tk.Label(test_window, text="🎯 Mouse Blocking Test", 
                font=("Segoe UI", 14, "bold"), bg=self.colors['surface'], 
                fg=self.colors['text_primary']).pack(pady=20)
        
        tk.Label(test_window, text="Try clicking different mouse buttons in this area.", 
                font=("Segoe UI", 10), bg=self.colors['surface'], 
                fg=self.colors['text_secondary']).pack(pady=10)
        
        mouse_status = self.security_manager.mouse_manager.get_status()
        if mouse_status.get('block_all_mode', False):
            status_text = "All mouse clicks are blocked"
        else:
            blocked = ', '.join(mouse_status['blocked_buttons'])
            status_text = f"Blocked buttons: {blocked}"
        
        tk.Label(test_window, text=status_text, 
                font=("Segoe UI", 9, "bold"), bg=self.colors['surface'], 
                fg=self.colors['info']).pack(pady=5)
        
        tk.Label(test_window, text="Mouse movement should work normally.", 
                font=("Segoe UI", 9), bg=self.colors['surface'], 
                fg=self.colors['success']).pack(pady=5)
        
        tk.Button(test_window, text="Close Test", command=test_window.destroy,
                 bg=self.colors['primary'], fg=self.colors['card'],
                 font=("Segoe UI", 10, "bold"), relief=tk.FLAT, 
                 cursor='hand2', padx=15, pady=8).pack(pady=20)