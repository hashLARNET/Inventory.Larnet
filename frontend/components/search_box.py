import tkinter as tk
from tkinter import ttk
import threading

class SearchBox(ttk.Frame):
    def __init__(self, parent, on_search, delay_ms=300):
        super().__init__(parent)
        self.on_search = on_search
        self.delay_ms = delay_ms
        self.search_timer = None
        
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self._on_text_change)
        
        self.entry = ttk.Entry(
            self,
            textvariable=self.search_var,
            font=('Arial', 12)
        )
        self.entry.pack(fill=tk.X)
        
        self.loading_label = ttk.Label(self, text="")
        self.loading_label.pack()
        
    def _on_text_change(self, *args):
        # Cancelar búsqueda anterior
        if self.search_timer:
            self.after_cancel(self.search_timer)
        
        # Programar nueva búsqueda
        self.search_timer = self.after(
            self.delay_ms,
            self._perform_search
        )
        
    def _perform_search(self):
        query = self.search_var.get()
        if len(query) >= 2 or len(query) == 0:
            self.loading_label.config(text="Buscando...")
            
            # Ejecutar en thread separado
            thread = threading.Thread(
                target=self._search_thread,
                args=(query,)
            )
            thread.daemon = True
            thread.start()
    
    def _search_thread(self, query):
        try:
            self.on_search(query)
        finally:
            self.after(0, lambda: self.loading_label.config(text=""))
