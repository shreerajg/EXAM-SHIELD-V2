# NOTE: This is a partial update to fix the specific control methods in admin_panel.py
# I'll add the fixed methods to the existing file

# Add these fixed methods to the AdminPanel class:

def show_mouse_controls(self):
    """FIXED: Show mouse controls with proper integration"""
    mouse_window = tk.Toplevel(self.window)
    mouse_window.title("🖱️ Mouse Security Controls")
    mouse_window.geometry("600x500")
    mouse_window.configure(bg=self.colors['surface'])
    mouse_window.transient(self.window)
    
    # Center window
    mouse_window.update_idletasks()
    x = (mouse_window.winfo_screenwidth() // 2) - 300
    y = (mouse_window.winfo_screenheight() // 2) - 250
    mouse_window.geometry(f"600x500+{x}+{y}")
    
    # Premium header
    header = tk.Frame(mouse_window, bg=self.colors['info'], height=60)
    header.pack(fill=tk.X)
    header.pack_propagate(False)
    
    tk.Label(header, text="🖱️ Mouse Button Blocking System", 
            font=("Segoe UI", 14, "bold"), bg=self.colors['info'], 
            fg=self.colors['card']).pack(pady=20)
    
    # Content
    content = tk.Frame(mouse_window, bg=self.colors['surface'])
    content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    # Status display
    status_frame = tk.Frame(content, bg=self.colors['card'], pady=15)
    status_frame.pack(fill=tk.X, pady=(0, 20))
    
    # Get real status from mouse manager
    is_active = self.security_manager.mouse_manager.is_active
    status_text = "🟢 ACTIVE" if is_active else "🔴 INACTIVE"
    status_color = self.colors['success'] if is_active else self.colors['danger']
    
    tk.Label(status_frame, text=f"Status: {status_text}", font=("Segoe UI", 12, "bold"),
            bg=self.colors['card'], fg=status_color).pack(pady=10)
    
    # Get blocked buttons info
    try:
        blocked_info = self.security_manager.mouse_manager.get_status()
        blocked_buttons_text = ", ".join(blocked_info.get('blocked_buttons', []))
        if not blocked_buttons_text:
            blocked_buttons_text = "None"
    except:
        blocked_buttons_text = "Error getting status"
    
    tk.Label(status_frame, text=f"Blocked Buttons: {blocked_buttons_text}",
            font=("Segoe UI", 10), bg=self.colors['card'], 
            fg=self.colors['text_primary']).pack(pady=5)
    
    # Control buttons
    control_frame = tk.Frame(content, bg=self.colors['card'], pady=20)
    control_frame.pack(fill=tk.X, pady=(0, 20))
    
    # Create control buttons based on current state
    if not is_active:
        activate_btn = tk.Button(control_frame, text="🚀 Activate Mouse Blocking",
                               command=lambda: self._toggle_mouse_and_close(True, mouse_window),
                               bg=self.colors['success'], fg=self.colors['card'],
                               font=("Segoe UI", 11, "bold"), relief=tk.FLAT, 
                               cursor='hand2', padx=20, pady=10)
        activate_btn.pack(pady=10)
    else:
        deactivate_btn = tk.Button(control_frame, text="🛑 Deactivate Mouse Blocking",
                                 command=lambda: self._toggle_mouse_and_close(False, mouse_window),
                                 bg=self.colors['danger'], fg=self.colors['card'],
                                 font=("Segoe UI", 11, "bold"), relief=tk.FLAT, 
                                 cursor='hand2', padx=20, pady=10)
        deactivate_btn.pack(pady=10)
    
    # Settings section
    settings_frame = tk.Frame(content, bg=self.colors['card'], pady=15)
    settings_frame.pack(fill=tk.BOTH, expand=True)
    
    tk.Label(settings_frame, text="Quick Settings:", font=("Segoe UI", 11, "bold"),
            bg=self.colors['card'], fg=self.colors['text_primary']).pack(anchor=tk.W, pady=(0, 10))
    
    # Quick setting buttons
    btn_frame = tk.Frame(settings_frame, bg=self.colors['card'])
    btn_frame.pack(fill=tk.X, pady=5)
    
    tk.Button(btn_frame, text="Allow Basic Clicks Only",
             command=lambda: self._apply_mouse_setting('basic'),
             bg=self.colors['primary'], fg=self.colors['card'],
             font=("Segoe UI", 9, "bold"), relief=tk.FLAT, 
             cursor='hand2', padx=15, pady=8).pack(side=tk.LEFT, padx=(0, 10))
    
    tk.Button(btn_frame, text="Block All Buttons",
             command=lambda: self._apply_mouse_setting('all'),
             bg=self.colors['warning'], fg=self.colors['card'],
             font=("Segoe UI", 9, "bold"), relief=tk.FLAT, 
             cursor='hand2', padx=15, pady=8).pack(side=tk.LEFT, padx=(0, 10))
    
    # Close button
    tk.Button(content, text="Close", command=mouse_window.destroy,
             bg=self.colors['secondary'], fg=self.colors['card'],
             font=("Segoe UI", 10, "bold"), relief=tk.FLAT, 
             cursor='hand2', padx=20, pady=8).pack(pady=20)

def _toggle_mouse_and_close(self, enable, window):
    """Toggle mouse blocking and close window"""
    try:
        success = self.security_manager.toggle_mouse_blocking(enable)
        action = "activated" if enable else "deactivated"
        
        if success:
            messagebox.showinfo("✅ Success", f"Mouse blocking {action} successfully!")
        else:
            messagebox.showerror("❌ Error", f"Failed to {action.replace('ed', '')} mouse blocking.")
        
        window.destroy()
        self.refresh_status()
    except Exception as e:
        messagebox.showerror("❌ Error", f"Mouse blocking error: {str(e)}")
        window.destroy()

def _apply_mouse_setting(self, setting_type):
    """Apply quick mouse settings"""
    try:
        if setting_type == 'basic':
            self.security_manager.mouse_manager.allow_basic_clicks()
            messagebox.showinfo("✅ Applied", "Mouse set to allow basic clicks only (blocks middle/side buttons)")
        elif setting_type == 'all':
            self.security_manager.mouse_manager.block_all_buttons()
            messagebox.showinfo("✅ Applied", "Mouse set to block all buttons")
        
        self.refresh_status()
    except Exception as e:
        messagebox.showerror("❌ Error", f"Failed to apply mouse setting: {str(e)}")

def show_window_controls(self):
    """FIXED: Show window controls with proper integration"""
    window_control = tk.Toplevel(self.window)
    window_control.title("🪟 Window Guardian Controls")
    window_control.geometry("600x500")
    window_control.configure(bg=self.colors['surface'])
    window_control.transient(self.window)
    
    # Center window
    window_control.update_idletasks()
    x = (window_control.winfo_screenwidth() // 2) - 300
    y = (window_control.winfo_screenheight() // 2) - 250
    window_control.geometry(f"600x500+{x}+{y}")
    
    # Premium header
    header = tk.Frame(window_control, bg=self.colors['primary'], height=60)
    header.pack(fill=tk.X)
    header.pack_propagate(False)
    
    tk.Label(header, text="🪟 Window Protection System", 
            font=("Segoe UI", 14, "bold"), bg=self.colors['primary'], 
            fg=self.colors['card']).pack(pady=20)
    
    # Content
    content = tk.Frame(window_control, bg=self.colors['surface'])
    content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    # Status display
    status_frame = tk.Frame(content, bg=self.colors['card'], pady=15)
    status_frame.pack(fill=tk.X, pady=(0, 20))
    
    # Get real status from window manager
    is_active = self.security_manager.window_manager.is_active
    status_text = "🟢 ACTIVE" if is_active else "🔴 INACTIVE"
    status_color = self.colors['success'] if is_active else self.colors['danger']
    
    tk.Label(status_frame, text=f"Status: {status_text}", font=("Segoe UI", 12, "bold"),
            bg=self.colors['card'], fg=status_color).pack(pady=10)
    
    # Get protection info
    try:
        status_info = self.security_manager.window_manager.get_status()
        protected_count = status_info.get('protected_windows_count', 0)
        protection_level = status_info.get('protection_level', 'Unknown')
    except:
        protected_count = 0
        protection_level = "Error"
    
    tk.Label(status_frame, text=f"Protected Windows: {protected_count}",
            font=("Segoe UI", 10), bg=self.colors['card'], 
            fg=self.colors['text_primary']).pack(pady=2)
    
    tk.Label(status_frame, text=f"Protection Level: {protection_level}",
            font=("Segoe UI", 10), bg=self.colors['card'], 
            fg=self.colors['text_primary']).pack(pady=2)
    
    # Control buttons
    control_frame = tk.Frame(content, bg=self.colors['card'], pady=20)
    control_frame.pack(fill=tk.X, pady=(0, 20))
    
    # Create control buttons based on current state
    if not is_active:
        activate_btn = tk.Button(control_frame, text="🚀 Activate Window Protection",
                               command=lambda: self._toggle_window_and_close(True, window_control),
                               bg=self.colors['success'], fg=self.colors['card'],
                               font=("Segoe UI", 11, "bold"), relief=tk.FLAT, 
                               cursor='hand2', padx=20, pady=10)
        activate_btn.pack(pady=10)
        
        # Info text
        info_text = ("Window Protection will:\n"
                    "• Disable close buttons on protected windows\n"
                    "• Disable minimize buttons on protected windows\n"
                    "• Prevent windows from being closed accidentally\n"
                    "• Monitor and protect exam/browser windows")
        
        tk.Label(control_frame, text=info_text, font=("Segoe UI", 9),
                bg=self.colors['card'], fg=self.colors['text_secondary'],
                justify=tk.LEFT).pack(pady=10)
    else:
        deactivate_btn = tk.Button(control_frame, text="🛑 Deactivate Window Protection",
                                 command=lambda: self._toggle_window_and_close(False, window_control),
                                 bg=self.colors['danger'], fg=self.colors['card'],
                                 font=("Segoe UI", 11, "bold"), relief=tk.FLAT, 
                                 cursor='hand2', padx=20, pady=10)
        deactivate_btn.pack(pady=10)
        
        # Show protected windows if any
        if protected_count > 0:
            try:
                protected_windows = status_info.get('protected_windows', {})
                if protected_windows:
                    tk.Label(control_frame, text="Currently Protected Windows:", 
                            font=("Segoe UI", 10, "bold"), bg=self.colors['card'], 
                            fg=self.colors['text_primary']).pack(anchor=tk.W, pady=(10, 5))
                    
                    windows_text = "\n".join([f"• {title}" for title in list(protected_windows.values())[:5]])
                    if len(protected_windows) > 5:
                        windows_text += f"\n... and {len(protected_windows) - 5} more"
                    
                    tk.Label(control_frame, text=windows_text, font=("Segoe UI", 9),
                            bg=self.colors['card'], fg=self.colors['text_secondary'],
                            justify=tk.LEFT).pack(anchor=tk.W, pady=5)
            except:
                pass
    
    # Close button
    tk.Button(content, text="Close", command=window_control.destroy,
             bg=self.colors['secondary'], fg=self.colors['card'],
             font=("Segoe UI", 10, "bold"), relief=tk.FLAT, 
             cursor='hand2', padx=20, pady=8).pack(pady=20)

def _toggle_window_and_close(self, enable, window):
    """Toggle window protection and close window"""
    try:
        success = self.security_manager.toggle_window_protection(enable)
        action = "activated" if enable else "deactivated"
        
        if success:
            messagebox.showinfo("✅ Success", f"Window protection {action} successfully!")
        else:
            messagebox.showerror("❌ Error", f"Failed to {action.replace('ed', '')} window protection.")
        
        window.destroy()
        self.refresh_status()
    except Exception as e:
        messagebox.showerror("❌ Error", f"Window protection error: {str(e)}")
        window.destroy()

# FIXED: Update the existing toggle methods in AdminPanel class
def toggle_mouse_blocking(self, enable):
    """FIXED: Toggle mouse blocking with proper error handling"""
    try:
        success = self.security_manager.toggle_mouse_blocking(enable)
        action = "activated" if enable else "deactivated"
        
        if success:
            messagebox.showinfo("✅ Success", f"Mouse blocking {action} successfully!")
        else:
            messagebox.showerror("❌ Error", f"Failed to {action.replace('ed', '')} mouse blocking.")
        
        self.refresh_status()
        return success
    except Exception as e:
        messagebox.showerror("❌ Error", f"Mouse blocking error: {str(e)}")
        return False

def toggle_window_protection(self, enable):
    """FIXED: Toggle window protection with proper error handling"""
    try:
        success = self.security_manager.toggle_window_protection(enable)
        action = "activated" if enable else "deactivated"
        
        if success:
            messagebox.showinfo("✅ Success", f"Window protection {action} successfully!")
        else:
            messagebox.showerror("❌ Error", f"Failed to {action.replace('ed', '')} window protection.")
        
        self.refresh_status()
        return success
    except Exception as e:
        messagebox.showerror("❌ Error", f"Window protection error: {str(e)}")
        return False