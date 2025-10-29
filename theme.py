import tkinter as tk
from tkinter import ttk
import sys
import os

class ExamShieldTheme:
    """Modern theme system for Exam Shield Pro"""
    
    def __init__(self, theme_mode="light"):
        self.theme_mode = theme_mode
        self.setup_theme()
    
    def setup_theme(self):
        """Initialize theme configuration"""
        if self.theme_mode == "dark":
            self.colors = self.get_dark_theme()
        else:
            self.colors = self.get_light_theme()
        
        self.fonts = self.get_font_system()
        self.animations = self.get_animation_config()
    
    def get_light_theme(self):
        """Light theme color palette"""
        return {
            # Primary colors
            'primary': '#2563EB',
            'primary_light': '#60A5FA',
            'primary_dark': '#1D4ED8',
            'primary_hover': '#1E40AF',
            
            # Secondary colors
            'secondary': '#10B981',
            'secondary_light': '#34D399',
            'secondary_dark': '#047857',
            
            # Status colors
            'success': '#10B981',
            'warning': '#F59E0B',
            'danger': '#EF4444',
            'info': '#3B82F6',
            
            # Neutral colors
            'white': '#FFFFFF',
            'gray_50': '#F9FAFB',
            'gray_100': '#F3F4F6',
            'gray_200': '#E5E7EB',
            'gray_300': '#D1D5DB',
            'gray_400': '#9CA3AF',
            'gray_500': '#6B7280',
            'gray_600': '#4B5563',
            'gray_700': '#374151',
            'gray_800': '#1F2937',
            'gray_900': '#111827',
            
            # Surface colors
            'background': '#F8FAFC',
            'surface': '#FFFFFF',
            'card': '#FFFFFF',
            'sidebar': '#1E293B',
            'sidebar_hover': '#334155',
            
            # Text colors
            'text_primary': '#1E293B',
            'text_secondary': '#64748B',
            'text_muted': '#94A3B8',
            'text_inverse': '#FFFFFF',
            
            # Border colors
            'border': '#E2E8F0',
            'border_light': '#F1F5F9',
            'border_focus': '#2563EB',
            
            # Shadow colors
            'shadow': 'rgba(0, 0, 0, 0.1)',
            'shadow_dark': 'rgba(0, 0, 0, 0.25)',
        }
    
    def get_dark_theme(self):
        """Dark theme color palette"""
        return {
            # Primary colors (same as light)
            'primary': '#3B82F6',
            'primary_light': '#60A5FA',
            'primary_dark': '#1D4ED8',
            'primary_hover': '#2563EB',
            
            # Secondary colors
            'secondary': '#10B981',
            'secondary_light': '#34D399',
            'secondary_dark': '#047857',
            
            # Status colors
            'success': '#10B981',
            'warning': '#F59E0B',
            'danger': '#EF4444',
            'info': '#3B82F6',
            
            # Neutral colors (inverted)
            'white': '#FFFFFF',
            'gray_50': '#18181B',
            'gray_100': '#27272A',
            'gray_200': '#3F3F46',
            'gray_300': '#52525B',
            'gray_400': '#71717A',
            'gray_500': '#A1A1AA',
            'gray_600': '#D4D4D8',
            'gray_700': '#E4E4E7',
            'gray_800': '#F4F4F5',
            'gray_900': '#FAFAFA',
            
            # Surface colors
            'background': '#0F172A',
            'surface': '#1E293B',
            'card': '#1E293B',
            'sidebar': '#0F172A',
            'sidebar_hover': '#1E293B',
            
            # Text colors
            'text_primary': '#F1F5F9',
            'text_secondary': '#CBD5E1',
            'text_muted': '#94A3B8',
            'text_inverse': '#1E293B',
            
            # Border colors
            'border': '#334155',
            'border_light': '#475569',
            'border_focus': '#3B82F6',
            
            # Shadow colors
            'shadow': 'rgba(0, 0, 0, 0.3)',
            'shadow_dark': 'rgba(0, 0, 0, 0.5)',
        }
    
    def get_font_system(self):
        """Professional font system"""
        # Detect system fonts
        system_font = self.get_system_font()
        
        return {
            'heading': (system_font, 28, 'bold'),
            'title': (system_font, 20, 'bold'),
            'subtitle': (system_font, 16, 'bold'),
            'body': (system_font, 11, 'normal'),
            'body_bold': (system_font, 11, 'bold'),
            'body_large': (system_font, 12, 'normal'),
            'caption': (system_font, 10, 'normal'),
            'small': (system_font, 9, 'normal'),
            'mono': ('Consolas', 10, 'normal'),
            'mono_small': ('Consolas', 9, 'normal'),
        }
    
    def get_system_font(self):
        """Get appropriate system font"""
        if sys.platform.startswith('win'):
            return 'Segoe UI'
        elif sys.platform.startswith('darwin'):
            return 'SF Pro Display'
        else:
            return 'Ubuntu'
    
    def get_animation_config(self):
        """Animation and transition configuration"""
        return {
            'duration_fast': 150,
            'duration_normal': 250,
            'duration_slow': 400,
            'easing': 'ease-out',
            'hover_scale': 1.02,
            'button_press_scale': 0.98,
        }
    
    def apply_ttk_theme(self, root):
        """Apply theme to ttk widgets"""
        style = ttk.Style()
        
        # Use modern theme if available
        try:
            import sv_ttk
            if self.theme_mode == "dark":
                sv_ttk.set_theme("dark")
            else:
                sv_ttk.set_theme("light")
        except ImportError:
            # Fallback to built-in themes
            style.theme_use('clam')
        
        # Configure custom styles
        self.configure_button_styles(style)
        self.configure_entry_styles(style)
        self.configure_frame_styles(style)
        self.configure_treeview_styles(style)
        self.configure_notebook_styles(style)
    
    def configure_button_styles(self, style):
        """Configure button styles"""
        # Primary button
        style.configure('Primary.TButton',
                       background=self.colors['primary'],
                       foreground=self.colors['text_inverse'],
                       font=self.fonts['body_bold'],
                       borderwidth=0,
                       focuscolor='none',
                       relief='flat')
        
        style.map('Primary.TButton',
                 background=[('active', self.colors['primary_hover']),
                           ('pressed', self.colors['primary_dark'])])
        
        # Success button
        style.configure('Success.TButton',
                       background=self.colors['success'],
                       foreground=self.colors['text_inverse'],
                       font=self.fonts['body_bold'],
                       borderwidth=0,
                       focuscolor='none',
                       relief='flat')
        
        # Danger button
        style.configure('Danger.TButton',
                       background=self.colors['danger'],
                       foreground=self.colors['text_inverse'],
                       font=self.fonts['body_bold'],
                       borderwidth=0,
                       focuscolor='none',
                       relief='flat')
        
        # Warning button
        style.configure('Warning.TButton',
                       background=self.colors['warning'],
                       foreground=self.colors['text_inverse'],
                       font=self.fonts['body_bold'],
                       borderwidth=0,
                       focuscolor='none',
                       relief='flat')
    
    def configure_entry_styles(self, style):
        """Configure entry widget styles"""
        style.configure('Modern.TEntry',
                       fieldbackground=self.colors['surface'],
                       foreground=self.colors['text_primary'],
                       bordercolor=self.colors['border'],
                       focuscolor=self.colors['border_focus'],
                       insertcolor=self.colors['primary'],
                       font=self.fonts['body'])
    
    def configure_frame_styles(self, style):
        """Configure frame styles"""
        style.configure('Card.TFrame',
                       background=self.colors['card'],
                       relief='flat',
                       borderwidth=1)
        
        style.configure('Sidebar.TFrame',
                       background=self.colors['sidebar'])
    
    def configure_treeview_styles(self, style):
        """Configure treeview styles"""
        style.configure('Modern.Treeview',
                       background=self.colors['surface'],
                       foreground=self.colors['text_primary'],
                       fieldbackground=self.colors['surface'],
                       font=self.fonts['body'])
        
        style.configure('Modern.Treeview.Heading',
                       background=self.colors['gray_100'],
                       foreground=self.colors['text_primary'],
                       font=self.fonts['body_bold'])
    
    def configure_notebook_styles(self, style):
        """Configure notebook styles"""
        style.configure('Modern.TNotebook',
                       background=self.colors['background'],
                       borderwidth=0)
        
        style.configure('Modern.TNotebook.Tab',
                       background=self.colors['surface'],
                       foreground=self.colors['text_secondary'],
                       font=self.fonts['body'],
                       padding=(20, 10))
        
        style.map('Modern.TNotebook.Tab',
                 background=[('selected', self.colors['primary']),
                           ('active', self.colors['gray_100'])],
                 foreground=[('selected', self.colors['text_inverse']),
                           ('active', self.colors['text_primary'])])

