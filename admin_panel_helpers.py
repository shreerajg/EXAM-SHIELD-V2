"""
Admin Panel supplemental methods: implement missing methods to prevent attribute errors
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, simpledialog
from datetime import datetime

# This file augments AdminPanel by defining the missing methods inside the class via monkey patch pattern.
# If AdminPanel is not imported here, this file should be merged into admin_panel.py. For stability,
# we re-open the class using the same name and add methods.

from admin_panel import AdminPanel as _AP

def _create_monitoring_tab(self):
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

_AP.create_monitoring_tab = _create_monitoring_tab


def _create_settings_tab(self):
    frame = ttk.Frame(self.notebook)
    self.notebook.add(frame, text="⚙️ Settings")
    container = tk.Frame(frame, bg=self.colors['surface']); container.pack(fill=tk.BOTH, expand=True)
    canvas = tk.Canvas(container, bg=self.colors['surface'], highlightthickness=0)
    scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
    inner = tk.Frame(canvas, bg=self.colors['surface'])
    inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0,0), window=inner, anchor="nw"); canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True, padx=15, pady=15); scrollbar.pack(side="right", fill="y", padx=(0,15), pady=15)

_AP.create_settings_tab = _create_settings_tab


def _create_logs_tab(self):
    frame = ttk.Frame(self.notebook)
    self.notebook.add(frame, text="📋 Security Logs")
    container = tk.Frame(frame, bg=self.colors['surface']); container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    controls = tk.Frame(container, bg=self.colors['card'], height=60); controls.pack(fill=tk.X, pady=(0,10)); controls.pack_propagate(False)
    row = tk.Frame(controls, bg=self.colors['card']); row.pack(fill=tk.X, padx=15, pady=15)
    tk.Button(row, text="🔄 Refresh", command=self.refresh_logs, bg=self.colors['info'], fg=self.colors['card'], font=("Segoe UI", 9, "bold"), relief=tk.FLAT, cursor='hand2', padx=10, pady=5).pack(side=tk.LEFT, padx=(0,10))
    tk.Button(row, text="🗑️ Clear All", command=self.clear_logs, bg=self.colors['warning'], fg=self.colors['card'], font=("Segoe UI", 9, "bold"), relief=tk.FLAT, cursor='hand2', padx=10, pady=5).pack(side=tk.LEFT, padx=(0,10))
    tk.Button(row, text="💾 Export", command=self.export_logs, bg=self.colors['success'], fg=self.colors['card'], font=("Segoe UI", 9, "bold"), relief=tk.FLAT, cursor='hand2', padx=10, pady=5).pack(side=tk.LEFT, padx=(0,10))
    logs_card = tk.Frame(container, bg=self.colors['card']); logs_card.pack(fill=tk.BOTH, expand=True)
    header = tk.Frame(logs_card, bg=self.colors['danger'], height=40); header.pack(fill=tk.X); header.pack_propagate(False)
    tk.Label(header, text="📋 Security Activity History", font=("Segoe UI", 12, "bold"), bg=self.colors['danger'], fg=self.colors['card']).pack(pady=10)
    content = tk.Frame(logs_card, bg=self.colors['card']); content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    self.logs_text = scrolledtext.ScrolledText(content, wrap=tk.WORD, height=25, font=("Consolas", 9), bg=self.colors['surface'], fg=self.colors['text_primary'])
    self.logs_text.pack(fill=tk.BOTH, expand=True)

_AP.create_logs_tab = _create_logs_tab


def _refresh_logs(self):
    # safe no-op if db method missing
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

_AP.refresh_logs = _refresh_logs


def _clear_logs(self):
    self.logs_text.delete(1.0, tk.END)

_AP.clear_logs = _clear_logs


def _export_logs(self):
    pass

_AP.export_logs = _export_logs
