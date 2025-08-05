#!/usr/bin/env python3
"""
Sistema de Inventario Multi-Bodega - GUI conectado al backend
Versión con interfaz del ejemplo pero conectado al backend FastAPI real
"""

import tkinter as tk
from tkinter import ttk, messagebox, font
from datetime import datetime
import json
import os
from typing import Dict, List, Optional, Any
from frontend.data_manager import DataManager

# Configuración de colores y estilos
class Config:
    # Colores principales
    PRIMARY_COLOR = "#1976D2"
    SECONDARY_COLOR = "#424242"
    SUCCESS_COLOR = "#4CAF50"
    WARNING_COLOR = "#FF9800"
    ERROR_COLOR = "#F44336"
    BACKGROUND_COLOR = "#F5F5F5"
    WHITE = "#FFFFFF"
    TEXT_COLOR = "#212121"
    ACCENT_COLOR = "#FF5722"
    
    # Tamaños para interfaz táctil
    BUTTON_HEIGHT = 3
    BUTTON_WIDTH = 20
    FONT_SIZE_LARGE = 18
    FONT_SIZE_MEDIUM = 14
    FONT_SIZE_SMALL = 12
    FONT_SIZE_TITLE = 24
    FONT_FAMILY = "Arial"
    
    # Configuración de la aplicación
    APP_TITLE = "Sistema de Inventario Multi-Bodega"
    APP_VERSION = "1.0.0"

# Clase para manejar el estado de sesión
class SessionState:
    def __init__(self):
        self.current_user = None
        self.current_warehouse = None
        self.is_authenticated = False
    
    def login(self, user):
        self.current_user = user
        self.is_authenticated = True
    
    def logout(self):
        self.current_user = None
        self.current_warehouse = None
        self.is_authenticated = False
    
    def set_warehouse(self, warehouse):
        self.current_warehouse = warehouse
        self.app.data_manager.set_current_warehouse(warehouse)

