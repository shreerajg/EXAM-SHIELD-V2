"""
Patch AdminPanel: ensure show_selective_lockdown_dialog exists and works
"""

import tkinter as tk
from tkinter import messagebox

from admin_panel import AdminPanel as _AP


def _show_selective_lockdown_dialog(self):
    dialog = tk.Toplevel(self.window)
    dialog.title("🔒 Selective Lockdown Configuration")
    dialog.geometry("500x600")
    dialog.configure(bg=self.colors['surface'])
    dialog.transient(self.window)
    dialog.grab_set()

    # Center dialog
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
        content = tk.Frame(card, bg=self.colors['card']); content.pack(fill=tk.X, padx=15, pady=12)
        var = tk.BooleanVar(value=True)
        self.selective_vars[key] = var
        chk = tk.Checkbutton(content, text=title, variable=var,
                             font=("Segoe UI", 11, "bold"), bg=self.colors['card'],
                             fg=self.colors['text_primary'], selectcolor=self.colors['card'],
                             activebackground=self.colors['card'])
        chk.pack(anchor=tk.W)
        tk.Label(content, text=desc, font=("Segoe UI", 9), bg=self.colors['card'],
                 fg=self.colors['text_secondary']).pack(anchor=tk.W, padx=20, pady=(2, 0))

    # Buttons
    btns = tk.Frame(dialog, bg=self.colors['surface'])
    btns.pack(fill=tk.X, padx=40, pady=20)

    def start():
        selected = {k: v.get() for k, v in self.selective_vars.items()}
        if not any(selected.values()):
            messagebox.showwarning("No Selection", "Please select at least one security module!")
            return
        names = [k.title() for k, s in selected.items() if s]
        if messagebox.askyesno("Confirm Selective Lockdown", "Start lockdown with these modules?\n\n" + "\n".join(f"✓ {n}" for n in names)):
            dialog.destroy()
            try:
                self.security_manager.start_exam_mode(selected)
                self.start_btn.config(state=tk.DISABLED); self.stop_btn.config(state=tk.NORMAL)
                self.refresh_status()
                messagebox.showinfo("🔒 SELECTIVE LOCKDOWN ACTIVE", "Lockdown active with:\n" + "\n".join(f"✓ {n}" for n in names))
            except Exception as e:
                messagebox.showerror("Error", f"Failed to start lockdown: {e}")

    tk.Button(btns, text="🚀 START SELECTED LOCKDOWN", command=start,
              bg=self.colors['success'], fg=self.colors['card'], font=("Segoe UI", 11, "bold"),
              relief=tk.FLAT, pady=10, cursor='hand2').pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0,10))
    tk.Button(btns, text="❌ CANCEL", command=dialog.destroy,
              bg=self.colors['danger'], fg=self.colors['card'], font=("Segoe UI", 11, "bold"),
              relief=tk.FLAT, pady=10, cursor='hand2').pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(10,0))

_AP.show_selective_lockdown_dialog = _show_selective_lockdown_dialog
