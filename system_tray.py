"""
System Tray functionality for Exam Shield Premium
Enhanced with premium design and improved user experience
"""

import pystray
from PIL import Image, ImageDraw, ImageFont
import threading
import tkinter as tk
from tkinter import simpledialog, messagebox

class SystemTray:
    def __init__(self, admin_panel, security_manager):
        self.admin_panel = admin_panel
        self.security_manager = security_manager
        self.icon = None
        self.running = False
        
        # Premium colors
        self.colors = {
            'primary': (30, 61, 89),      # Deep navy blue
            'accent': (255, 201, 71),     # Premium gold
            'success': (39, 174, 96),     # Professional green
            'danger': (231, 76, 60),      # Professional red
            'white': (255, 255, 255),
            'dark': (44, 62, 80)
        }

    def create_icon_image(self):
        """Create a premium system tray icon"""
        size = 64
        image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        
        # Create shield shape with premium styling
        center_x, center_y = size // 2, size // 2
        
        # Shield outline
        shield_points = [
            (center_x, 8),           # Top
            (center_x + 20, 16),     # Top right
            (center_x + 20, 40),     # Right
            (center_x, 56),          # Bottom point
            (center_x - 20, 40),     # Left
            (center_x - 20, 16)      # Top left
        ]
        
        # Draw shield with gradient effect
        draw.polygon(shield_points, fill=self.colors['primary'], 
                    outline=self.colors['dark'], width=2)
        
        # Add inner shield design
        inner_points = [
            (center_x, 14),
            (center_x + 14, 20),
            (center_x + 14, 38),
            (center_x, 48),
            (center_x - 14, 38),
            (center_x - 14, 20)
        ]
        
        draw.polygon(inner_points, fill=self.colors['accent'])
        
        # Add lock symbol
        lock_size = 8
        lock_x, lock_y = center_x - 4, center_y - 2
        
        # Lock body
        draw.rectangle([lock_x, lock_y + 2, lock_x + lock_size, lock_y + lock_size], 
                      fill=self.colors['primary'])
        
        # Lock shackle
        draw.arc([lock_x + 1, lock_y - 3, lock_x + 7, lock_y + 3], 
                start=0, end=180, fill=self.colors['primary'], width=2)
        
        return image

    def create_menu(self):
        """Create premium context menu"""
        menu_items = []
        
        # Header item
        menu_items.append(
            pystray.MenuItem("Exam Shield Premium", self.show_admin_panel, 
                           default=True, enabled=True)
        )
        
        menu_items.append(pystray.Menu.SEPARATOR)
        
        # Main actions
        menu_items.append(
            pystray.MenuItem("🎛️ Open Control Center", self.show_admin_panel)
        )
        
        # Status-dependent items
        if self.security_manager.is_exam_mode:
            menu_items.extend([
                pystray.MenuItem("🔒 Lockdown Status: ACTIVE", None, enabled=False),
                pystray.MenuItem("🔓 End Lockdown Mode", self.stop_exam_mode_with_password),
            ])
        else:
            menu_items.extend([
                pystray.MenuItem("🔓 System Status: READY", None, enabled=False),
                pystray.MenuItem("🚀 Start Quick Lockdown", self.quick_start_exam_mode),
            ])
        
        menu_items.append(pystray.Menu.SEPARATOR)
        
        # System information
        try:
            system_info = self.security_manager.get_system_info()
            cpu_percent = system_info.get('cpu_percent', 0)
            memory_percent = system_info.get('memory_percent', 0)
            
            menu_items.extend([
                pystray.MenuItem(f"💻 CPU: {cpu_percent:.1f}%", None, enabled=False),
                pystray.MenuItem(f"🧠 RAM: {memory_percent:.1f}%", None, enabled=False),
            ])
        except:
            menu_items.append(
                pystray.MenuItem("📊 System Info Unavailable", None, enabled=False)
            )
        
        menu_items.append(pystray.Menu.SEPARATOR)
        
        # Exit option
        menu_items.append(
            pystray.MenuItem("🚪 Exit (Admin Required)", self.exit_application)
        )
        
        return pystray.Menu(*menu_items)

    def show_admin_panel(self, icon=None, item=None):
        """Show the admin panel with improved error handling"""
        try:
            if hasattr(self.admin_panel, 'window') and self.admin_panel.window:
                self.admin_panel.window.deiconify()
                self.admin_panel.window.lift()
                self.admin_panel.window.focus_force()
            else:
                self.show_notification("Admin Panel", "Admin panel is not available")
        except Exception as e:
            self.show_notification("Error", f"Failed to show admin panel: {str(e)}")

    def quick_start_exam_mode(self, icon=None, item=None):
        """Quick start exam mode with default settings"""
        try:
            # Use default security settings for quick start
            default_options = {
                'keyboard': True,
                'mouse': True,
                'internet': True,
                'windows': True,
                'processes': True
            }
            
            self.security_manager.start_exam_mode(default_options)
            if self.icon:
                self.icon.menu = self.create_menu()
            
            self.show_notification("Lockdown Active", 
                                 "Full security lockdown has been activated")
        except Exception as e:
            self.show_notification("Error", f"Failed to start lockdown: {str(e)}")

    def stop_exam_mode_with_password(self, icon=None, item=None):
        """Stop exam mode with premium password dialog"""
        try:
            # Create a premium-styled password dialog
            root = tk.Tk()
            root.withdraw()
            root.configure(bg='#f8f9fa')
            
            # Custom dialog
            dialog = tk.Toplevel(root)
            dialog.title("Security Authentication Required")
            dialog.geometry("450x300")
            dialog.configure(bg='#f8f9fa')
            dialog.resizable(False, False)
            dialog.grab_set()
            
            # Center dialog
            dialog.update_idletasks()
            x = (dialog.winfo_screenwidth() // 2) - 225
            y = (dialog.winfo_screenheight() // 2) - 150
            dialog.geometry(f"450x300+{x}+{y}")
            
            # Header
            header = tk.Frame(dialog, bg='#1e3d59', height=80)
            header.pack(fill=tk.X)
            header.pack_propagate(False)
            
            header_content = tk.Frame(header, bg='#1e3d59')
            header_content.pack(expand=True, pady=20)
            
            tk.Label(header_content, text="🔒", font=("Segoe UI", 24),
                    bg='#1e3d59', fg='#ffc947').pack()
            tk.Label(header_content, text="End Lockdown Mode",
                    font=("Segoe UI", 14, "bold"), bg='#1e3d59', fg='white').pack()
            
            # Content
            content = tk.Frame(dialog, bg='#f8f9fa')
            content.pack(fill=tk.BOTH, expand=True, padx=40, pady=30)
            
            tk.Label(content, text="Administrator Password Required",
                    font=("Segoe UI", 12, "bold"), bg='#f8f9fa', fg='#2c3e50').pack(pady=(0, 20))
            
            password_var = tk.StringVar()
            password_entry = tk.Entry(content, textvariable=password_var,
                                    font=("Segoe UI", 12), show="*", width=30,
                                    relief=tk.FLAT, bd=5, bg='white')
            password_entry.pack(pady=(0, 20), ipady=8)
            
            result = {'password': None, 'confirmed': False}
            
            def confirm():
                result['password'] = password_var.get()
                result['confirmed'] = True
                dialog.destroy()
                root.destroy()
            
            def cancel():
                dialog.destroy()
                root.destroy()
            
            button_frame = tk.Frame(content, bg='#f8f9fa')
            button_frame.pack(fill=tk.X, pady=10)
            
            tk.Button(button_frame, text="✅ Confirm", command=confirm,
                     bg='#27ae60', fg='white', font=("Segoe UI", 10, "bold"),
                     relief=tk.FLAT, padx=15, pady=8).pack(side=tk.LEFT, padx=(0, 10))
            
            tk.Button(button_frame, text="❌ Cancel", command=cancel,
                     bg='#e74c3c', fg='white', font=("Segoe UI", 10, "bold"),
                     relief=tk.FLAT, padx=15, pady=8).pack(side=tk.RIGHT)
            
            password_entry.bind("<Return>", lambda e: confirm())
            password_entry.focus()
            
            dialog.wait_window()
            
            if result['confirmed'] and result['password']:
                import hashlib
                from database_manager import DatabaseManager
                
                db_manager = DatabaseManager()
                password_hash = hashlib.sha256(result['password'].encode()).hexdigest()
                
                if db_manager.verify_admin("admin", password_hash):
                    self.security_manager.stop_exam_mode()
                    if self.icon:
                        self.icon.menu = self.create_menu()
                    
                    self.show_notification("Lockdown Ended", 
                                         "Security lockdown has been deactivated")
                else:
                    self.show_notification("Authentication Failed", 
                                         "Invalid administrator password")
            
        except Exception as e:
            self.show_notification("Error", f"Authentication error: {str(e)}")

    def exit_application(self, icon=None, item=None):
        """Exit application with premium authentication"""
        try:
            root = tk.Tk()
            root.withdraw()
            
            # Premium exit confirmation dialog
            dialog = tk.Toplevel(root)
            dialog.title("Exit Exam Shield Premium")
            dialog.geometry("500x350")
            dialog.configure(bg='#f8f9fa')
            dialog.resizable(False, False)
            dialog.grab_set()
            
            # Center dialog
            dialog.update_idletasks()
            x = (dialog.winfo_screenwidth() // 2) - 250
            y = (dialog.winfo_screenheight() // 2) - 175
            dialog.geometry(f"500x350+{x}+{y}")
            
            # Header
            header = tk.Frame(dialog, bg='#e74c3c', height=80)
            header.pack(fill=tk.X)
            header.pack_propagate(False)
            
            header_content = tk.Frame(header, bg='#e74c3c')
            header_content.pack(expand=True, pady=20)
            
            tk.Label(header_content, text="⚠️", font=("Segoe UI", 24),
                    bg='#e74c3c', fg='white').pack()
            tk.Label(header_content, text="Exit Security System",
                    font=("Segoe UI", 14, "bold"), bg='#e74c3c', fg='white').pack()
            
            # Content
            content = tk.Frame(dialog, bg='#f8f9fa')
            content.pack(fill=tk.BOTH, expand=True, padx=40, pady=30)
            
            warning_text = ("⚠️ WARNING: This will completely shut down all security features!\n\n"
                          "• All lockdown protections will be disabled\n"
                          "• System monitoring will stop\n"
                          "• Security logging will end\n\n"
                          "Enter administrator password to confirm:")
            
            tk.Label(content, text=warning_text, font=("Segoe UI", 10),
                    bg='#f8f9fa', fg='#2c3e50', justify=tk.LEFT).pack(pady=(0, 15))
            
            password_var = tk.StringVar()
            password_entry = tk.Entry(content, textvariable=password_var,
                                    font=("Segoe UI", 12), show="*", width=35,
                                    relief=tk.FLAT, bd=5, bg='white')
            password_entry.pack(pady=(0, 20), ipady=8)
            
            result = {'password': None, 'confirmed': False}
            
            def confirm_exit():
                result['password'] = password_var.get()
                result['confirmed'] = True
                dialog.destroy()
                root.destroy()
            
            def cancel_exit():
                dialog.destroy()
                root.destroy()
            
            button_frame = tk.Frame(content, bg='#f8f9fa')
            button_frame.pack(fill=tk.X, pady=10)
            
            tk.Button(button_frame, text="🚪 EXIT SYSTEM", command=confirm_exit,
                     bg='#e74c3c', fg='white', font=("Segoe UI", 11, "bold"),
                     relief=tk.FLAT, padx=20, pady=10).pack(side=tk.LEFT, padx=(0, 15))
            
            tk.Button(button_frame, text="❌ Cancel", command=cancel_exit,
                     bg='#95a5a6', fg='white', font=("Segoe UI", 11, "bold"),
                     relief=tk.FLAT, padx=20, pady=10).pack(side=tk.RIGHT)
            
            password_entry.bind("<Return>", lambda e: confirm_exit())
            password_entry.focus()
            
            dialog.wait_window()
            
            if result['confirmed'] and result['password']:
                import hashlib
                from database_manager import DatabaseManager
                
                db_manager = DatabaseManager()
                password_hash = hashlib.sha256(result['password'].encode()).hexdigest()
                
                if db_manager.verify_admin("admin", password_hash):
                    self.show_notification("Exam Shield Premium", 
                                         "Security system is shutting down...")
                    self.stop()
                    import sys
                    sys.exit(0)
                else:
                    self.show_notification("Authentication Failed", 
                                         "Invalid administrator password")
                    
        except Exception as e:
            self.show_notification("Error", f"Exit error: {str(e)}")

    def show_notification(self, title, message, duration=3):
        """Show system notification with premium styling"""
        try:
            if self.icon:
                self.icon.notify(message, title)
        except:
            pass  # Fallback if notifications aren't supported

    def run(self):
        """Run the system tray with premium icon and menu"""
        self.running = True
        image = self.create_icon_image()
        menu = self.create_menu()
        
        self.icon = pystray.Icon(
            "ExamShieldPremium", 
            image, 
            "Exam Shield Premium - Security Monitor", 
            menu
        )
        
        # Update menu periodically
        def update_menu():
            while self.running:
                try:
                    if self.icon and self.running:
                        self.icon.menu = self.create_menu()
                    threading.Event().wait(5)  # Update every 5 seconds
                except:
                    break
        
        menu_thread = threading.Thread(target=update_menu, daemon=True)
        menu_thread.start()
        
        self.icon.run()

    def stop(self):
        """Stop the system tray"""
        self.running = False
        if self.icon:
            self.icon.stop()