class AnimationManager:
    """Handle smooth animations and transitions"""
    
    def __init__(self, root):
        self.root = root
        self.animations = {}
    
    def fade_in(self, widget, duration=300):
        """Fade in animation"""
        widget.attributes('-alpha', 0.0)
        self.animate_alpha(widget, 0.0, 1.0, duration)
    
    def fade_out(self, widget, duration=300, callback=None):
        """Fade out animation"""
        self.animate_alpha(widget, 1.0, 0.0, duration, callback)
    
    def animate_alpha(self, widget, start_alpha, end_alpha, duration, callback=None):
        """Animate widget alpha"""
        steps = 30
        step_time = duration // steps
        alpha_step = (end_alpha - start_alpha) / steps
        current_step = 0
        
        def step():
            nonlocal current_step
            if current_step <= steps:
                alpha = start_alpha + (alpha_step * current_step)
                try:
                    widget.attributes('-alpha', alpha)
                    current_step += 1
                    widget.after(step_time, step)
                except tk.TclError:
                    pass  # Widget was destroyed
            elif callback:
                callback()
        
        step()
    
    def slide_in(self, widget, direction='left', duration=300):
        """Slide in animation"""
        # Implementation for slide animations
        pass
    
    def button_press_effect(self, button):
        """Button press visual effect"""
        original_relief = button.cget('relief')
        button.config(relief='sunken')
        button.after(100, lambda: button.config(relief=original_relief))

