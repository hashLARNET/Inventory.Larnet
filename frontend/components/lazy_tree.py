import tkinter as tk
from tkinter import ttk
from typing import List, Dict, Any, Callable

class LazyTreeview(ttk.Frame):
    def __init__(self, parent, columns, data_loader: Callable, **kwargs):
        super().__init__(parent)
        self.data_loader = data_loader
        self.current_page = 1
        self.items_per_page = 50
        self.total_items = 0
        self.cache = {}
        
        # Frame principal
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Treeview con scrollbar virtual
        self.tree = ttk.Treeview(main_frame, columns=columns, **kwargs)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(main_frame, command=self._on_scroll)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Paginación
        self.pagination_frame = ttk.Frame(self)
        self.pagination_frame.pack(fill=tk.X, pady=5)
        
        self.prev_btn = ttk.Button(
            self.pagination_frame, 
            text="← Anterior",
            command=self.prev_page,
            state=tk.DISABLED
        )
        self.prev_btn.pack(side=tk.LEFT)
        
        self.page_label = ttk.Label(
            self.pagination_frame,
            text="Página 1 de 1"
        )
        self.page_label.pack(side=tk.LEFT, padx=20)
        
        self.next_btn = ttk.Button(
            self.pagination_frame,
            text="Siguiente →",
            command=self.next_page
        )
        self.next_btn.pack(side=tk.LEFT)
        
        # Información de rendimiento
        self.info_label = ttk.Label(
            self.pagination_frame,
            text="",
            foreground="gray"
        )
        self.info_label.pack(side=tk.RIGHT)
        
    def load_data(self, filters=None):
        """Cargar datos con paginación"""
        import time
        start_time = time.time()
        
        # Verificar caché
        cache_key = f"{self.current_page}_{str(filters)}"
        if cache_key in self.cache:
            data = self.cache[cache_key]
        else:
            # Cargar datos del servidor
            data = self.data_loader(
                page=self.current_page,
                per_page=self.items_per_page,
                filters=filters
            )
            self.cache[cache_key] = data
        
        # Limpiar árbol
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Insertar nuevos datos
        if isinstance(data, dict):
            items = data.get('items', [])
            self.total_items = data.get('total', 0)
            total_pages = data.get('pages', 1)
        else:
            items = data
            total_pages = 1
        
        for item in items:
            self.insert_item(item)
        
        # Actualizar paginación
        self.page_label.config(text=f"Página {self.current_page} de {total_pages}")
        self.prev_btn.config(state=tk.NORMAL if self.current_page > 1 else tk.DISABLED)
        self.next_btn.config(state=tk.NORMAL if self.current_page < total_pages else tk.DISABLED)
        
        # Mostrar tiempo de carga
        load_time = time.time() - start_time
        self.info_label.config(text=f"Cargado en {load_time:.2f}s | {len(items)} items")
        
    def insert_item(self, item_data):
        """Insertar item en el árbol - Override en subclases"""
        pass
        
    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.load_data()
    
    def next_page(self):
        self.current_page += 1
        self.load_data()
        
    def _on_scroll(self, *args):
        """Manejar scroll virtual para cargar más datos si es necesario"""
        pass
        
    def clear_cache(self):
        """Limpiar caché cuando sea necesario"""
        self.cache.clear()
