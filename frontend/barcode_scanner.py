import tkinter as tk
from tkinter import ttk

class BarcodeScanner(ttk.Frame):
    def __init__(self, parent, on_scan=None, placeholder="Escanear código de barras"):
        super().__init__(parent)
        self.on_scan = on_scan
        
        # Frame principal
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Label
        label = ttk.Label(main_frame, text=placeholder, font=('Arial', 14))
        label.pack(anchor=tk.W)
        
        # Frame para entrada y botón
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=(5, 0))
        
        # Campo de entrada
        self.barcode_var = tk.StringVar()
        self.entry = ttk.Entry(
            input_frame,
            textvariable=self.barcode_var,
            font=('Arial', 18)
        )
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.entry.bind('<Return>', self._on_submit)
        
        # Botón de escaneo
        self.scan_button = ttk.Button(
            input_frame,
            text="📷 Escanear",
            command=self._on_scan_click,
            width=15
        )
        self.scan_button.pack(side=tk.RIGHT, padx=(10, 0))
    
    def _on_submit(self, event):
        if self.barcode_var.get() and self.on_scan:
            self.on_scan(self.barcode_var.get().strip())
            self.clear()
    
    def _on_scan_click(self):
        if self.barcode_var.get() and self.on_scan:
            self.on_scan(self.barcode_var.get().strip())
            self.clear()
    
    def clear(self):
        self.barcode_var.set("")
        self.entry.focus()
    
    def focus(self):
        self.entry.focus()