class ModernComponents:
    """Custom modern UI components"""
    
    def __init__(self, theme):
        self.theme = theme
    
    def create_card(self, parent, title=None, **kwargs):
        """Create a modern card component"""
        card_frame = tk.Frame(parent, 
                             bg=self.theme.colors['card'],
                             relief='flat',
                             bd=0,
                             **kwargs)
        
        if title:
            title_label = tk.Label(card_frame,
                                  text=title,
                                  font=self.theme.fonts['subtitle'],
                                  bg=self.theme.colors['card'],
                                  fg=self.theme.colors['text_primary'])
            title_label.pack(anchor='w', padx=20, pady=(20, 10))
        
        return card_frame
    
    def create_icon_button(self, parent, icon, text, command, style='primary'):
        """Create modern icon button"""
        colors = {
            'primary': (self.theme.colors['primary'], self.theme.colors['text_inverse']),
            'success': (self.theme.colors['success'], self.theme.colors['text_inverse']),
            'danger': (self.theme.colors['danger'], self.theme.colors['text_inverse']),
            'warning': (self.theme.colors['warning'], self.theme.colors['text_inverse']),
        }
        
        bg_color, fg_color = colors.get(style, colors['primary'])
        
        button = tk.Button(parent,
                          text=f"{icon}  {text}",
                          command=command,
                          bg=bg_color,
                          fg=fg_color,
                          font=self.theme.fonts['body_bold'],
                          relief='flat',
                          bd=0,
                          cursor='hand2',
                          padx=20,
                          pady=12)
        
        # Add hover effects
        def on_enter(e):
            if style == 'primary':
                button.config(bg=self.theme.colors['primary_hover'])
        
        def on_leave(e):
            button.config(bg=bg_color)
        
        button.bind('<Enter>', on_enter)
        button.bind('<Leave>', on_leave)
        
        return button
    
    def create_status_indicator(self, parent, status='inactive'):
        """Create modern status indicator"""
        colors = {
            'active': self.theme.colors['success'],
            'inactive': self.theme.colors['gray_400'],
            'warning': self.theme.colors['warning'],
            'danger': self.theme.colors['danger']
        }
        
        indicator = tk.Label(parent,
                           text="●",
                           font=('Segoe UI', 12),
                           fg=colors.get(status, colors['inactive']),
                           bg=parent.cget('bg') if hasattr(parent, 'cget') else self.theme.colors['surface'])
        
        return indicator
    
    def create_progress_ring(self, parent, value=0, max_value=100):
        """Create modern circular progress indicator"""
        # This would require custom drawing with tkinter Canvas
        # For now, return a simple progress bar
        progress = ttk.Progressbar(parent,
                                  mode='determinate',
                                  value=value,
                                  maximum=max_value)
        return progress

# Theme presets
THEMES = {
    'light': ExamShieldTheme('light'),
    'dark': ExamShieldTheme('dark'),
}

def get_theme(theme_name='light'):
    """Get theme instance"""
    return THEMES.get(theme_name, THEMES['light'])