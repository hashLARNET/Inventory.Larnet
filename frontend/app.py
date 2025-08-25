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
        def ir_al_home():
            try:
                print("¡Botón presionado!")
                # Destruir la página actual primero
                self.destroy()
                # Limpiar el frame principal
                for widget in self.app.main_frame.winfo_children():
                    widget.destroy()
                # Crear nueva página de inicio
                self.app.current_page = HomePage(self.app.main_frame, self.app)
                print("Página de inicio creada")
            except Exception as e:
                print(f"Error: {e}")

        back_button = ttk.Button(
            header_frame,
            text="← Volver",
            command=ir_al_home,
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
        
        # Botón transferir entre obras
        transfer_button = ttk.Button(
            buttons_frame,
            text="🔄 Transferir entre Obras",
            command=self.show_transfer_dialog,
            style='Info.TButton'
        )
        transfer_button.pack(side=tk.RIGHT, padx=(0, 10))
        
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
        
        # Frame de filtros
        filters_frame = ttk.LabelFrame(main_frame, text="Filtros de Visualización", padding=10)
        filters_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Primera fila de filtros
        filter_row1 = ttk.Frame(filters_frame)
        filter_row1.pack(fill=tk.X, pady=5)
        
        # Filtro por obra
        ttk.Label(
            filter_row1,
            text="Filtrar por Obra:",
            font=('Arial', Config.FONT_SIZE_MEDIUM)
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.obra_filter_var = tk.StringVar()
        self.obra_filter_combo = ttk.Combobox(
            filter_row1,
            textvariable=self.obra_filter_var,
            font=('Arial', Config.FONT_SIZE_MEDIUM),
            state='readonly',
            width=30
        )
        self.obra_filter_combo.pack(side=tk.LEFT, padx=(0, 10))
        self.obra_filter_combo.bind('<<ComboboxSelected>>', self.on_obra_filter_changed)
        
        # Botón limpiar filtro
        clear_filter_button = ttk.Button(
            filter_row1,
            text="Limpiar Filtro",
            command=self.clear_obra_filter,
            style='Secondary.TButton'
        )
        clear_filter_button.pack(side=tk.LEFT, padx=(0, 20))
        
        # Modo de visualización
        ttk.Label(
            filter_row1,
            text="Vista:",
            font=('Arial', Config.FONT_SIZE_MEDIUM)
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.view_mode_var = tk.StringVar(value="detallado")
        view_modes = [
            ("Detallado", "detallado"),
            ("Por Obra", "por_obra"),
            ("Resumen", "resumen")
        ]
        
        for text, value in view_modes:
            ttk.Radiobutton(
                filter_row1,
                text=text,
                variable=self.view_mode_var,
                value=value,
                command=self.on_view_mode_changed
            ).pack(side=tk.LEFT, padx=(0, 10))
        
        # Segunda fila - Barra de búsqueda
        filter_row2 = ttk.Frame(filters_frame)
        filter_row2.pack(fill=tk.X, pady=5)
        
        ttk.Label(
            filter_row2,
            text="Buscar:",
            font=('Arial', Config.FONT_SIZE_MEDIUM)
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.on_search_changed)
        search_entry = ttk.Entry(
            filter_row2,
            textvariable=self.search_var,
            font=('Arial', Config.FONT_SIZE_MEDIUM),
            width=50
        )
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        # Botón búsqueda avanzada
        advanced_search_button = ttk.Button(
            filter_row2,
            text="🔍 Búsqueda Avanzada",
            command=self.show_advanced_search
        )
        advanced_search_button.pack(side=tk.LEFT)
        
        # Notebook para diferentes vistas
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Vista detallada
        self.detailed_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.detailed_frame, text="📋 Vista Detallada")
        
        # Scrollbar para vista detallada
        scrollbar_detailed = ttk.Scrollbar(self.detailed_frame)
        scrollbar_detailed.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview para vista detallada
        self.tree_detailed = ttk.Treeview(
            self.detailed_frame,
            columns=('barcode', 'stock', 'obra', 'factura', 'ubicacion'),
            show='tree headings',
            yscrollcommand=scrollbar_detailed.set,
            height=15
        )
        self.tree_detailed.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_detailed.config(command=self.tree_detailed.yview)
        
        # Configurar columnas vista detallada
        self.tree_detailed.heading('#0', text='Nombre del Material')
        self.tree_detailed.heading('barcode', text='Código')
        self.tree_detailed.heading('stock', text='Stock')
        self.tree_detailed.heading('obra', text='Obra')
        self.tree_detailed.heading('factura', text='Factura')
        self.tree_detailed.heading('ubicacion', text='Ubicación')
        
        self.tree_detailed.column('#0', width=250)
        self.tree_detailed.column('barcode', width=120)
        self.tree_detailed.column('stock', width=80)
        self.tree_detailed.column('obra', width=150)
        self.tree_detailed.column('factura', width=100)
        self.tree_detailed.column('ubicacion', width=150)
        
        # Bind para doble click en vista detallada
        self.tree_detailed.bind('<Double-1>', self.on_item_double_click)
        
        # Vista por obra
        self.obra_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.obra_frame, text="🏗️ Vista por Obra")
        
        # Frame para controles de vista por obra
        obra_controls_frame = ttk.Frame(self.obra_frame)
        obra_controls_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(
            obra_controls_frame,
            text="🔄 Actualizar Vista",
            command=self.load_obra_summary
        ).pack(side=tk.LEFT)
        
        ttk.Button(
            obra_controls_frame,
            text="📊 Expandir Todo",
            command=self.expand_all_obras
        ).pack(side=tk.LEFT, padx=(10, 0))
        
        ttk.Button(
            obra_controls_frame,
            text="📁 Contraer Todo",
            command=self.collapse_all_obras
        ).pack(side=tk.LEFT, padx=(10, 0))
        
        # Scrollbar para vista por obra
        scrollbar_obra = ttk.Scrollbar(self.obra_frame)
        scrollbar_obra.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview para vista por obra
        self.tree_obra = ttk.Treeview(
            self.obra_frame,
            columns=('total_items', 'total_stock', 'valor_estimado'),
            show='tree headings',
            yscrollcommand=scrollbar_obra.set,
            height=15
        )
        self.tree_obra.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_obra.config(command=self.tree_obra.yview)
        
        # Configurar columnas vista por obra
        self.tree_obra.heading('#0', text='Obra / Material')
        self.tree_obra.heading('total_items', text='Total Items')
        self.tree_obra.heading('total_stock', text='Stock Total')
        self.tree_obra.heading('valor_estimado', text='Valor Estimado')
        
        self.tree_obra.column('#0', width=300)
        self.tree_obra.column('total_items', width=120)
        self.tree_obra.column('total_stock', width=120)
        self.tree_obra.column('valor_estimado', width=150)
        
        # Bind double click para expandir obra
        self.tree_obra.bind('<Double-1>', self.on_obra_double_click)
        
        # Vista de resumen
        self.summary_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.summary_frame, text="📊 Resumen")
        
        # Frame para métricas de resumen
        metrics_frame = ttk.LabelFrame(self.summary_frame, text="Métricas Generales", padding=10)
        metrics_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.metrics_text = ttk.Label(
            metrics_frame,
            text="Cargando métricas...",
            font=('Arial', Config.FONT_SIZE_MEDIUM)
        )
        self.metrics_text.pack()
        
        # Frame para alertas
        alerts_frame = ttk.LabelFrame(self.summary_frame, text="Alertas de Stock", padding=10)
        alerts_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Treeview para alertas
        self.tree_alerts = ttk.Treeview(
            alerts_frame,
            columns=('stock', 'obra', 'estado'),
            show='tree headings',
            height=10
        )
        self.tree_alerts.pack(fill=tk.BOTH, expand=True)
        
        self.tree_alerts.heading('#0', text='Material')
        self.tree_alerts.heading('stock', text='Stock')
        self.tree_alerts.heading('obra', text='Obra')
        self.tree_alerts.heading('estado', text='Estado')
        
        self.tree_alerts.column('#0', width=250)
        self.tree_alerts.column('stock', width=100)
        self.tree_alerts.column('obra', width=150)
        self.tree_alerts.column('estado', width=120)
        
        # Frame de información y estadísticas
        info_frame = ttk.Frame(main_frame)
        info_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Estadísticas básicas
        stats_frame = ttk.LabelFrame(info_frame, text="Estadísticas Rápidas", padding=5)
        stats_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.stats_label = ttk.Label(
            stats_frame,
            text="",
            font=('Arial', Config.FONT_SIZE_SMALL)
        )
        self.stats_label.pack()
        
        # Botones de acciones rápidas
        quick_actions_frame = ttk.LabelFrame(info_frame, text="Acciones Rápidas", padding=5)
        quick_actions_frame.pack(side=tk.RIGHT, padx=(10, 0))
        
        ttk.Button(
            quick_actions_frame,
            text="📤 Exportar Datos",
            command=self.export_data
        ).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(
            quick_actions_frame,
            text="🔄 Actualizar Todo",
            command=self.refresh_all_data
        ).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(
            quick_actions_frame,
            text="⚠️ Ver Alertas",
            command=self.show_alerts_only
        ).pack(side=tk.LEFT, padx=2)
        
        # Cargar datos iniciales
        self.load_obras_filter()
        self.load_items()
    
    def load_obras_filter(self):
        """Cargar obras disponibles en el filtro"""
        warehouse_id = str(self.app.session_state.current_warehouse['id'])
        obras = self.app.data_manager.get_obras_by_warehouse(warehouse_id)
        
        # Añadir opción "Todas las obras"
        obras_options = ["Todas las obras"] + sorted(obras)
        self.obra_filter_combo['values'] = obras_options
        self.obra_filter_combo.set("Todas las obras")
    
    def on_obra_filter_changed(self, event):
        """Manejar cambio de filtro por obra"""
        self.load_items()
        if self.view_mode_var.get() == "por_obra":
            self.load_obra_summary()
    
    def clear_obra_filter(self):
        """Limpiar filtro de obra"""
        self.obra_filter_combo.set("Todas las obras")
        self.load_items()
    
    def on_view_mode_changed(self):
        """Manejar cambio de modo de vista"""
        view_mode = self.view_mode_var.get()
        if view_mode == "detallado":
            self.notebook.select(0)
            self.load_items()
        elif view_mode == "por_obra":
            self.notebook.select(1)
            self.load_obra_summary()
        elif view_mode == "resumen":
            self.notebook.select(2)
            self.load_summary_view()
    
    def load_items(self, search_query=None):
        """Cargar items con límite y optimizaciones"""
        # Mostrar indicador de carga
        self.tree_detailed.delete(*self.tree_detailed.get_children())
        loading_item = self.tree_detailed.insert('', 'end', text='Cargando...', values=('', '', '', '', ''))
        self.update_idletasks()
        
        try:
            warehouse_id = str(self.app.session_state.current_warehouse['id'])
            
            # Limitar resultados
            if search_query:
                items_data = self.app.data_manager.search_items(search_query, warehouse_id)
                # Extraer solo los items si es necesario
                items = items_data if isinstance(items_data, list) else items_data.get('items', [])
                items = items[:100]  # Limitar a 100 items
            else:
                selected_obra = self.obra_filter_var.get()
                if selected_obra and selected_obra != "Todas las obras":
                    items_data = self.app.data_manager.get_items_by_obra(selected_obra, warehouse_id)
                    # Extraer solo los items si es necesario
                    items = items_data if isinstance(items_data, list) else items_data.get('items', [])
                    items = items[:100]  # Limitar a 100 items

                else:
                    items_data = self.app.data_manager.get_items_by_warehouse(warehouse_id)
                    # Asegurarse de extraer solo los items de la respuesta
                    if isinstance(items_data, dict) and 'items' in items_data:
                        items = items_data['items']
                    else:
                        items = items_data if isinstance(items_data, list) else []
                    items = items[:100]  # Limitar a 100 items
            
            # Eliminar indicador de carga
            self.tree_detailed.delete(loading_item)
            
            # Insertar items en lotes
            for i, item in enumerate(items):
                if i % 10 == 0:  # Actualizar UI cada 10 items
                    self.update_idletasks()
                
                tags = []
                if item['stock'] == 0:
                    tags.append('no_stock')
                elif item['stock'] < 10:
                    tags.append('low_stock')
                elif item['stock'] > 100:
                    tags.append('high_stock')
                
                self.tree_detailed.insert(
                    '', 'end',
                    text=item['name'],
                    values=(item['barcode'], item['stock'], item['obra'], 
                        item['n_factura'], self.app.session_state.current_warehouse['name']),
                    tags=tags + [str(item['id'])]
                )

            self.tree_detailed.tag_configure('no_stock', foreground='red', background='#ffeeee')
            self.tree_detailed.tag_configure('low_stock', foreground='orange', background='#fff7e6')
            self.tree_detailed.tag_configure('high_stock', foreground='green', background='#eeffee')    
            
            self.update_stats(items)
            
            if len(items) >= 100:
                self.stats_label.config(text=self.stats_label.cget("text") + " | Mostrando primeros 100 items")
                
        except Exception as e:
            self.tree_detailed.delete(*self.tree_detailed.get_children())
            self.tree_detailed.insert('', 'end', text=f'Error: {str(e)}', values=('', '', '', '', ''))

    
    def load_obra_summary(self):
        """Cargar resumen por obra"""
        # Limpiar vista por obra
        for item in self.tree_obra.get_children():
            self.tree_obra.delete(item)
        
        # Obtener items agrupados por obra
        warehouse_id = str(self.app.session_state.current_warehouse['id'])
        
        # Aplicar filtro de obra si existe
        selected_obra = self.obra_filter_var.get()
        if selected_obra and selected_obra != "Todas las obras":
            items_data = self.app.data_manager.get_items_by_obra(selected_obra, warehouse_id)
            # Extraer items de la respuesta
            all_items = items_data if isinstance(items_data, list) else items_data.get('items', [])
            obras_to_show = [selected_obra]
        else:
            items_data = self.app.data_manager.get_items_by_warehouse(warehouse_id)
            # Extraer items de la respuesta
            if isinstance(items_data, dict) and 'items' in items_data:
                all_items = items_data['items']
            else:
                all_items = items_data if isinstance(items_data, list) else []
            obras_to_show = list(set(item['obra'] for item in all_items))   
        
        # Agrupar por obra
        obras_summary = {}
        for item in all_items:
            obra = item['obra']
            if obra not in obras_summary:
                obras_summary[obra] = {
                    'total_items': 0,
                    'total_stock': 0,
                    'items': []
                }
            
            obras_summary[obra]['total_items'] += 1
            obras_summary[obra]['total_stock'] += item['stock']
            obras_summary[obra]['items'].append(item)
        
        # Agregar al árbol (ordenado por stock total)
        sorted_obras = sorted(obras_summary.items(), key=lambda x: x[1]['total_stock'], reverse=True)
        
        for obra, summary in sorted_obras:
            # Calcular valor estimado (usando precio base de $10 por unidad)
            estimated_value = summary['total_stock'] * 10
            
            # Determinar color según estado
            if summary['total_stock'] == 0:
                obra_tags = ['obra_empty']
            elif summary['total_stock'] < 50:
                obra_tags = ['obra_low']
            else:
                obra_tags = ['obra_normal']
            
            obra_node = self.tree_obra.insert(
                '',
                'end',
                text=f"🏗️ {obra}",
                values=(
                    summary['total_items'],
                    summary['total_stock'],
                    f"${estimated_value:,.2f}"
                ),
                tags=obra_tags
            )
            
            # Agregar items como hijos (ordenados por stock)
            sorted_items = sorted(summary['items'], key=lambda x: x['stock'], reverse=True)
            for item in sorted_items:
                item_value = item['stock'] * 10
                
                # Tags para items
                item_tags = ['item']
                if item['stock'] == 0:
                    item_tags.append('item_no_stock')
                elif item['stock'] < 10:
                    item_tags.append('item_low_stock')
                
                self.tree_obra.insert(
                    obra_node,
                    'end',
                    text=f"  📦 {item['name']}",
                    values=(
                        "",
                        item['stock'],
                        f"${item_value:,.2f}"
                    ),
                    tags=item_tags + [str(item['id'])]
                )
        
        # Configurar colores
        self.tree_obra.tag_configure('obra_empty', foreground='red', background='#ffeeee')
        self.tree_obra.tag_configure('obra_low', foreground='orange', background='#fff7e6')
        self.tree_obra.tag_configure('obra_normal', foreground='green', background='#eeffee')
        self.tree_obra.tag_configure('item_no_stock', foreground='red')
        self.tree_obra.tag_configure('item_low_stock', foreground='orange')
    
    def load_summary_view(self):
        """Cargar vista de resumen"""
        warehouse_id = str(self.app.session_state.current_warehouse['id'])
        all_items = self.app.data_manager.get_items_by_warehouse(warehouse_id)
        
        # Calcular métricas
        total_items = len(all_items)
        total_stock = sum(item['stock'] for item in all_items)
        obras_count = len(set(item['obra'] for item in all_items))
        no_stock_items = [item for item in all_items if item['stock'] == 0]
        low_stock_items = [item for item in all_items if 0 < item['stock'] < 10]
        
        # Actualizar métricas
        metrics_text = (
            f"📊 Total Items: {total_items} | "
            f"📦 Stock Total: {total_stock:,} | "
            f"🏗️ Obras: {obras_count} | "
            f"⚠️ Stock Bajo: {len(low_stock_items)} | "
            f"❌ Sin Stock: {len(no_stock_items)}"
        )
        self.metrics_text.config(text=metrics_text)
        
        # Limpiar y llenar alertas
        for item in self.tree_alerts.get_children():
            self.tree_alerts.delete(item)
        
        # Agregar items sin stock
        if no_stock_items:
            no_stock_node = self.tree_alerts.insert('', 'end', text='❌ SIN STOCK', values=('', '', ''))
            for item in no_stock_items:
                self.tree_alerts.insert(
                    no_stock_node,
                    'end',
                    text=item['name'],
                    values=(item['stock'], item['obra'], 'SIN STOCK'),
                    tags=['no_stock']
                )
        
        # Agregar items con stock bajo
        if low_stock_items:
            low_stock_node = self.tree_alerts.insert('', 'end', text='⚠️ STOCK BAJO', values=('', '', ''))
            for item in low_stock_items:
                self.tree_alerts.insert(
                    low_stock_node,
                    'end',
                    text=item['name'],
                    values=(item['stock'], item['obra'], 'STOCK BAJO'),
                    tags=['low_stock']
                )
        
        # Configurar colores
        self.tree_alerts.tag_configure('no_stock', foreground='red', background='#ffeeee')
        self.tree_alerts.tag_configure('low_stock', foreground='orange', background='#fff7e6')
        
        # Expandir nodos
        for child in self.tree_alerts.get_children():
            self.tree_alerts.item(child, open=True)
    
    def on_obra_double_click(self, event):
        """Manejar doble click en obra para expandir/contraer"""
        selected = self.tree_obra.selection()
        if not selected:
            return
        
        item = selected[0]
        if self.tree_obra.get_children(item):
            # Si tiene hijos, alternar entre expandido/contraído
            if self.tree_obra.item(item, "open"):
                self.tree_obra.item(item, open=False)
            else:
                self.tree_obra.item(item, open=True)
    
    def on_item_double_click(self, event):
        """Manejar doble click en item para mostrar detalles"""
        selected = self.tree_detailed.selection()
        if not selected:
            return
        
        item_data = self.tree_detailed.item(selected[0])
        item_name = item_data['text']
        item_values = item_data['values']
        
        # Mostrar ventana de detalles
        self.show_item_details(item_name, item_values, item_data['tags'])
    
    def show_item_details(self, name, values, tags):
        """Mostrar detalles del item"""
        dialog = tk.Toplevel(self)
        dialog.title(f"Detalles: {name}")
        dialog.geometry("400x300")
        dialog.transient(self)
        dialog.grab_set()
        
        main_frame = ttk.Frame(dialog, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        ttk.Label(
            main_frame,
            text=name,
            font=('Arial', 16, 'bold')
        ).pack(pady=(0, 20))
        
        # Detalles
        details = [
            ("Código de Barras", values[0]),
            ("Stock Actual", values[1]),
            ("Obra", values[2]),
            ("Número de Factura", values[3]),
            ("Ubicación", values[4])
        ]
        
        for label, value in details:
            detail_frame = ttk.Frame(main_frame)
            detail_frame.pack(fill=tk.X, pady=5)
            
            ttk.Label(
                detail_frame,
                text=f"{label}:",
                font=('Arial', 10, 'bold')
            ).pack(side=tk.LEFT)
            
            ttk.Label(
                detail_frame,
                text=str(value),
                font=('Arial', 10)
            ).pack(side=tk.RIGHT)
        
        # Estado del stock
        stock = int(values[1])
        if stock == 0:
            status = "❌ SIN STOCK"
            color = "red"
        elif stock < 10:
            status = "⚠️ STOCK BAJO"
            color = "orange"
        else:
            status = "✅ STOCK NORMAL"
            color = "green"
        
        ttk.Label(
            main_frame,
            text=f"Estado: {status}",
            font=('Arial', 12, 'bold'),
            foreground=color
        ).pack(pady=(20, 10))
        
        # Botón cerrar
        ttk.Button(
            main_frame,
            text="Cerrar",
            command=dialog.destroy
        ).pack(pady=10)
    
    def expand_all_obras(self):
        """Expandir todas las obras"""
        for child in self.tree_obra.get_children():
            self.tree_obra.item(child, open=True)
    
    def collapse_all_obras(self):
        """Contraer todas las obras"""
        for child in self.tree_obra.get_children():
            self.tree_obra.item(child, open=False)
    
    def show_advanced_search(self):
        """Mostrar búsqueda avanzada"""
        dialog = tk.Toplevel(self)
        dialog.title("Búsqueda Avanzada")
        dialog.geometry("500x400")
        dialog.transient(self)
        dialog.grab_set()
        
        main_frame = ttk.Frame(dialog, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(
            main_frame,
            text="Búsqueda Avanzada de Materiales",
            font=('Arial', 14, 'bold')
        ).pack(pady=(0, 20))
        
        # Filtros
        filters_frame = ttk.LabelFrame(main_frame, text="Filtros", padding=10)
        filters_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Nombre
        ttk.Label(filters_frame, text="Nombre contiene:").grid(row=0, column=0, sticky=tk.W, pady=5)
        name_var = tk.StringVar()
        ttk.Entry(filters_frame, textvariable=name_var, width=30).grid(row=0, column=1, pady=5, padx=(10, 0))
        
        # Obra
        ttk.Label(filters_frame, text="Obra:").grid(row=1, column=0, sticky=tk.W, pady=5)
        obra_var = tk.StringVar()
        obra_combo = ttk.Combobox(filters_frame, textvariable=obra_var, width=28, state='readonly')
        obras = ["Todas"] + self.app.data_manager.get_obras_by_warehouse(str(self.app.session_state.current_warehouse['id']))
        obra_combo['values'] = obras
        obra_combo.set("Todas")
        obra_combo.grid(row=1, column=1, pady=5, padx=(10, 0))
        
        # Stock mínimo
        ttk.Label(filters_frame, text="Stock mínimo:").grid(row=2, column=0, sticky=tk.W, pady=5)
        min_stock_var = tk.StringVar(value="0")
        ttk.Entry(filters_frame, textvariable=min_stock_var, width=30).grid(row=2, column=1, pady=5, padx=(10, 0))
        
        # Stock máximo
        ttk.Label(filters_frame, text="Stock máximo:").grid(row=3, column=0, sticky=tk.W, pady=5)
        max_stock_var = tk.StringVar(value="99999")
        ttk.Entry(filters_frame, textvariable=max_stock_var, width=30).grid(row=3, column=1, pady=5, padx=(10, 0))
       
        # Código de barras
        ttk.Label(filters_frame, text="Código contiene:").grid(row=4, column=0, sticky=tk.W, pady=5)
        barcode_var = tk.StringVar()
        ttk.Entry(filters_frame, textvariable=barcode_var, width=30).grid(row=4, column=1, pady=5, padx=(10, 0))
        
        # Resultados
        results_frame = ttk.LabelFrame(main_frame, text="Resultados", padding=10)
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        # Tabla de resultados
        results_tree = ttk.Treeview(
            results_frame,
            columns=('stock', 'obra', 'codigo'),
            show='tree headings',
            height=8
        )
        results_tree.pack(fill=tk.BOTH, expand=True)
        
        results_tree.heading('#0', text='Material')
        results_tree.heading('stock', text='Stock')
        results_tree.heading('obra', text='Obra')
        results_tree.heading('codigo', text='Código')
        
        def perform_search():
            # Limpiar resultados
            for item in results_tree.get_children():
                results_tree.delete(item)
            
            # Obtener todos los items
            warehouse_id = str(self.app.session_state.current_warehouse['id'])
            all_items = self.app.data_manager.get_items_by_warehouse(warehouse_id)
            
            # Aplicar filtros
            filtered_items = []
            for item in all_items:
                # Filtro por nombre
                if name_var.get() and name_var.get().lower() not in item['name'].lower():
                    continue
                
                # Filtro por obra
                if obra_var.get() != "Todas" and obra_var.get() != item['obra']:
                    continue
                
                # Filtro por código
                if barcode_var.get() and barcode_var.get().lower() not in item['barcode'].lower():
                    continue
                
                # Filtro por stock
                try:
                    min_stock = int(min_stock_var.get())
                    max_stock = int(max_stock_var.get())
                    if not (min_stock <= item['stock'] <= max_stock):
                        continue
                except ValueError:
                    pass
                
                filtered_items.append(item)
            
            # Mostrar resultados
            for item in filtered_items:
                results_tree.insert(
                    '',
                    'end',
                    text=item['name'],
                    values=(item['stock'], item['obra'], item['barcode'])
                )
            
            # Mostrar contador
            ttk.Label(
                results_frame,
                text=f"Encontrados: {len(filtered_items)} materiales"
            ).pack()
        
        # Botones
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(pady=10)
        
        ttk.Button(
            buttons_frame,
            text="🔍 Buscar",
            command=perform_search
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            buttons_frame,
            text="Aplicar Filtro",
            command=lambda: self.apply_advanced_filter(name_var.get(), obra_var.get(), dialog)
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            buttons_frame,
            text="Cerrar",
            command=dialog.destroy
        ).pack(side=tk.LEFT, padx=5)
    
    def apply_advanced_filter(self, name_filter, obra_filter, dialog):
        """Aplicar filtro avanzado a la vista principal"""
        if obra_filter and obra_filter != "Todas":
            self.obra_filter_combo.set(obra_filter)
        
        if name_filter:
            self.search_var.set(name_filter)
        
        dialog.destroy()
        self.load_items()
    
    def export_data(self):
        """Exportar datos a archivo"""
        try:
            import csv
            from tkinter import filedialog
            
            # Seleccionar archivo
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                title="Guardar inventario como..."
            )
            
            if filename:
                warehouse_id = str(self.app.session_state.current_warehouse['id'])
                items = self.app.data_manager.get_items_by_warehouse(warehouse_id)
                
                with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                    fieldnames = ['nombre', 'codigo_barras', 'stock', 'obra', 'factura', 'bodega']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    
                    writer.writeheader()
                    for item in items:
                        writer.writerow({
                            'nombre': item['name'],
                            'codigo_barras': item['barcode'],
                            'stock': item['stock'],
                            'obra': item['obra'],
                            'factura': item['n_factura'],
                            'bodega': self.app.session_state.current_warehouse['name']
                        })
                
                messagebox.showinfo("Éxito", f"Datos exportados a: {filename}")
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar datos: {str(e)}")
    
    def refresh_all_data(self):
        """Actualizar todos los datos"""
        self.load_obras_filter()
        self.load_items()
        if self.view_mode_var.get() == "por_obra":
            self.load_obra_summary()
        elif self.view_mode_var.get() == "resumen":
            self.load_summary_view()
        messagebox.showinfo("Actualizado", "Todos los datos han sido actualizados")
    
    def show_alerts_only(self):
        """Mostrar solo items con alertas"""
        # Cambiar a vista de resumen
        self.view_mode_var.set("resumen")
        self.notebook.select(2)
        self.load_summary_view()
        messagebox.showinfo("Alertas", "Mostrando vista de alertas de stock")
    
    def on_search_changed(self, *args):
        """Manejar cambio en búsqueda"""
        search_query = self.search_var.get()
        if len(search_query) >= 2:
            self.load_items(search_query)
        elif len(search_query) == 0:
            self.load_items()
    
    def update_stats(self, items):
        """Actualizar estadísticas"""
        total_items = len(items)
        total_stock = sum(item['stock'] for item in items)
        obras_count = len(set(item['obra'] for item in items))
        low_stock_items = len([item for item in items if 0 < item['stock'] < 10])
        no_stock_items = len([item for item in items if item['stock'] == 0])
        high_stock_items = len([item for item in items if item['stock'] > 100])
        
        warehouse_name = self.app.session_state.current_warehouse['name']
        
        stats_text = (
            f"🏭 {warehouse_name} | "
            f"📦 Items: {total_items} | "
            f"📊 Stock: {total_stock:,} | "
            f"🏗️ Obras: {obras_count} | "
            f"⚠️ Bajo: {low_stock_items} | "
            f"❌ Vacío: {no_stock_items} | "
            f"📈 Alto: {high_stock_items}"
        )
        
        self.stats_label.config(text=stats_text)
    
    def show_transfer_dialog(self):
        """Mostrar diálogo de transferencia entre obras"""
        dialog = tk.Toplevel(self)
        dialog.title("Transferir Material entre Obras")
        dialog.geometry("700x600")
        dialog.transient(self)
        dialog.grab_set()
        
        # Frame principal
        main_frame = ttk.Frame(dialog, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        ttk.Label(
            main_frame,
            text="🔄 Transferir Material entre Obras",
            font=('Arial', Config.FONT_SIZE_LARGE, 'bold')
        ).pack(pady=(0, 20))
        
        # Instrucciones
        instructions_frame = ttk.LabelFrame(main_frame, text="Instrucciones", padding=10)
        instructions_frame.pack(fill=tk.X, pady=(0, 10))
        
        instructions_text = (
            "1. Escanee el código de barras del material a transferir\n"
            "2. Seleccione la obra de destino\n"
            "3. Ingrese la cantidad a transferir\n"
            "4. Añada notas opcionales\n"
            "5. Confirme la transferencia"
        )
        
        ttk.Label(
            instructions_frame,
            text=instructions_text,
            font=('Arial', Config.FONT_SIZE_SMALL),
            justify=tk.LEFT
        ).pack(anchor=tk.W)
        
        # Seleccionar item
        item_frame = ttk.LabelFrame(main_frame, text="Seleccionar Material", padding=10)
        item_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Scanner de código de barras
        scanner_frame = ttk.Frame(item_frame)
        scanner_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(scanner_frame, text="Código de Barras:", font=('Arial', Config.FONT_SIZE_MEDIUM)).pack(side=tk.LEFT)
        
        self.transfer_barcode_var = tk.StringVar()
        barcode_entry = ttk.Entry(
            scanner_frame, 
            textvariable=self.transfer_barcode_var, 
            font=('Arial', Config.FONT_SIZE_MEDIUM), 
            width=25
        )
        barcode_entry.pack(side=tk.LEFT, padx=(10, 5))
        barcode_entry.bind('<Return>', lambda e: self.load_item_for_transfer(self.transfer_barcode_var.get(), dialog))
        
        ttk.Button(
            scanner_frame,
            text="🔍 Buscar",
            command=lambda: self.load_item_for_transfer(self.transfer_barcode_var.get(), dialog)
        ).pack(side=tk.LEFT)
        
        # Información del item seleccionado
        self.transfer_item_info = ttk.Label(
            item_frame,
            text="Escanee un código de barras para seleccionar el material",
            font=('Arial', Config.FONT_SIZE_MEDIUM),
            foreground='blue'
        )
        self.transfer_item_info.pack(pady=(10, 0))
        
        # Configuración de transferencia
        transfer_config_frame = ttk.LabelFrame(main_frame, text="Configuración de Transferencia", padding=10)
        transfer_config_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Obra origen (readonly)
        ttk.Label(transfer_config_frame, text="Obra Origen:", font=('Arial', Config.FONT_SIZE_MEDIUM)).grid(
            row=0, column=0, sticky=tk.W, pady=5, padx=(0, 10)
        )
        self.from_obra_var = tk.StringVar()
        from_obra_entry = ttk.Entry(
            transfer_config_frame, 
            textvariable=self.from_obra_var, 
            state='readonly', 
            font=('Arial', Config.FONT_SIZE_MEDIUM), 
            width=30
        )
        from_obra_entry.grid(row=0, column=1, pady=5, sticky=tk.W)
        
        # Obra destino
        ttk.Label(transfer_config_frame, text="Obra Destino:", font=('Arial', Config.FONT_SIZE_MEDIUM)).grid(
            row=1, column=0, sticky=tk.W, pady=5, padx=(0, 10)
        )
        self.to_obra_var = tk.StringVar()
        to_obra_combo = ttk.Combobox(
            transfer_config_frame, 
            textvariable=self.to_obra_var, 
            font=('Arial', Config.FONT_SIZE_MEDIUM), 
            width=28,
            state='readonly'
        )
        to_obra_combo.grid(row=1, column=1, pady=5, sticky=tk.W)
        
        # Cargar obras disponibles
        warehouse_id = str(self.app.session_state.current_warehouse['id'])
        obras = self.app.data_manager.get_obras_by_warehouse(warehouse_id)
        to_obra_combo['values'] = obras
        
        # Cantidad
        ttk.Label(transfer_config_frame, text="Cantidad:", font=('Arial', Config.FONT_SIZE_MEDIUM)).grid(
            row=2, column=0, sticky=tk.W, pady=5, padx=(0, 10)
        )
        self.transfer_quantity_var = tk.StringVar(value="1")
        quantity_spinbox = ttk.Spinbox(
            transfer_config_frame, 
            textvariable=self.transfer_quantity_var, 
            from_=1, 
            to=9999, 
            font=('Arial', Config.FONT_SIZE_MEDIUM), 
            width=15
        )
        quantity_spinbox.grid(row=2, column=1, pady=5, sticky=tk.W)
        
        # Notas
        ttk.Label(transfer_config_frame, text="Notas:", font=('Arial', Config.FONT_SIZE_MEDIUM)).grid(
            row=3, column=0, sticky=tk.W, pady=5, padx=(0, 10)
        )
        self.transfer_notes_var = tk.StringVar()
        notes_entry = ttk.Entry(
            transfer_config_frame, 
            textvariable=self.transfer_notes_var, 
            font=('Arial', Config.FONT_SIZE_MEDIUM), 
            width=30
        )
        notes_entry.grid(row=3, column=1, pady=5, sticky=tk.W)
        
        # Vista previa de la transferencia
        preview_frame = ttk.LabelFrame(main_frame, text="Vista Previa de la Transferencia", padding=10)
        preview_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.transfer_preview = tk.Text(
            preview_frame,
            height=6,
            width=60,
            wrap=tk.WORD,
            state=tk.DISABLED,
            font=('Arial', Config.FONT_SIZE_SMALL)
        )
        self.transfer_preview.pack(fill=tk.BOTH, expand=True)
        
        # Mensaje de error
        self.transfer_error_label = ttk.Label(main_frame, text="", foreground='red')
        self.transfer_error_label.pack(pady=5)
        
        # Botones
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=10)
        
        ttk.Button(
            button_frame,
            text="❌ Cancelar",
            command=dialog.destroy,
            style='Secondary.TButton'
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text="👁️ Vista Previa",
            command=self.update_transfer_preview,
            style='Info.TButton'
        ).pack(side=tk.LEFT, padx=5)
        
        self.execute_transfer_button = ttk.Button(
            button_frame,
            text="✅ Confirmar Transferencia",
            command=lambda: self.execute_transfer(dialog),
            style='Primary.TButton',
            state=tk.DISABLED
        )
        self.execute_transfer_button.pack(side=tk.LEFT, padx=5)
        
        # Variables del diálogo
        self.transfer_dialog_item = None
        
        # Focus en el scanner
        barcode_entry.focus()
    
    def load_item_for_transfer(self, barcode, dialog):
        """Cargar item para transferencia"""
        if not barcode.strip():
            self.transfer_error_label.config(text="Ingrese un código de barras")
            return
        
        item = self.app.data_manager.get_item_by_barcode(barcode.strip())
        if item:
            # Verificar que pertenece a la bodega actual
            if str(item['warehouse_id']) == str(self.app.session_state.current_warehouse['id']):
                self.transfer_dialog_item = item
                self.from_obra_var.set(item['obra'])
                
                info_text = (
                    f"✅ Material encontrado:\n"
                    f"📦 Nombre: {item['name']}\n"
                    f"📊 Stock disponible: {item['stock']} unidades\n"
                    f"🏗️ Obra actual: {item['obra']}\n"
                    f"🔢 Código: {item['barcode']}"
                )
                
                self.transfer_item_info.config(text=info_text, foreground='green')
                self.transfer_error_label.config(text="")
                self.execute_transfer_button.config(state=tk.NORMAL)
                
                # Actualizar rango del spinbox
                try:
                    quantity_spinbox = None
                    for widget in dialog.winfo_children():
                        if isinstance(widget, ttk.Frame):
                            for child in widget.winfo_children():
                                if isinstance(child, ttk.LabelFrame) and "Configuración" in str(child):
                                    for grandchild in child.winfo_children():
                                        if isinstance(grandchild, ttk.Spinbox):
                                            grandchild.config(to=item['stock'])
                                            break
                except:
                    pass
                
                self.update_transfer_preview()
            else:
                self.transfer_error_label.config(text="❌ El material no pertenece a esta bodega")
                self.reset_transfer_form()
        else:
            self.transfer_error_label.config(text=f"❌ No se encontró material con código: {barcode}")
            self.reset_transfer_form()
    
    def reset_transfer_form(self):
        """Resetear formulario de transferencia"""
        self.transfer_dialog_item = None
        self.from_obra_var.set("")
        self.to_obra_var.set("")
        self.transfer_quantity_var.set("1")
        self.transfer_notes_var.set("")
        self.execute_transfer_button.config(state=tk.DISABLED)
        self.transfer_item_info.config(
            text="Escanee un código de barras para seleccionar el material",
            foreground='blue'
        )
        self.transfer_preview.config(state=tk.NORMAL)
        self.transfer_preview.delete(1.0, tk.END)
        self.transfer_preview.config(state=tk.DISABLED)
    
    def update_transfer_preview(self):
        """Actualizar vista previa de transferencia"""
        if not self.transfer_dialog_item:
            return
        
        try:
            quantity = int(self.transfer_quantity_var.get())
            to_obra = self.to_obra_var.get()
            notes = self.transfer_notes_var.get()
            
            preview_text = f"""
    📋 RESUMEN DE TRANSFERENCIA

    📦 Material: {self.transfer_dialog_item['name']}
    🔢 Código: {self.transfer_dialog_item['barcode']}

    📊 CANTIDADES:
    • Stock actual: {self.transfer_dialog_item['stock']} unidades
    • Cantidad a transferir: {quantity} unidades
    • Stock restante: {self.transfer_dialog_item['stock'] - quantity} unidades

    🏗️ OBRAS:
    • Origen: {self.from_obra_var.get()}
    • Destino: {to_obra if to_obra else '(Seleccionar obra)'}

    📝 Notas: {notes if notes else 'Sin notas'}

    ⚠️ IMPORTANTE: Esta transferencia no se puede deshacer.
            """.strip()
            
            self.transfer_preview.config(state=tk.NORMAL)
            self.transfer_preview.delete(1.0, tk.END)
            self.transfer_preview.insert(1.0, preview_text)
            self.transfer_preview.config(state=tk.DISABLED)
            
        except ValueError:
            pass
    
    def execute_transfer(self, dialog):
        """Ejecutar transferencia"""
        if not self.transfer_dialog_item:
            self.transfer_error_label.config(text="❌ Debe seleccionar un material primero")
            return
        
        to_obra = self.to_obra_var.get().strip()
        if not to_obra:
            self.transfer_error_label.config(text="❌ Debe seleccionar una obra de destino")
            return
        
        if to_obra == self.from_obra_var.get():
            self.transfer_error_label.config(text="❌ La obra de destino debe ser diferente a la de origen")
            return
        
        try:
            quantity = int(self.transfer_quantity_var.get())
            if quantity <= 0:
                self.transfer_error_label.config(text="❌ La cantidad debe ser mayor a 0")
                return
            
            if quantity > self.transfer_dialog_item['stock']:
                self.transfer_error_label.config(text="❌ Cantidad excede el stock disponible")
                return
        except ValueError:
            self.transfer_error_label.config(text="❌ Ingrese una cantidad válida")
            return
        
        # Confirmar transferencia
        if messagebox.askyesno(
            "Confirmar Transferencia",
            f"¿Está seguro de transferir {quantity} unidades de '{self.transfer_dialog_item['name']}'?\n\n"
            f"De: {self.from_obra_var.get()}\n"
            f"A: {to_obra}\n\n"
            f"Esta acción NO se puede deshacer."
        ):
            # Ejecutar transferencia
            success = self.app.data_manager.transfer_item_between_obras(
                str(self.transfer_dialog_item['id']),
                self.from_obra_var.get(),
                to_obra,
                quantity,
                self.transfer_notes_var.get()
            )
            
            if success:
                # Actualizar vistas
                self.load_items()
                self.load_obra_summary()
                dialog.destroy()
                messagebox.showinfo(
                    "✅ Transferencia Exitosa", 
                    f"Se transfirieron {quantity} unidades de '{self.transfer_dialog_item['name']}' "
                    f"de {self.from_obra_var.get()} a {to_obra}"
                )
            else:
                self.transfer_error_label.config(text="❌ Error al realizar la transferencia")
    
    # Mantener todos los métodos existentes como show_add_stock_dialog, show_add_item_dialog, etc.
    # (Los métodos que ya existen en el código original se mantienen sin cambios)
   
    def show_add_stock_dialog(self):
        """Mantener método existente"""
        # El código existente del método se mantiene igual
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
    
    def show_add_item_dialog(self):
        """Mantener método existente"""
        # El código existente del método se mantiene igual
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
    
    # Métodos de soporte para agregar stock (mantener los existentes)
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

    def open_transfer_dialog(self):
        """Abrir diálogo de transferencia simple"""
        dialog = tk.Toplevel(self)
        dialog.title("Transferir Material")
        dialog.geometry("500x400")
        dialog.transient(self)
        dialog.grab_set()
    
        main_frame = ttk.Frame(dialog, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
    
        ttk.Label(main_frame, text="Transferir Material entre Obras", 
                font=('Arial', 16, 'bold')).pack(pady=(0, 20))
    
        # Código de barras
        ttk.Label(main_frame, text="Código de barras:").pack(anchor=tk.W)
        barcode_var = tk.StringVar()
        barcode_entry = ttk.Entry(main_frame, textvariable=barcode_var, width=40)
        barcode_entry.pack(fill=tk.X, pady=(5, 15))
    
        # Item info
        item_info = ttk.Label(main_frame, text="Escanee un código de barras")
        item_info.pack(pady=(0, 15))
    
        # Obra destino
        ttk.Label(main_frame, text="Obra destino:").pack(anchor=tk.W)
        obra_var = tk.StringVar()
        obra_combo = ttk.Combobox(main_frame, textvariable=obra_var, state='readonly', width=38)
    
        # Cargar obras
        warehouse_id = str(self.app.session_state.current_warehouse['id'])
        obras = self.app.data_manager.get_obras_by_warehouse(warehouse_id)
        obra_combo['values'] = obras
        obra_combo.pack(fill=tk.X, pady=(5, 15))
    
        # Cantidad
        ttk.Label(main_frame, text="Cantidad:").pack(anchor=tk.W)
        quantity_var = tk.StringVar(value="1")
        quantity_entry = ttk.Entry(main_frame, textvariable=quantity_var, width=40)
        quantity_entry.pack(fill=tk.X, pady=(5, 15))
    
        # Variables globales del diálogo
        current_item = [None]  # Usar lista para poder modificar desde funciones internas
    
        def buscar_item():
            barcode = barcode_var.get().strip()
            if not barcode:
                return
            
            item = self.app.data_manager.get_item_by_barcode(barcode)
            if item and str(item['warehouse_id']) == warehouse_id:
                current_item[0] = item
                item_info.config(text=f"Material: {item['name']} | Stock: {item['stock']} | Obra: {item['obra']}")
            else:
                item_info.config(text="Material no encontrado en esta bodega")
                current_item[0] = None
    
        def transferir():
            if not current_item[0]:
                messagebox.showerror("Error", "Debe seleccionar un material primero")
                return
            
            if not obra_var.get():
                messagebox.showerror("Error", "Debe seleccionar una obra destino")
                return
            
            try:
                qty = int(quantity_var.get())
                if qty <= 0 or qty > current_item[0]['stock']:
                    messagebox.showerror("Error", "Cantidad inválida")
                    return
            except ValueError:
                messagebox.showerror("Error", "Ingrese una cantidad válida")
                return
        
            if obra_var.get() == current_item[0]['obra']:
                messagebox.showerror("Error", "La obra destino debe ser diferente")
                return
            
            # Realizar transferencia
            success = self.app.data_manager.transfer_item_between_obras(
                str(current_item[0]['id']),
                current_item[0]['obra'],
                obra_var.get(),
                qty,
                "Transferencia desde interfaz"
            )
        
            if success:
                messagebox.showinfo("Éxito", "Transferencia realizada")
                self.load_items()  # Actualizar lista
                dialog.destroy()
            else:
                messagebox.showerror("Error", "No se pudo realizar la transferencia")
    
        # Botones
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=20)
    
        ttk.Button(btn_frame, text="Buscar", command=buscar_item).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Transferir", command=transferir).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancelar", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
    
        barcode_entry.focus()
        barcode_entry.bind('<Return>', lambda e: buscar_item())

    def load_items_optimized(self, search_query=None):
        """Versión optimizada de load_items"""
        # Mostrar indicador de carga
        self.stats_label.config(text="Cargando...")
        self.update()
    
        # Limpiar vista detallada
        for item in self.tree_detailed.get_children():
            self.tree_detailed.delete(item)
    
        # Obtener filtro de obra
        selected_obra = self.obra_filter_var.get()
        if selected_obra == "Todas las obras":
            selected_obra = None
    
        # Obtener items
        warehouse_id = str(self.app.session_state.current_warehouse['id'])
    
        try:
            if search_query:
                items = self.app.data_manager.search_items(search_query, warehouse_id)
                if selected_obra:
                    items = [item for item in items if item['obra'] == selected_obra]
            else:
                if selected_obra:
                        items = self.app.data_manager.get_items_by_obra(selected_obra, warehouse_id)
                else:
                    items = self.app.data_manager.get_items_by_warehouse(warehouse_id)
        
            # Limitar items mostrados para mejor rendimiento
            if len(items) > 500:
                items = items[:500]
                messagebox.showinfo("Información", f"Mostrando primeros 500 items de {len(items)} encontrados")
        
            # Agregar items al árbol en lotes
            for i, item in enumerate(items):
                if i % 50 == 0:  # Actualizar UI cada 50 items
                    self.update()
            
                tags = []
                if item['stock'] == 0:
                    tags.append('no_stock')
                elif item['stock'] < 10:
                    tags.append('low_stock')
                elif item['stock'] > 100:
                    tags.append('high_stock')
            
                self.tree_detailed.insert(
                    '',
                    'end',
                    text=item['name'],
                    values=(
                        item['barcode'],
                        item['stock'],
                        item['obra'],
                        item['n_factura'],
                        self.app.session_state.current_warehouse['name']
                    ),
                    tags=tags + [str(item['id'])]
                )
        
            # Configurar tags
            self.tree_detailed.tag_configure('no_stock', foreground='red')
            self.tree_detailed.tag_configure('low_stock', foreground='orange')
            self.tree_detailed.tag_configure('high_stock', foreground='green')
        
            self.update_stats(items)
        
        except Exception as e:
            messagebox.showerror("Error", f"Error cargando items: {str(e)}")
            self.stats_label.config(text="Error al cargar datos")



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
            command=self.volver_home,
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

    def volver_home(self):
        print("DEBUG: Intentando volver...")
        try:
            if hasattr(self.app, 'show_home_page'):
                print("DEBUG: Método show_home_page encontrado")
                self.app.show_home_page()
            else:
                print("DEBUG: Método show_home_page NO encontrado")
                # Alternativa: destruir la ventana actual
                self.destroy()
        except Exception as e:
            print(f"DEBUG: Error al volver: {e}")

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

        email_button = ttk.Button(
            header_frame,
            text="✉︎ Enviar Reporte",
            command=self.show_email_dialog,
            style='Primary.TButton'
        )
        email_button.pack(side=tk.RIGHT)
        
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
    
    def show_email_dialog(self):
        """Mostrar diálogo para enviar email con validación"""
        dialog = tk.Toplevel(self)
        dialog.title("Enviar Reporte por Email")
        dialog.geometry("600x450")  # Un poco más grande para mensajes
        dialog.transient(self)
        dialog.grab_set()

        
        # Frame principal
        main_frame = ttk.Frame(dialog, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        ttk.Label(
            main_frame,
            text="Enviar Reporte de Historial",
            font=('Arial', Config.FONT_SIZE_LARGE, 'bold')
        ).pack(pady=(0, 20))
        
        # Campo de email
        email_frame = ttk.Frame(main_frame)
        email_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(
            email_frame,
            text="Email destino:",
            font=('Arial', Config.FONT_SIZE_MEDIUM)
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.email_var = tk.StringVar()
        email_entry = ttk.Entry(
            email_frame,
            textvariable=self.email_var,
            font=('Arial', Config.FONT_SIZE_MEDIUM),
            width=30
        )
        email_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Botón para validar email
        validate_button = ttk.Button(
            email_frame,
            text="Validar",
            command=self.validate_email_input,
            style='Secondary.TButton',
            width=10
        )
        validate_button.pack(side=tk.RIGHT, padx=(10, 0))
        
        # Mensaje de validación
        self.validation_label = ttk.Label(
            main_frame,
            text="Ingrese un email y presione Validar",
            font=('Arial', Config.FONT_SIZE_SMALL),
            foreground='blue'
        )
        self.validation_label.pack(pady=5)
        
        # Campo de asunto
        subject_frame = ttk.Frame(main_frame)
        subject_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(
            subject_frame,
            text="Asunto:",
            font=('Arial', Config.FONT_SIZE_MEDIUM)
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.subject_var = tk.StringVar(value="Historial de acciones de bodega")
        subject_entry = ttk.Entry(
            subject_frame,
            textvariable=self.subject_var,
            font=('Arial', Config.FONT_SIZE_MEDIUM),
            width=30
        )
        subject_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Mensaje de estado
        self.dialog_status_label = ttk.Label(
            main_frame,
            text="",
            font=('Arial', Config.FONT_SIZE_SMALL),
            foreground='blue'
        )
        self.dialog_status_label.pack(pady=10)
        
        # Botones
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)
        
        ttk.Button(
            button_frame,
            text="Cancelar",
            command=dialog.destroy,
            style='Secondary.TButton'
        ).pack(side=tk.LEFT, padx=10)
        
        self.send_button = ttk.Button(
            button_frame,
            text="Enviar Reporte",
            command=lambda: self.send_email_report(dialog),
            style='Primary.TButton',
            state=tk.DISABLED  # Inicialmente deshabilitado
        )
        self.send_button.pack(side=tk.LEFT, padx=10)
        
        # Bind eventos para validación en tiempo real
        email_entry.bind('<KeyRelease>', lambda e: self.on_email_changed())
        email_entry.bind('<Return>', lambda e: self.validate_email_input())
        
        # Focus en el campo de email
        email_entry.focus()
    
    def on_email_changed(self):
        """Cuando el email cambia, resetear validación"""
        self.validation_label.config(text="Presione Validar para verificar el email", foreground='blue')
        self.send_button.config(state=tk.DISABLED)
    
    def validate_email_input(self):
        """Validar el email ingresado"""
        email = self.email_var.get().strip()
        
        if not email:
            self.validation_label.config(text="Ingrese un email para validar", foreground='red')
            return
        
        # Validar el email
        is_valid, message = self.app.data_manager.validate_email_format(email)
        
        if is_valid:
            self.validation_label.config(text=f"✅ {message}", foreground='green')
            self.send_button.config(state=tk.NORMAL)
        else:
            self.validation_label.config(text=f"❌ {message}", foreground='red')
            self.send_button.config(state=tk.DISABLED)
    
    def send_email_report(self, dialog):
        """Enviar reporte por email a través del backend - filtrado por bodega actual"""
        email = self.email_var.get().strip()
        subject = self.subject_var.get().strip()
        
        if not email:
            self.dialog_status_label.config(text="Por favor ingrese un email válido", foreground='red')
            return
        
        # Deshabilitar botones durante el envío
        for widget in dialog.winfo_children():
            if isinstance(widget, ttk.Button):
                widget.config(state=tk.DISABLED)
        
        self.dialog_status_label.config(text="Enviando reporte...", foreground='blue')
        
        # Get current warehouse ID for filtering
        current_warehouse = self.app.session_state.current_warehouse
        warehouse_id = str(current_warehouse['id']) if current_warehouse else None
        warehouse_name = current_warehouse['name'] if current_warehouse else "Desconocida"
        
        # Usar el data_manager existente para llamar al backend con filtro de bodega
        result = self.app.data_manager.send_history_report_email(
            receiver_email=email,
            subject=subject,
            warehouse_name=warehouse_name,
            warehouse_id=warehouse_id  # Pass warehouse ID for filtering
        )
        
        if result.get('success'):
            records_count = result.get('records_count', 0)
            self.dialog_status_label.config(
                text=f"✅ Reporte enviado exitosamente ({records_count} registros)", 
                foreground='green'
            )
            self.status_label.config(
                text=f"Reporte de {warehouse_name} enviado a {email} ({records_count} registros)", 
                foreground='green'
            )
            # Cerrar diálogo después de 2 segundos
            self.after(2000, dialog.destroy)
        else:
            error_msg = result.get('message', 'Error desconocido')
            self.dialog_status_label.config(text=f"❌ Error: {error_msg}", foreground='red')
            # Rehabilitar botones
            for widget in dialog.winfo_children():
                if isinstance(widget, ttk.Button):
                    widget.config(state=tk.NORMAL)



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
            foreground='black',
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
            foreground='black',
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
            foreground='black',
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
            foreground='black',
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
        notebook = ttk.Notebook(self.main_frame)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        inventory_frame = ttk.Frame(notebook)
        notebook.add(inventory_frame, text="📦 Inventario")
        stats_frame = ttk.Frame(notebook)
        notebook.add(stats_frame, text="📊 Estadísticas")
        comparison_frame = ttk.Frame(notebook)
        notebook.add(comparison_frame, text="🔍 Comparar Obras")
        transfer_frame = ttk.Frame(notebook)
        notebook.add(transfer_frame, text="🔄 Transferencia Rápida")
        self.current_page = InventoryPage(inventory_frame, self)
        warehouse_id = str(self.session_state.current_warehouse['id'])
        try:
            from frontend.widgets import StatsWidget, ObraComparisonWidget, MaterialTransferWidget
        
            stats_widget = StatsWidget(stats_frame, self.data_manager, warehouse_id)
            stats_widget.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
            comparison_widget = ObraComparisonWidget(comparison_frame, self.data_manager, warehouse_id)
            comparison_widget.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
            transfer_widget = MaterialTransferWidget(transfer_frame, self.data_manager, warehouse_id)
            transfer_widget.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        except ImportError as e:
            # Si no se puede importar widgets, mostrar mensaje en cada frame
            for frame in [stats_frame, comparison_frame, transfer_frame]:
                error_frame = ttk.Frame(frame)
                error_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
                ttk.Label(
                    error_frame,
                    text="Error al cargar widgets avanzados.\nInstale matplotlib para funcionalidades completas.",
                    font=('Arial', 12),
                    justify=tk.CENTER
                ).pack(expand=True)
    
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
    