# Componente de escaneo de código de barras
class BarcodeScanner(ttk.Frame):
    def __init__(self, parent, on_scan=None, placeholder="Escanear código de barras"):
        super().__init__(parent)
        self.on_scan = on_scan
        
        # Frame principal
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Label
        label = ttk.Label(main_frame, text=placeholder, font=('Arial', Config.FONT_SIZE_MEDIUM))
        label.pack(anchor=tk.W)
        
        # Frame para entrada y botón
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=(5, 0))
        
        # Campo de entrada
        self.barcode_var = tk.StringVar()
        self.entry = ttk.Entry(
            input_frame,
            textvariable=self.barcode_var,
            font=('Arial', Config.FONT_SIZE_LARGE)
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

# Página de Login
class LoginPage(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.pack(fill=tk.BOTH, expand=True)
        
        # Configurar estilo
        self.configure(style='Background.TFrame')
        
        # Frame central
        center_frame = ttk.Frame(self, style='Card.TFrame')
        center_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Título
        title_frame = ttk.Frame(center_frame, style='Card.TFrame')
        title_frame.pack(pady=20)
        
        icon_label = ttk.Label(
            title_frame,
            text="🏭",
            font=('Arial', 48),
            style='Card.TLabel'
        )
        icon_label.pack()
        
        title_label = ttk.Label(
            title_frame,
            text=Config.APP_TITLE,
            font=('Arial', Config.FONT_SIZE_LARGE, 'bold'),
            style='Card.TLabel'
        )
        title_label.pack(pady=(10, 0))
        
        # Frame de login
        login_frame = ttk.Frame(center_frame, style='Card.TFrame')
        login_frame.pack(padx=40, pady=20)
        
        # Usuario
        ttk.Label(
            login_frame,
            text="Usuario:",
            font=('Arial', Config.FONT_SIZE_MEDIUM),
            style='Card.TLabel'
        ).grid(row=0, column=0, sticky=tk.W, pady=10)
        
        self.username_var = tk.StringVar()
        self.username_entry = ttk.Entry(
            login_frame,
            textvariable=self.username_var,
            font=('Arial', Config.FONT_SIZE_MEDIUM),
            width=25
        )
        self.username_entry.grid(row=0, column=1, padx=(10, 0), pady=10)
        self.username_entry.focus()
        
        # Contraseña
        ttk.Label(
            login_frame,
            text="Contraseña:",
            font=('Arial', Config.FONT_SIZE_MEDIUM),
            style='Card.TLabel'
        ).grid(row=1, column=0, sticky=tk.W, pady=10)
        
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(
            login_frame,
            textvariable=self.password_var,
            show="*",
            font=('Arial', Config.FONT_SIZE_MEDIUM),
            width=25
        )
        self.password_entry.grid(row=1, column=1, padx=(10, 0), pady=10)
        self.password_entry.bind('<Return>', lambda e: self.login())
        
        # Mensaje de error
        self.error_label = ttk.Label(
            login_frame,
            text="",
            font=('Arial', Config.FONT_SIZE_SMALL),
            foreground='red',
            style='Card.TLabel'
        )
        self.error_label.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Botón de login
        login_button = ttk.Button(
            login_frame,
            text="Iniciar Sesión",
            command=self.login,
            style='Primary.TButton',
            width=30
        )
        login_button.grid(row=3, column=0, columnspan=2, pady=20)
        
        # Información de usuarios de prueba
        info_frame = ttk.Frame(center_frame, style='Card.TFrame')
        info_frame.pack(pady=(0, 20))
        
        ttk.Label(
            info_frame,
            text="Usuarios de prueba:",
            font=('Arial', Config.FONT_SIZE_SMALL, 'italic'),
            style='Card.TLabel'
        ).pack()
        
        users_info = [
            "Admin_Santiago (pass: admin123)",
            "Operador_Juan (pass: admin123)",
            "Operador_Maria (pass: admin123)",
            "Supervisor_Carlos (pass: admin123)"
        ]
        
        for info in users_info:
            ttk.Label(
                info_frame,
                text=info,
                font=('Arial', Config.FONT_SIZE_SMALL),
                style='Card.TLabel'
            ).pack()
    
    def login(self):
        username = self.username_var.get()
        password = self.password_var.get()
        
        if not username or not password:
            self.show_error("Por favor ingrese usuario y contraseña")
            return
        
        user = self.app.data_manager.verify_login(username, password)
        if user:
            self.app.session_state.login(user)
            self.app.show_home_page()
        else:
            self.show_error("Usuario o contraseña incorrectos")
    
    def show_error(self, message):
        self.error_label.config(text=message)
        self.after(3000, lambda: self.error_label.config(text=""))

# Página Principal
class HomePage(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header_frame = ttk.Frame(self, style='Header.TFrame')
        header_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Información del usuario
        user_info = ttk.Label(
            header_frame,
            text=f"Bienvenido, {self.app.session_state.current_user['full_name']}",
            font=('Arial', Config.FONT_SIZE_LARGE, 'bold'),
            style='Header.TLabel'
        )
        user_info.pack(side=tk.LEFT)
        
        # Botón de cerrar sesión
        logout_button = ttk.Button(
            header_frame,
            text="Cerrar Sesión",
            command=self.logout,
            style='Danger.TButton'
        )
        logout_button.pack(side=tk.RIGHT)
        
        # Frame principal
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Sección de selección de bodega
        warehouse_frame = ttk.LabelFrame(
            main_frame,
            text="Selección de Bodega",
            padding=20
        )
        warehouse_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(
            warehouse_frame,
            text="Seleccione la bodega donde se encuentra:",
            font=('Arial', Config.FONT_SIZE_MEDIUM)
        ).pack(anchor=tk.W, pady=(0, 10))
        
        self.warehouse_var = tk.StringVar()
        self.warehouse_combo = ttk.Combobox(
            warehouse_frame,
            textvariable=self.warehouse_var,
            font=('Arial', Config.FONT_SIZE_MEDIUM),
            state='readonly',
            width=40
        )
        self.warehouse_combo.pack(fill=tk.X)
        self.warehouse_combo.bind('<<ComboboxSelected>>', self.on_warehouse_selected)
        
        # Cargar bodegas
        self.load_warehouses()
        
        # Frame de opciones (inicialmente deshabilitado)
        self.options_frame = ttk.LabelFrame(
            main_frame,
            text="Opciones Disponibles",
            padding=20
        )
        self.options_frame.pack(fill=tk.BOTH, expand=True)
        
        # Crear botones de opciones
        buttons_frame = ttk.Frame(self.options_frame)
        buttons_frame.pack(expand=True)
        
        # Botón de Inventario
        self.inventory_button = ttk.Button(
            buttons_frame,
            text="📦 Inventario",
            command=lambda: self.app.show_inventory_page(),
            style='Primary.TButton',
            width=20,
            state=tk.DISABLED
        )
        self.inventory_button.grid(row=0, column=0, padx=10, pady=10)
        
        # Botón de Retiros
        self.withdrawals_button = ttk.Button(
            buttons_frame,
            text="📤 Retiros",
            command=lambda: self.app.show_withdrawals_page(),
            style='Success.TButton',
            width=20,
            state=tk.DISABLED
        )
        self.withdrawals_button.grid(row=0, column=1, padx=10, pady=10)
        
        # Botón de Historial
        self.history_button = ttk.Button(
            buttons_frame,
            text="📊 Historial",
            command=lambda: self.app.show_history_page(),
            style='Info.TButton',
            width=20,
            state=tk.DISABLED
        )
        self.history_button.grid(row=0, column=2, padx=10, pady=10)
        
        # Descripciones
        ttk.Label(
            buttons_frame,
            text="Consultar stock\ny gestionar items",
            font=('Arial', Config.FONT_SIZE_SMALL),
            justify=tk.CENTER
        ).grid(row=1, column=0, padx=10, pady=(0, 10))
        
        ttk.Label(
            buttons_frame,
            text="Realizar retiros\ncon código de barras",
            font=('Arial', Config.FONT_SIZE_SMALL),
            justify=tk.CENTER
        ).grid(row=1, column=1, padx=10, pady=(0, 10))
        
        ttk.Label(
            buttons_frame,
            text="Ver movimientos\ny transacciones",
            font=('Arial', Config.FONT_SIZE_SMALL),
            justify=tk.CENTER
        ).grid(row=1, column=2, padx=10, pady=(0, 10))
    
    def load_warehouses(self):
        warehouses = self.app.data_manager.get_warehouses()
        warehouse_names = [f"{w['name']} - {w['code']}" for w in warehouses]
        self.warehouse_combo['values'] = warehouse_names
        self.warehouses = warehouses
    
    def on_warehouse_selected(self, event):
        selected_index = self.warehouse_combo.current()
        if selected_index >= 0:
            selected_warehouse = self.warehouses[selected_index]
            self.app.session_state.set_warehouse(selected_warehouse)
            self.app.data_manager.set_current_warehouse(selected_warehouse)
            
            # Habilitar botones
            self.inventory_button.config(state=tk.NORMAL)
            self.withdrawals_button.config(state=tk.NORMAL)
            self.history_button.config(state=tk.NORMAL)
            
            # Mostrar mensaje de confirmación
            messagebox.showinfo(
                "Bodega Seleccionada",
                f"Ha seleccionado: {selected_warehouse['name']}\n"
                f"Ubicación: {selected_warehouse['location']}"
            )
    
    def logout(self):
        if messagebox.askyesno("Cerrar Sesión", "¿Está seguro que desea cerrar sesión?"):
            self.app.session_state.logout()
            self.app.data_manager.logout()
            self.app.show_login_page()

# Página de Inventario
class InventoryPage(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header_frame = ttk.Frame(self, style='Header.TFrame')
        header_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Botón de volver
        back_button = ttk.Button(
            header_frame,
            text="← Volver",
            command=lambda: self.app.show_home_page(),
            style='Secondary.TButton'
        )
        back_button.pack(side=tk.LEFT)
        
        # Título
        title_label = ttk.Label(
            header_frame,
            text=f"Inventario - {self.app.session_state.current_warehouse['name']}",
            font=('Arial', Config.FONT_SIZE_LARGE, 'bold'),
            style='Header.TLabel'
        )
        title_label.pack(side=tk.LEFT, padx=20)
        
        # Botones de acción
        buttons_frame = ttk.Frame(header_frame)
        buttons_frame.pack(side=tk.RIGHT)
        
        # Botón agregar stock
        add_stock_button = ttk.Button(
            buttons_frame,
            text="➕ Agregar Stock",
            command=self.show_add_stock_dialog,
            style='Primary.TButton'
        )
        add_stock_button.pack(side=tk.RIGHT, padx=(0, 10))
        
        # Botón nuevo material
        new_material_button = ttk.Button(
            buttons_frame,
            text="✨ Nuevo Material",
            command=self.show_add_item_dialog,
            style='Success.TButton'
        )
        new_material_button.pack(side=tk.RIGHT)
        
        # Frame principal
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Barra de búsqueda
        search_frame = ttk.Frame(main_frame)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(
            search_frame,
            text="Buscar:",
            font=('Arial', Config.FONT_SIZE_MEDIUM)
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.on_search_changed)
        search_entry = ttk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=('Arial', Config.FONT_SIZE_MEDIUM),
            width=40
        )
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Frame para la lista de items
        list_frame = ttk.LabelFrame(
            main_frame,
            text="Items en Inventario",
            padding=10
        )
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview para mostrar items
        self.tree = ttk.Treeview(
            list_frame,
            columns=('barcode', 'stock', 'obra', 'factura'),
            show='tree headings',
            yscrollcommand=scrollbar.set,
            height=15
        )
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.tree.yview)
        
        # Configurar columnas
        self.tree.heading('#0', text='Nombre')
        self.tree.heading('barcode', text='Código')
        self.tree.heading('stock', text='Stock')
        self.tree.heading('obra', text='Obra')
        self.tree.heading('factura', text='Factura')
        
        self.tree.column('#0', width=200)
        self.tree.column('barcode', width=120)
        self.tree.column('stock', width=80)
        self.tree.column('obra', width=150)
        self.tree.column('factura', width=100)
        
        # Frame de información
        info_frame = ttk.Frame(main_frame)
        info_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.info_label = ttk.Label(
            info_frame,
            text="",
            font=('Arial', Config.FONT_SIZE_MEDIUM)
        )
        self.info_label.pack()
        
        # Cargar items
        self.load_items()
    
    def load_items(self, search_query=None):
        # Limpiar árbol
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Obtener items
        warehouse_id = str(self.app.session_state.current_warehouse['id'])
        
        if search_query:
            items = self.app.data_manager.search_items(search_query, warehouse_id)
        else:
            items = self.app.data_manager.get_items_by_warehouse(warehouse_id)
        
        # Agregar items al árbol
        for item in items:
            # Color según stock
            tags = []
            if item['stock'] == 0:
                tags.append('no_stock')
            elif item['stock'] < 10:
                tags.append('low_stock')
            
            self.tree.insert(
                '',
                'end',
                text=item['name'],
                values=(
                    item['barcode'],
                    item['stock'],
                    item['obra'],
                    item['n_factura']
                ),
                tags=tags
            )
        
        # Configurar tags
        self.tree.tag_configure('no_stock', foreground='red')
        self.tree.tag_configure('low_stock', foreground='orange')
        
        self.update_info()
    
    def on_search_changed(self, *args):
        search_query = self.search_var.get()
        if len(search_query) >= 2:
            self.load_items(search_query)
        elif len(search_query) == 0:
            self.load_items()
    
    def update_info(self):
        total_items = len(self.tree.get_children())
        warehouse_name = self.app.session_state.current_warehouse['name']
        self.info_label.config(text=f"Total de items en {warehouse_name}: {total_items}")
    
    def show_add_stock_dialog(self):
        dialog = tk.Toplevel(self)
        dialog.title("Agregar Stock")
        dialog.geometry("600x400")
        dialog.transient(self)
        dialog.grab_set()
        
        # Frame principal
        main_frame = ttk.Frame(dialog, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        ttk.Label(
            main_frame,
            text="Agregar Stock a Item Existente",
            font=('Arial', Config.FONT_SIZE_LARGE, 'bold')
        ).pack(pady=(0, 20))
        
        # Buscar item
        search_frame = ttk.LabelFrame(main_frame, text="Buscar Item", padding=10)
        search_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Scanner de código de barras
        self.stock_scanner = BarcodeScanner(
            search_frame,
            on_scan=lambda barcode: self.search_item_for_stock(barcode, dialog),
            placeholder="Escanear código de barras del item"
        )
        self.stock_scanner.pack(fill=tk.X, pady=(0, 10))
        
        # O buscar por nombre
        ttk.Label(search_frame, text="O buscar por nombre:", font=('Arial', Config.FONT_SIZE_MEDIUM)).pack(anchor=tk.W)
        
        search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=search_var, font=('Arial', Config.FONT_SIZE_MEDIUM), width=40)
        search_entry.pack(fill=tk.X, pady=(5, 10))
        search_entry.bind('<KeyRelease>', lambda e: self.search_items_for_stock(search_var.get(), dialog))
        
        # Lista de items encontrados
        list_frame = ttk.LabelFrame(main_frame, text="Items Encontrados", padding=10)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Treeview para items
        self.stock_tree = ttk.Treeview(
            list_frame,
            columns=('barcode', 'stock', 'obra'),
            show='tree headings',
            height=8
        )
        self.stock_tree.pack(fill=tk.BOTH, expand=True)
        
        self.stock_tree.heading('#0', text='Nombre')
        self.stock_tree.heading('barcode', text='Código')
        self.stock_tree.heading('stock', text='Stock Actual')
        self.stock_tree.heading('obra', text='Obra')
        
        self.stock_tree.column('#0', width=200)
        self.stock_tree.column('barcode', width=120)
        self.stock_tree.column('stock', width=100)
        self.stock_tree.column('obra', width=150)
        
        # Doble click para seleccionar
        self.stock_tree.bind('<Double-1>', lambda e: self.select_item_for_stock(dialog))
        
        # Botones
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(
            button_frame,
            text="Cancelar",
            command=dialog.destroy,
            style='Secondary.TButton'
        ).pack(side=tk.LEFT)
        
        ttk.Button(
            button_frame,
            text="Seleccionar Item",
            command=lambda: self.select_item_for_stock(dialog),
            style='Primary.TButton'
        ).pack(side=tk.RIGHT)
        
        # Focus en el scanner
        self.stock_scanner.focus()
    
    def search_item_for_stock(self, barcode, dialog):
        """Buscar item por código de barras para agregar stock"""
        item = self.app.data_manager.get_item_by_barcode(barcode)
        if item:
            # Verificar que pertenece a la bodega actual
            if str(item['warehouse_id']) == str(self.app.session_state.current_warehouse['id']):
                self.show_quantity_dialog_for_stock(item, dialog)
            else:
                messagebox.showerror("Error", "El item no pertenece a esta bodega")
        else:
            messagebox.showerror("Error", f"No se encontró item con código: {barcode}")
    
    def search_items_for_stock(self, query, dialog):
        """Buscar items por nombre para agregar stock"""
        if len(query) < 2:
            # Limpiar lista
            for item in self.stock_tree.get_children():
                self.stock_tree.delete(item)
            return
        
        warehouse_id = str(self.app.session_state.current_warehouse['id'])
        items = self.app.data_manager.search_items(query, warehouse_id)
        
        # Limpiar y llenar lista
        for item in self.stock_tree.get_children():
            self.stock_tree.delete(item)
        
        for item in items:
            self.stock_tree.insert(
                '',
                'end',
                text=item['name'],
                values=(item['barcode'], item['stock'], item['obra']),
                tags=[str(item['id'])]  # Guardar ID en tags
            )
    
    def select_item_for_stock(self, dialog):
        """Seleccionar item de la lista para agregar stock"""
        selected = self.stock_tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un item de la lista")
            return
        
        # Obtener item seleccionado
        item_data = self.stock_tree.item(selected[0])
        item_id = item_data['tags'][0] if item_data['tags'] else None
        
        if not item_id:
            messagebox.showerror("Error", "No se pudo obtener el ID del item")
            return
        
        # Buscar item completo
        warehouse_id = str(self.app.session_state.current_warehouse['id'])
        items = self.app.data_manager.get_items_by_warehouse(warehouse_id)
        selected_item = next((item for item in items if str(item['id']) == item_id), None)
        
        if selected_item:
            self.show_quantity_dialog_for_stock(selected_item, dialog)
        else:
            messagebox.showerror("Error", "No se encontró el item seleccionado")
    
    def show_quantity_dialog_for_stock(self, item, parent_dialog):
        """Mostrar diálogo para ingresar cantidad a agregar"""
        parent_dialog.destroy()  # Cerrar diálogo de búsqueda
        
        dialog = tk.Toplevel(self)
        dialog.title(f"Agregar Stock: {item['name']}")
        dialog.geometry("400x300")
        dialog.transient(self)
        dialog.grab_set()
        
        # Frame principal
        main_frame = ttk.Frame(dialog, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Información del item
        ttk.Label(
            main_frame,
            text=f"Item: {item['name']}",
            font=('Arial', Config.FONT_SIZE_MEDIUM, 'bold')
        ).pack(pady=5)
        
        ttk.Label(
            main_frame,
            text=f"Stock actual: {item['stock']}",
            font=('Arial', Config.FONT_SIZE_MEDIUM)
        ).pack(pady=5)

        ttk.Label(
            main_frame,
            text=f"Codigo: {item['barcode']}",
            font=('Arial', Config.FONT_SIZE_MEDIUM)
        ).pack(pady=5)
                
        # Campo de cantidad
        quantity_frame = ttk.Frame(main_frame)
        quantity_frame.pack(pady=20)
        
        ttk.Label(
            quantity_frame,
            text="Cantidad a agregar:",
            font=('Arial', Config.FONT_SIZE_MEDIUM)
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        quantity_var = tk.StringVar(value="1")
        quantity_spinbox = ttk.Spinbox(
            quantity_frame,
            from_=1,
            to=9999,
            textvariable=quantity_var,
            font=('Arial', Config.FONT_SIZE_MEDIUM),
            width=10
        )
        quantity_spinbox.pack(side=tk.LEFT)
        
        # Mensaje de error
        error_label = ttk.Label(main_frame, text="", foreground='red')
        error_label.pack(pady=10)
        
        # Botones
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=10)
        
        def add_stock():
            try:
                quantity = int(quantity_var.get())
                if quantity <= 0:
                    error_label.config(text="La cantidad debe ser mayor a 0")
                    return
                
                # Agregar stock
                success = self.app.data_manager.add_item_stock(str(item['id']), quantity)
                
                if success:
                    # Actualizar lista
                    self.load_items()
                    dialog.destroy()
                    messagebox.showinfo("Éxito", f"Se agregaron {quantity} unidades al stock de '{item['name']}'")
                else:
                    error_label.config(text="Error al agregar stock")
                
            except ValueError:
                error_label.config(text="Ingrese una cantidad válida")
            except Exception as e:
                error_label.config(text=f"Error: {str(e)}")
        
        ttk.Button(
            button_frame,
            text="Cancelar",
            command=dialog.destroy,
            style='Secondary.TButton'
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text="Agregar Stock",
            command=add_stock,
            style='Primary.TButton'
        ).pack(side=tk.LEFT, padx=5)
        
        # Focus en el spinbox
        quantity_spinbox.focus()
    
    def show_add_item_dialog(self):
        dialog = tk.Toplevel(self)
        dialog.title("Agregar Nuevo Material")
        dialog.geometry("500x600")
        dialog.transient(self)
        dialog.grab_set()
        
        # Frame principal
        main_frame = ttk.Frame(dialog, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        ttk.Label(
            main_frame,
            text="Agregar Nuevo Material",
            font=('Arial', Config.FONT_SIZE_LARGE, 'bold')
        ).grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Campos del formulario
        fields = []
        
        # Nombre
        ttk.Label(main_frame, text="Nombre:", font=('Arial', Config.FONT_SIZE_MEDIUM)).grid(
            row=1, column=0, sticky=tk.W, pady=5
        )
        name_var = tk.StringVar()
        name_entry = ttk.Entry(main_frame, textvariable=name_var, font=('Arial', Config.FONT_SIZE_MEDIUM), width=30)
        name_entry.grid(row=1, column=1, pady=5, sticky=tk.W)
        fields.append(('name', name_var))
        
        # Descripción
        ttk.Label(main_frame, text="Descripción:", font=('Arial', Config.FONT_SIZE_MEDIUM)).grid(
            row=2, column=0, sticky=tk.W, pady=5
        )
        desc_var = tk.StringVar()
        desc_entry = ttk.Entry(main_frame, textvariable=desc_var, font=('Arial', Config.FONT_SIZE_MEDIUM), width=30)
        desc_entry.grid(row=2, column=1, pady=5, sticky=tk.W)
        fields.append(('description', desc_var))
        
        # Código de barras
        ttk.Label(main_frame, text="Código de barras:", font=('Arial', Config.FONT_SIZE_MEDIUM)).grid(
            row=3, column=0, sticky=tk.W, pady=5
        )
        barcode_var = tk.StringVar()
        barcode_entry = ttk.Entry(main_frame, textvariable=barcode_var, font=('Arial', Config.FONT_SIZE_MEDIUM), width=30)
        barcode_entry.grid(row=3, column=1, pady=5, sticky=tk.W)
        fields.append(('barcode', barcode_var))
        
        # Stock inicial
        ttk.Label(main_frame, text="Stock inicial:", font=('Arial', Config.FONT_SIZE_MEDIUM)).grid(
            row=4, column=0, sticky=tk.W, pady=5
        )
        stock_var = tk.StringVar(value="0")
        stock_entry = ttk.Entry(main_frame, textvariable=stock_var, font=('Arial', Config.FONT_SIZE_MEDIUM), width=30)
        stock_entry.grid(row=4, column=1, pady=5, sticky=tk.W)
        fields.append(('stock', stock_var))
        
        # Obra
        ttk.Label(main_frame, text="Obra:", font=('Arial', Config.FONT_SIZE_MEDIUM)).grid(
            row=5, column=0, sticky=tk.W, pady=5
        )
        obra_var = tk.StringVar()
        obra_entry = ttk.Entry(main_frame, textvariable=obra_var, font=('Arial', Config.FONT_SIZE_MEDIUM), width=30)
        obra_entry.grid(row=5, column=1, pady=5, sticky=tk.W)
        fields.append(('obra', obra_var))
        
        # Número de factura
        ttk.Label(main_frame, text="N° Factura:", font=('Arial', Config.FONT_SIZE_MEDIUM)).grid(
            row=6, column=0, sticky=tk.W, pady=5
        )
        factura_var = tk.StringVar()
        factura_entry = ttk.Entry(main_frame, textvariable=factura_var, font=('Arial', Config.FONT_SIZE_MEDIUM), width=30)
        factura_entry.grid(row=6, column=1, pady=5, sticky=tk.W)
        fields.append(('n_factura', factura_var))
        
        # Mensaje de error
        error_label = ttk.Label(main_frame, text="", foreground='red', font=('Arial', Config.FONT_SIZE_SMALL))
        error_label.grid(row=7, column=0, columnspan=2, pady=10)
        
        # Botones
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=8, column=0, columnspan=2, pady=20)
        
        def save_item():
            # Validar campos
            data = {}
            for field_name, field_var in fields:
                value = field_var.get().strip()
                if field_name in ['name', 'barcode'] and not value:
                    error_label.config(text=f"El campo {field_name} es obligatorio")
                    return
                data[field_name] = value
            
            # Convertir tipos
            try:
                data['stock'] = int(data.get('stock', 0))
            except ValueError:
                error_label.config(text="Stock debe ser un número válido")
                return
            
            # Agregar warehouse_id
            data['warehouse_id'] = str(self.app.session_state.current_warehouse['id'])
            
            # Si no se especifica obra o factura, usar valores por defecto
            if not data['obra']:
                data['obra'] = self.app.session_state.current_warehouse['name']
            if not data['n_factura']:
                data['n_factura'] = self.app.session_state.current_warehouse['code']
            
            try:
                # Crear item
                if self.app.data_manager.add_item(data):
                    # Actualizar lista
                    self.load_items()
                    
                    # Cerrar diálogo
                    dialog.destroy()
                    
                    messagebox.showinfo("Éxito", "Item agregado correctamente")
                else:
                    error_label.config(text="Error al crear el item")
                
            except Exception as e:
                error_label.config(text=str(e))
        
        ttk.Button(
            button_frame,
            text="Cancelar",
            command=dialog.destroy,
            style='Secondary.TButton'
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text="Guardar",
            command=save_item,
            style='Primary.TButton'
        ).pack(side=tk.LEFT, padx=5)
        
        # Focus en el primer campo
        name_entry.focus()

# Página de Retiros
class WithdrawalsPage(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.withdrawal_items = []
        self.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header_frame = ttk.Frame(self, style='Header.TFrame')
        header_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Botón de volver
        back_button = ttk.Button(
            header_frame,
            text="← Volver",
            command=lambda: self.app.show_home_page(),
            style='Secondary.TButton'
        )
        back_button.pack(side=tk.LEFT)
        
        # Título
        title_label = ttk.Label(
            header_frame,
            text=f"Retiros - {self.app.session_state.current_warehouse['name']}",
            font=('Arial', Config.FONT_SIZE_LARGE, 'bold'),
            style='Header.TLabel'
        )
        title_label.pack(side=tk.LEFT, padx=20)
        
        # Frame principal
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Frame superior para scanner y obra
        top_frame = ttk.Frame(main_frame)
        top_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Scanner de código de barras
        scanner_frame = ttk.LabelFrame(top_frame, text="Escanear Item", padding=10)
        scanner_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.barcode_scanner = BarcodeScanner(
            scanner_frame,
            on_scan=self.on_barcode_scan,
            placeholder="Escanear código de barras para retiro"
        )
        self.barcode_scanner.pack(fill=tk.X)
        
        # Campo de obra
        obra_frame = ttk.LabelFrame(top_frame, text="Información del Retiro", padding=10)
        obra_frame.pack(fill=tk.X)
        
        ttk.Label(
            obra_frame,
            text="Obra:",
            font=('Arial', Config.FONT_SIZE_MEDIUM)
        ).grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        
        self.obra_var = tk.StringVar()
        obra_entry = ttk.Entry(
            obra_frame,
            textvariable=self.obra_var,
            font=('Arial', Config.FONT_SIZE_MEDIUM),
            width=40
        )
        obra_entry.grid(row=0, column=1, sticky=tk.W)
        
        # Lista de items para retiro
        list_frame = ttk.LabelFrame(
            main_frame,
            text="Items para Retiro",
            padding=10
        )
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview para mostrar items
        self.tree = ttk.Treeview(
            list_frame,
            columns=('barcode', 'obra', 'factura', 'stock_disponible', 'cantidad'),
            show='tree headings',
            yscrollcommand=scrollbar.set,
            height=10
        )
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.tree.yview)
        
        # Configurar columnas
        self.tree.heading('#0', text='Nombre')
        self.tree.heading('barcode', text='Código')
        self.tree.heading('obra', text='Obra')
        self.tree.heading('factura', text='Factura')
        self.tree.heading('stock_disponible', text='Stock Disp.')
        self.tree.heading('cantidad', text='Cantidad')
        
        self.tree.column('#0', width=200)
        self.tree.column('barcode', width=120)
        self.tree.column('obra', width=150)
        self.tree.column('factura', width=100)
        self.tree.column('stock_disponible', width=100)
        self.tree.column('cantidad', width=100)
        
        # Botones de acción
        action_frame = ttk.Frame(list_frame)
        action_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(
            action_frame,
            text="🗑️ Eliminar Seleccionado",
            command=self.remove_selected_item,
            style='Danger.TButton'
        ).pack(side=tk.LEFT, padx=5)
        
        # Frame inferior para confirmar retiro
        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.pack(fill=tk.X, pady=(20, 0))
        
        self.confirm_button = ttk.Button(
            bottom_frame,
            text="✓ Confirmar Retiro",
            command=self.confirm_withdrawal,
            style='Success.TButton',
            width=30,
            state=tk.DISABLED
        )
        self.confirm_button.pack()
        
        # Focus en el scanner
        self.barcode_scanner.focus()
    
    def on_barcode_scan(self, barcode):
        try:
            # Buscar item por código de barras
            item = self.app.data_manager.get_item_by_barcode(barcode)
            if not item:
                messagebox.showerror("Error", f"No se encontró item con código: {barcode}")
                return
            
            # Verificar que el item pertenece a la bodega actual
            if str(item['warehouse_id']) != str(self.app.session_state.current_warehouse['id']):
                messagebox.showerror(
                    "Error",
                    f"El item '{item['name']}' no pertenece a esta bodega.\n"
                    f"Solo se pueden retirar items de la bodega actual."
                )
                return
            
            # Verificar stock
            if item['stock'] <= 0:
                messagebox.showerror(
                    "Error",
                    f"El item '{item['name']}' no tiene stock disponible"
                )
                return
            
            # Mostrar diálogo de cantidad
            self.show_quantity_dialog(item)
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def show_quantity_dialog(self, item):
        dialog = tk.Toplevel(self)
        dialog.title(f"Retirar: {item['name']}")
        dialog.geometry("400x400")
        dialog.transient(self)
        dialog.grab_set()
        
        # Frame principal
        main_frame = ttk.Frame(dialog, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Información del item
        ttk.Label(
            main_frame,
            text=f"Item: {item['name']}",
            font=('Arial', Config.FONT_SIZE_MEDIUM, 'bold')
        ).pack(pady=5)
        
        ttk.Label(
            main_frame,
            text=f"Stock disponible: {item['stock']}",
            font=('Arial', Config.FONT_SIZE_MEDIUM)
        ).pack(pady=5)
        
        ttk.Label(
            main_frame,
            text=f"Obra del item: {item['obra']}",
            font=('Arial', Config.FONT_SIZE_MEDIUM)
        ).pack(pady=5)
        
        ttk.Label(
            main_frame,
            text=f"Factura: {item['n_factura']}",
            font=('Arial', Config.FONT_SIZE_MEDIUM)
        ).pack(pady=5)
        
        # Campo de cantidad
        quantity_frame = ttk.Frame(main_frame)
        quantity_frame.pack(pady=20)
        
        ttk.Label(
            quantity_frame,
            text="Cantidad a retirar:",
            font=('Arial', Config.FONT_SIZE_MEDIUM)
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        quantity_var = tk.StringVar(value="1")
        quantity_spinbox = ttk.Spinbox(
            quantity_frame,
            from_=1,
            to=item['stock'],
            textvariable=quantity_var,
            font=('Arial', Config.FONT_SIZE_MEDIUM),
            width=10
        )
        quantity_spinbox.pack(side=tk.LEFT)
        
        # Mensaje de error
        error_label = ttk.Label(main_frame, text="", foreground='red')
        error_label.pack(pady=10)
        
        # Botones
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=10)
        
        def add_to_withdrawal():
            try:
                quantity = int(quantity_var.get())
                if quantity <= 0:
                    error_label.config(text="La cantidad debe ser mayor a 0")
                    return
                
                if quantity > item['stock']:
                    error_label.config(text=f"Cantidad máxima disponible: {item['stock']}")
                    return
                
                # Verificar si el item ya está en la lista
                for i, wi in enumerate(self.withdrawal_items):
                    if wi['item']['id'] == item['id']:
                        # Actualizar cantidad
                        new_quantity = wi['quantity'] + quantity
                        if new_quantity > item['stock']:
                            error_label.config(text="La cantidad total excede el stock disponible")
                            return
                        wi['quantity'] = new_quantity
                        self.update_withdrawal_list()
                        dialog.destroy()
                        return
                
                # Agregar nuevo item
                self.withdrawal_items.append({
                    'item': item,
                    'quantity': quantity
                })
                
                self.update_withdrawal_list()
                dialog.destroy()
                
            except ValueError:
                error_label.config(text="Ingrese una cantidad válida")
        
        dialog.bind("<Return>", lambda event: add_to_withdrawal())
        
        ttk.Button(
            button_frame,
            text="Cancelar",
            command=dialog.destroy,
            style='Secondary.TButton'
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text="Agregar",
            command=add_to_withdrawal,
            style='Primary.TButton'
        ).pack(side=tk.LEFT, padx=5)
        
        # Focus en el spinbox
        quantity_spinbox.focus()
    
    def update_withdrawal_list(self):
        # Limpiar árbol
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Agregar items
        for wi in self.withdrawal_items:
            item = wi['item']
            self.tree.insert(
                '',
                'end',
                text=item['name'],
                values=(
                    item['barcode'],
                    item['obra'],
                    item['n_factura'],
                    item['stock'],
                    wi['quantity']
                )
            )
        
        # Habilitar/deshabilitar botón de confirmar
        self.confirm_button.config(
            state=tk.NORMAL if self.withdrawal_items else tk.DISABLED
        )
    
    def remove_selected_item(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un item para eliminar")
            return
        
        # Obtener índice del item seleccionado
        index = self.tree.index(selected[0])
        
        # Eliminar de la lista
        del self.withdrawal_items[index]
        
        # Actualizar vista
        self.update_withdrawal_list()
    
    def confirm_withdrawal(self):
        # Validar obra
        if not self.obra_var.get().strip():
            messagebox.showerror("Error", "Debe especificar la obra")
            return
        
        if not self.withdrawal_items:
            messagebox.showerror("Error", "Debe agregar al menos un item")
            return
        
        # Confirmar acción
        total_items = sum(wi['quantity'] for wi in self.withdrawal_items)
        if not messagebox.askyesno(
            "Confirmar Retiro",
            f"¿Confirmar retiro de {total_items} items para la obra '{self.obra_var.get()}'?"
        ):
            return
        
        try:
            # Procesar retiro
            if self.app.data_manager.process_withdrawal(self.withdrawal_items, self.obra_var.get().strip()):
                # Limpiar formulario
                self.withdrawal_items.clear()
                self.obra_var.set("")
                self.update_withdrawal_list()
                self.barcode_scanner.clear()
                
                messagebox.showinfo("Éxito", "Retiro confirmado exitosamente")
            else:
                messagebox.showerror("Error", "Error al procesar el retiro")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al confirmar retiro: {str(e)}")

# Página de Historial
class HistoryPage(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header_frame = ttk.Frame(self, style='Header.TFrame')
        header_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Botón de volver
        back_button = ttk.Button(
            header_frame,
            text="← Volver",
            command=lambda: self.app.show_home_page(),
            style='Secondary.TButton'
        )
        back_button.pack(side=tk.LEFT)
        
        # Título
        title_label = ttk.Label(
            header_frame,
            text=f"Historial - {self.app.session_state.current_warehouse['name']}",
            font=('Arial', Config.FONT_SIZE_LARGE, 'bold'),
            style='Header.TLabel'
        )
        title_label.pack(side=tk.LEFT, padx=20)
        
        # Botón actualizar
        refresh_button = ttk.Button(
            header_frame,
            text="🔄 Actualizar",
            command=self.load_history,
            style='Primary.TButton'
        )
        refresh_button.pack(side=tk.RIGHT)
        
        # Frame principal
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Tabla de historial
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview
        self.tree = ttk.Treeview(
            tree_frame,
            columns=('fecha', 'accion', 'item', 'cantidad', 'obra', 'usuario'),
            show='headings',
            yscrollcommand=scrollbar.set,
            height=20
        )
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.tree.yview)
        
        # Configurar columnas
        self.tree.heading('fecha', text='Fecha y Hora')
        self.tree.heading('accion', text='Acción')
        self.tree.heading('item', text='Item')
        self.tree.heading('cantidad', text='Cantidad')
        self.tree.heading('obra', text='Obra')
        self.tree.heading('usuario', text='Usuario')
        
        self.tree.column('fecha', width=150)
        self.tree.column('accion', width=100)
        self.tree.column('item', width=200)
        self.tree.column('cantidad', width=100)
        self.tree.column('obra', width=150)
        self.tree.column('usuario', width=150)
        
        # Cargar historial
        self.load_history()
    
    def load_history(self):
        """Cargar historial de movimientos"""
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Cargar datos
        history = self.app.data_manager.get_history()
        
        for record in history:
            # Formatear fecha
            try:
                from datetime import datetime
                if isinstance(record['action_date'], str):
                    date_obj = datetime.fromisoformat(record['action_date'].replace('Z', '+00:00'))
                    formatted_date = date_obj.strftime('%d/%m/%Y %H:%M')
                else:
                    formatted_date = str(record['action_date'])
            except:
                formatted_date = str(record['action_date'])
            
            # Traducir tipo de acción
            action_translations = {
                'withdrawal': 'Retiro',
                'addition': 'Adición',
                'adjustment': 'Ajuste'
            }
            action_text = action_translations.get(record['action_type'], record['action_type'])
            
            # Color según tipo de acción
            tags = []
            if record['action_type'] == 'withdrawal':
                tags.append('withdrawal')
            elif record['action_type'] == 'addition':
                tags.append('addition')
            
            self.tree.insert('', 'end', values=(
                formatted_date,
                action_text,
                record['item_name'],
                record['quantity'],
                record['obra'],
                record['user_name']
            ), tags=tags)
        
        # Configurar colores
        self.tree.tag_configure('withdrawal', foreground='red')
        self.tree.tag_configure('addition', foreground='green')

# Aplicación Principal
class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title(Config.APP_TITLE)
        self.root.geometry("1024x768")
        
        # Centrar ventana
        self.center_window()
        
        # Configurar estilos
        self.setup_styles()
        
        # Inicializar componentes
        self.session_state = SessionState()
        self.session_state.app = self  # Agregar referencia a la app
        self.data_manager = DataManager()
        
        # Frame principal
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Mostrar login
        self.current_page = None
        self.show_login_page()
        
        # Configurar cierre de ventana
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def center_window(self):
        """Centrar la ventana en la pantalla"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_styles(self):
        """Configurar estilos de ttk"""
        style = ttk.Style()
        
        # Configurar colores de fondo
        style.configure('Background.TFrame', background=Config.BACKGROUND_COLOR)
        style.configure('Card.TFrame', background=Config.WHITE)
        style.configure('Card.TLabel', background=Config.WHITE)
        style.configure('Header.TFrame', background=Config.WHITE)
        style.configure('Header.TLabel', background=Config.WHITE)
        
        # Configurar botones
        style.configure(
            'Primary.TButton',
            font=('Arial', Config.FONT_SIZE_MEDIUM),
            foreground='white',
            background=Config.PRIMARY_COLOR,
            borderwidth=0,
            focuscolor='none'
        )
        style.map('Primary.TButton',
            background=[('active', '#1565C0')]
        )
        
        style.configure(
            'Success.TButton',
            font=('Arial', Config.FONT_SIZE_MEDIUM),
            foreground='white',
            background=Config.SUCCESS_COLOR,
            borderwidth=0,
            focuscolor='none'
        )
        style.map('Success.TButton',
            background=[('active', '#388E3C')]
        )
        
        style.configure(
            'Secondary.TButton',
            font=('Arial', Config.FONT_SIZE_MEDIUM),
            background='#E0E0E0',
            borderwidth=0,
            focuscolor='none'
        )
        style.map('Secondary.TButton',
            background=[('active', '#BDBDBD')]
        )
        
        style.configure(
            'Danger.TButton',
            font=('Arial', Config.FONT_SIZE_MEDIUM),
            foreground='white',
            background=Config.ERROR_COLOR,
            borderwidth=0,
            focuscolor='none'
        )
        style.map('Danger.TButton',
            background=[('active', '#D32F2F')]
        )
        
        style.configure(
            'Info.TButton',
            font=('Arial', Config.FONT_SIZE_MEDIUM),
            foreground='white',
            background=Config.SECONDARY_COLOR,
            borderwidth=0,
            focuscolor='none'
        )
        style.map('Info.TButton',
            background=[('active', '#303030')]
        )
        
        # Configurar Treeview
        style.configure(
            'Treeview',
            font=('Arial', Config.FONT_SIZE_SMALL),
            rowheight=30
        )
        style.configure(
            'Treeview.Heading',
            font=('Arial', Config.FONT_SIZE_SMALL, 'bold')
        )
    
    def clear_frame(self):
        """Limpiar el frame principal"""
        if self.current_page:
            self.current_page.destroy()
    
    def show_login_page(self):
        self.clear_frame()
        self.current_page = LoginPage(self.main_frame, self)
    
    def show_home_page(self):
        self.clear_frame()
        self.current_page = HomePage(self.main_frame, self)
    
    def show_inventory_page(self):
        self.clear_frame()
        self.current_page = InventoryPage(self.main_frame, self)
    
    def show_withdrawals_page(self):
        self.clear_frame()
        self.current_page = WithdrawalsPage(self.main_frame, self)
    
    def show_history_page(self):
        self.clear_frame()
        self.current_page = HistoryPage(self.main_frame, self)
    
    def on_closing(self):
        """Manejar cierre de la aplicación"""
        if self.session_state.is_authenticated:
            if messagebox.askyesno("Salir", "¿Está seguro que desea salir del sistema?"):
                self.root.destroy()
        else:
            self.root.destroy()

# Función principal
def main():
    root = tk.Tk()
    app = InventoryApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
    