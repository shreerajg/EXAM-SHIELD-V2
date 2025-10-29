# Import the enhanced controls at the top of admin_panel.py
from enhanced_controls import EnhancedControls

# Then update the show_mouse_controls method:
def show_mouse_controls(self):
    """Show enhanced mouse protection controls"""
    try:
        enhanced_controls = EnhancedControls(self.window, self.security_manager, self.db_manager)
        enhanced_controls.show_enhanced_mouse_controls()
    except Exception as e:
        # Fallback to simple controls if enhanced controls fail
        print(f"Enhanced controls unavailable: {e}")
        self._show_simple_mouse_controls()

def show_window_controls(self):
    """Show enhanced window protection controls"""
    try:
        enhanced_controls = EnhancedControls(self.window, self.security_manager, self.db_manager)
        enhanced_controls.show_enhanced_window_controls()
    except Exception as e:
        # Fallback to simple controls if enhanced controls fail
        print(f"Enhanced controls unavailable: {e}")
        self._show_simple_window_controls()

def _show_simple_mouse_controls(self):
    """Simple mouse controls as fallback"""
    mouse_window = tk.Toplevel(self.window)
    mouse_window.title("🕰 Mouse Security Controls")
    mouse_window.geometry("600x450")
    mouse_window.configure(bg=self.colors['surface'])
    mouse_window.transient(self.window)
    
    # Center window
    mouse_window.update_idletasks()
    x = (mouse_window.winfo_screenwidth() // 2) - 300
    y = (mouse_window.winfo_screenheight() // 2) - 225
    mouse_window.geometry(f"600x450+{x}+{y}")
    
    # Header
    header = tk.Frame(mouse_window, bg=self.colors['info'], height=60)
    header.pack(fill=tk.X)
    header.pack_propagate(False)
    
    tk.Label(header, text="🕰 Mouse Button Blocking System", 
            font=("Segoe UI", 14, "bold"), bg=self.colors['info'], 
            fg=self.colors['card']).pack(pady=20)
    
    # Content
    content = tk.Frame(mouse_window, bg=self.colors['surface'])
    content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    # Status display
    status_card = tk.Frame(content, bg=self.colors['card'], relief=tk.FLAT, bd=1)
    status_card.pack(fill=tk.X, pady=(0, 15))
    
    status_header = tk.Frame(status_card, bg=self.colors['primary'], height=35)
    status_header.pack(fill=tk.X)
    status_header.pack_propagate(False)
    
    tk.Label(status_header, text="📊 Current Status", font=("Segoe UI", 11, "bold"),
            bg=self.colors['primary'], fg=self.colors['card']).pack(pady=8)
    
    status_content = tk.Frame(status_card, bg=self.colors['card'])
    status_content.pack(fill=tk.X, padx=15, pady=10)
    
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
        
        block_mode = "All Clicks" if mouse_status.get('block_all_clicks', False) else "Selective"
        tk.Label(status_content, text=f"Blocking Mode: {block_mode}", 
                font=("Segoe UI", 9), bg=self.colors['card'], 
                fg=self.colors['text_primary']).pack(anchor=tk.W, pady=(2, 0))
    
    # Quick controls
    controls_card = tk.Frame(content, bg=self.colors['card'], relief=tk.FLAT, bd=1)
    controls_card.pack(fill=tk.X, pady=(0, 15))
    
    controls_header = tk.Frame(controls_card, bg=self.colors['success'], height=35)
    controls_header.pack(fill=tk.X)
    controls_header.pack_propagate(False)
    
    tk.Label(controls_header, text="🎮 Quick Controls", font=("Segoe UI", 11, "bold"),
            bg=self.colors['success'], fg=self.colors['card']).pack(pady=8)
    
    controls_content = tk.Frame(controls_card, bg=self.colors['card'])
    controls_content.pack(fill=tk.X, padx=15, pady=15)
    
    # Control buttons
    btn_frame = tk.Frame(controls_content, bg=self.colors['card'])
    btn_frame.pack(fill=tk.X, pady=(0, 10))
    
    if not is_active:
        tk.Button(btn_frame, text="🚀 Start Blocking",
                 command=lambda: [self.security_manager.mouse_manager.start_blocking(), 
                                mouse_window.destroy(), self.show_mouse_controls()],
                 bg=self.colors['success'], fg=self.colors['card'],
                 font=("Segoe UI", 10, "bold"), relief=tk.FLAT, 
                 cursor='hand2', padx=15, pady=8).pack(side=tk.LEFT, padx=(0, 10))
    else:
        tk.Button(btn_frame, text="🛑 Stop Blocking",
                 command=lambda: [self.security_manager.mouse_manager.stop_blocking(), 
                                mouse_window.destroy(), self.show_mouse_controls()],
                 bg=self.colors['danger'], fg=self.colors['card'],
                 font=("Segoe UI", 10, "bold"), relief=tk.FLAT, 
                 cursor='hand2', padx=15, pady=8).pack(side=tk.LEFT, padx=(0, 10))
    
    tk.Button(btn_frame, text="🎯 Test Blocking",
             command=self.security_manager.mouse_manager.test_blocking,
             bg=self.colors['accent'], fg=self.colors['text_primary'],
             font=("Segoe UI", 10, "bold"), relief=tk.FLAT, 
             cursor='hand2', padx=15, pady=8).pack(side=tk.LEFT, padx=(0, 10))
    
    tk.Button(btn_frame, text="🔄 Refresh",
             command=lambda: [mouse_window.destroy(), self.show_mouse_controls()],
             bg=self.colors['info'], fg=self.colors['card'],
             font=("Segoe UI", 10, "bold"), relief=tk.FLAT, 
             cursor='hand2', padx=15, pady=8).pack(side=tk.RIGHT)
    
    # Configuration section
    config_card = tk.Frame(content, bg=self.colors['card'], relief=tk.FLAT, bd=1)
    config_card.pack(fill=tk.X)
    
    config_header = tk.Frame(config_card, bg=self.colors['warning'], height=35)
    config_header.pack(fill=tk.X)
    config_header.pack_propagate(False)
    
    tk.Label(config_header, text="⚙️ Quick Configuration", font=("Segoe UI", 11, "bold"),
            bg=self.colors['warning'], fg=self.colors['card']).pack(pady=8)
    
    config_content = tk.Frame(config_card, bg=self.colors['card'])
    config_content.pack(fill=tk.X, padx=15, pady=15)
    
    # Button selection
    tk.Label(config_content, text="Select buttons to block:", font=("Segoe UI", 10, "bold"),
            bg=self.colors['card'], fg=self.colors['text_primary']).pack(anchor=tk.W)
    
    button_frame = tk.Frame(config_content, bg=self.colors['card'])
    button_frame.pack(anchor=tk.W, pady=(5, 10))
    
    # Button checkboxes
    current_blocked = mouse_status['blocked_buttons']
    self.button_vars = {}
    
    buttons = ['left', 'right', 'middle', 'x1', 'x2']
    for i, button in enumerate(buttons):
        var = tk.BooleanVar(value=button in current_blocked)
        self.button_vars[button] = var
        
        tk.Checkbutton(button_frame, text=button.capitalize(), variable=var,
                      font=("Segoe UI", 9), bg=self.colors['card'],
                      fg=self.colors['text_primary'], selectcolor=self.colors['card'],
                      activebackground=self.colors['card']).pack(side=tk.LEFT, padx=(0, 15))
    
    # Block all option
    self.block_all_var = tk.BooleanVar(value=mouse_status.get('block_all_clicks', False))
    tk.Checkbutton(config_content, text="🚫 Block ALL mouse clicks", 
                  variable=self.block_all_var, font=("Segoe UI", 10, "bold"),
                  bg=self.colors['card'], fg=self.colors['danger'],
                  selectcolor=self.colors['card'], activebackground=self.colors['card']).pack(anchor=tk.W, pady=(5, 10))
    
    # Apply button
    tk.Button(config_content, text="⚙️ Apply Configuration",
             command=lambda: self._apply_mouse_config_simple(mouse_window),
             bg=self.colors['primary'], fg=self.colors['card'],
             font=("Segoe UI", 10, "bold"), relief=tk.FLAT, 
             cursor='hand2', padx=20, pady=8).pack(pady=(10, 0))

def _apply_mouse_config_simple(self, window):
    """Apply simple mouse configuration"""
    try:
        # Set block all mode
        self.security_manager.mouse_manager.set_block_all_clicks(self.block_all_var.get())
        
        # Set individual blocked buttons
        if not self.block_all_var.get():
            selected_buttons = [button for button, var in self.button_vars.items() if var.get()]
            self.security_manager.mouse_manager.blocked_buttons = selected_buttons
        
        if self.block_all_var.get():
            messagebox.showinfo("✅ Applied", "Configuration applied: ALL mouse clicks will be blocked")
        else:
            blocked_list = ', '.join([button for button, var in self.button_vars.items() if var.get()])
            messagebox.showinfo("✅ Applied", f"Configuration applied: Blocking buttons: {blocked_list}")
        
        window.destroy()
        self.show_mouse_controls()
        
    except Exception as e:
        messagebox.showerror("❌ Error", f"Failed to apply configuration: {str(e)}")

def _show_simple_window_controls(self):
    """Simple window controls as fallback"""
    window_control = tk.Toplevel(self.window)
    window_control.title("🏠 Window Guardian Controls")
    window_control.geometry("500x400")
    window_control.configure(bg=self.colors['surface'])
    window_control.transient(self.window)
    
    # Premium header
    header = tk.Frame(window_control, bg=self.colors['primary'], height=60)
    header.pack(fill=tk.X)
    header.pack_propagate(False)
    
    tk.Label(header, text="🏠 Window Protection System", 
            font=("Segoe UI", 14, "bold"), bg=self.colors['primary'], 
            fg=self.colors['card']).pack(pady=20)
    
    # Content
    content = tk.Frame(window_control, bg=self.colors['surface'])
    content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    is_active = self.security_manager.window_manager.is_active
    status = "🔄 ACTIVE" if is_active else "⚫ INACTIVE"
    tk.Label(content, text=f"Status: {status}", font=("Segoe UI", 12, "bold"),
            bg=self.colors['surface'], fg=self.colors['text_primary']).pack(pady=10)

    control_frame = tk.Frame(content, bg=self.colors['card'])
    control_frame.pack(pady=20, fill=tk.BOTH, expand=True)
    
    if not is_active:
        tk.Button(control_frame, text="🚀 Start Window Protection",
                 command=lambda: [self.security_manager.window_manager.start_window_protection(), 
                                window_control.destroy()],
                 bg=self.colors['success'], fg=self.colors['card'],
                 font=("Segoe UI", 11, "bold"), relief=tk.FLAT, 
                 cursor='hand2', padx=20, pady=10).pack(pady=20)
    else:
        tk.Button(control_frame, text="🛑 Stop Window Protection",
                 command=lambda: [self.security_manager.window_manager.stop_window_protection(), 
                                window_control.destroy()],
                 bg=self.colors['danger'], fg=self.colors['card'],
                 font=("Segoe UI", 11, "bold"), relief=tk.FLAT, 
                 cursor='hand2', padx=20, pady=10).pack(pady=20)