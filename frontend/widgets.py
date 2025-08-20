import tkinter as tk
from tkinter import ttk

class StatsWidget(ttk.Frame):
    def __init__(self, parent, data_manager, warehouse_id):
        super().__init__(parent)
        self.data_manager = data_manager
        self.warehouse_id = warehouse_id
        
        # Frame para estadísticas textuales
        text_stats_frame = ttk.LabelFrame(self, text="Resumen General", padding=10)
        text_stats_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.stats_text = ttk.Label(
            text_stats_frame,
            text="Cargando estadísticas...",
            font=('Arial', 12)
        )
        self.stats_text.pack()
        
        # Frame para estadísticas detalladas
        detailed_stats_frame = ttk.LabelFrame(self, text="Estadísticas Detalladas", padding=10)
        detailed_stats_frame.pack(fill=tk.BOTH, expand=True)
        
        # Crear tabla de estadísticas
        self.stats_tree = ttk.Treeview(
            detailed_stats_frame,
            columns=('value',),
            show='tree headings',
            height=15
        )
        self.stats_tree.pack(fill=tk.BOTH, expand=True)
        
        # Configurar columnas
        self.stats_tree.heading('#0', text='Métrica')
        self.stats_tree.heading('value', text='Valor')
        
        self.stats_tree.column('#0', width=300)
        self.stats_tree.column('value', width=150)
        
        # Cargar datos
        self.update_stats()
    
    def update_stats(self):
        """Actualizar estadísticas"""
        stats = self.data_manager.get_warehouse_statistics(self.warehouse_id)
        
        # Actualizar texto resumen
        stats_text = (
            f"Total Items: {stats['total_items']} | "
            f"Stock Total: {stats['total_stock']} | "
            f"Obras Activas: {stats['obras_count']} | "
            f"Stock Bajo: {stats['low_stock_items']} | "
            f"Sin Stock: {stats['no_stock_items']}"
        )
        self.stats_text.config(text=stats_text)
        
        # Limpiar tabla
        for item in self.stats_tree.get_children():
            self.stats_tree.delete(item)
        
        # Añadir estadísticas generales
        general_node = self.stats_tree.insert('', 'end', text='📊 Estadísticas Generales', values=('',))
        self.stats_tree.insert(general_node, 'end', text='Total de Items', values=(stats['total_items'],))
        self.stats_tree.insert(general_node, 'end', text='Stock Total', values=(stats['total_stock'],))
        self.stats_tree.insert(general_node, 'end', text='Obras Activas', values=(stats['obras_count'],))
        
        # Añadir alertas de stock
        alerts_node = self.stats_tree.insert('', 'end', text='⚠️ Alertas de Stock', values=('',))
        self.stats_tree.insert(alerts_node, 'end', text='Items sin Stock', values=(stats['no_stock_items'],))
        self.stats_tree.insert(alerts_node, 'end', text='Items con Stock Bajo', values=(stats['low_stock_items'],))
        
        # Añadir top obras
        if stats['top_obras']:
            obras_node = self.stats_tree.insert('', 'end', text='🏗️ Top Obras por Stock', values=('',))
            for i, (obra, data) in enumerate(stats['top_obras'], 1):
                obra_text = f"{i}. {obra}"
                stock_text = f"{data['stock']} items ({data['items']} tipos)"
                self.stats_tree.insert(obras_node, 'end', text=obra_text, values=(stock_text,))

class ObraComparisonWidget(ttk.Frame):
    def __init__(self, parent, data_manager, warehouse_id):
        super().__init__(parent)
        self.data_manager = data_manager
        self.warehouse_id = warehouse_id
        
        # Selector de obras para comparar
        selector_frame = ttk.Frame(self)
        selector_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(selector_frame, text="Comparar Obras:", font=('Arial', 12, 'bold')).pack(side=tk.LEFT)
        
        # Obra 1
        self.obra1_var = tk.StringVar()
        self.obra1_combo = ttk.Combobox(selector_frame, textvariable=self.obra1_var, width=25, state='readonly')
        self.obra1_combo.pack(side=tk.LEFT, padx=(10, 5))
        
        ttk.Label(selector_frame, text="vs", font=('Arial', 12, 'bold')).pack(side=tk.LEFT, padx=5)
        
        # Obra 2
        self.obra2_var = tk.StringVar()
        self.obra2_combo = ttk.Combobox(selector_frame, textvariable=self.obra2_var, width=25, state='readonly')
        self.obra2_combo.pack(side=tk.LEFT, padx=(5, 10))
        
        # Botón comparar
        compare_button = ttk.Button(
            selector_frame,
            text="🔍 Comparar",
            command=self.compare_obras
        )
        compare_button.pack(side=tk.LEFT)
        
        # Botón limpiar
        clear_button = ttk.Button(
            selector_frame,
            text="🧹 Limpiar",
            command=self.clear_comparison
        )
        clear_button.pack(side=tk.LEFT, padx=(5, 0))
        
        # Frame para resultados
        self.results_frame = ttk.LabelFrame(self, text="Comparación de Obras", padding=10)
        self.results_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.results_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Tabla de comparación
        self.comparison_tree = ttk.Treeview(
            self.results_frame,
            columns=('obra1', 'obra2', 'diferencia'),
            show='tree headings',
            height=15,
            yscrollcommand=scrollbar.set
        )
        self.comparison_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.comparison_tree.yview)
        
        # Configurar columnas
        self.comparison_tree.heading('#0', text='Métrica')
        self.comparison_tree.heading('obra1', text='Obra 1')
        self.comparison_tree.heading('obra2', text='Obra 2')
        self.comparison_tree.heading('diferencia', text='Diferencia')
        
        self.comparison_tree.column('#0', width=200)
        self.comparison_tree.column('obra1', width=150)
        self.comparison_tree.column('obra2', width=150)
        self.comparison_tree.column('diferencia', width=150)
        
        # Cargar obras disponibles
        self.load_obras()
    
    def load_obras(self):
        """Cargar obras disponibles"""
        obras = self.data_manager.get_obras_by_warehouse(self.warehouse_id)
        self.obra1_combo['values'] = obras
        self.obra2_combo['values'] = obras
    
    def clear_comparison(self):
        """Limpiar comparación"""
        self.obra1_combo.set('')
        self.obra2_combo.set('')
        
        # Limpiar tabla
        for item in self.comparison_tree.get_children():
            self.comparison_tree.delete(item)
        
        self.results_frame.config(text="Comparación de Obras")
    
    def compare_obras(self):
        """Comparar dos obras seleccionadas"""
        obra1 = self.obra1_var.get()
        obra2 = self.obra2_var.get()
        
        if not obra1 or not obra2:
            tk.messagebox.showwarning("Advertencia", "Debe seleccionar ambas obras para comparar")
            return
        
        if obra1 == obra2:
            tk.messagebox.showwarning("Advertencia", "Debe seleccionar obras diferentes")
            return
        
        # Obtener datos de ambas obras
        items1 = self.data_manager.get_items_by_obra(obra1, self.warehouse_id)
        items2 = self.data_manager.get_items_by_obra(obra2, self.warehouse_id)
        
        # Calcular métricas
        metrics1 = self.calculate_metrics(items1)
        metrics2 = self.calculate_metrics(items2)
        
        # Limpiar tabla
        for item in self.comparison_tree.get_children():
            self.comparison_tree.delete(item)
        
        # Añadir comparaciones generales
        general_node = self.comparison_tree.insert('', 'end', text='📊 Métricas Generales', values=('', '', ''))
        
        comparisons = [
            ('Total Items', metrics1['total_items'], metrics2['total_items']),
            ('Stock Total', metrics1['total_stock'], metrics2['total_stock']),
            ('Stock Promedio', metrics1['avg_stock'], metrics2['avg_stock']),
        ]
        
        for metric, val1, val2 in comparisons:
            if isinstance(val1, float):
                diff = val1 - val2
                diff_str = f"{diff:+.2f}"
                val1_str = f"{val1:.2f}"
                val2_str = f"{val2:.2f}"
                
                # Color para diferencia
                if diff > 0:
                    diff_str = f"+{diff:.2f} ✓"
                elif diff < 0:
                    diff_str = f"{diff:.2f} ✗"
                else:
                    diff_str = "0.00 ="
            else:
                diff = val1 - val2
                diff_str = f"{diff:+d}" if diff != 0 else "0"
                val1_str = str(val1)
                val2_str = str(val2)
                
                if diff > 0:
                    diff_str += " ✓"
                elif diff < 0:
                    diff_str += " ✗"
                else:
                    diff_str += " ="
            
            self.comparison_tree.insert(general_node, 'end', text=f"  {metric}", 
                                      values=(val1_str, val2_str, diff_str))
        
        # Añadir alertas de stock
        alerts_node = self.comparison_tree.insert('', 'end', text='⚠️ Alertas de Stock', values=('', '', ''))
        
        alert_comparisons = [
            ('Items sin Stock', metrics1['no_stock'], metrics2['no_stock']),
            ('Items Stock Bajo', metrics1['low_stock'], metrics2['low_stock'])
        ]
        
        for metric, val1, val2 in alert_comparisons:
            diff = val1 - val2
            diff_str = f"{diff:+d}" if diff != 0 else "0"
            
            if diff > 0:
                diff_str += " ⚠️"  # Más alertas es malo
            elif diff < 0:
                diff_str += " ✓"   # Menos alertas es bueno
            else:
                diff_str += " ="
            
            self.comparison_tree.insert(alerts_node, 'end', text=f"  {metric}", 
                                      values=(str(val1), str(val2), diff_str))
        
        # Añadir análisis de materiales comunes
        common_materials = self.get_common_materials(items1, items2)
        if common_materials:
            materials_node = self.comparison_tree.insert('', 'end', text='🔧 Materiales Comunes', values=('', '', ''))
            
            for material_name, stock1, stock2 in common_materials[:10]:  # Top 10
                diff = stock1 - stock2
                diff_str = f"{diff:+d}" if diff != 0 else "0"
                
                if diff > 0:
                    diff_str += " ✓"
                elif diff < 0:
                    diff_str += " ✗"
                else:
                    diff_str += " ="
                
                material_text = material_name[:30] + "..." if len(material_name) > 30 else material_name
                self.comparison_tree.insert(materials_node, 'end', text=f"  {material_text}", 
                                          values=(str(stock1), str(stock2), diff_str))
        
        # Actualizar título
        self.results_frame.config(text=f"Comparación: {obra1} vs {obra2}")
        
        # Expandir nodos por defecto
        self.comparison_tree.item(general_node, open=True)
        self.comparison_tree.item(alerts_node, open=True)
    
    def get_common_materials(self, items1, items2):
        """Obtener materiales comunes entre dos obras"""
        # Crear diccionarios por nombre de material
        materials1 = {item['name']: item['stock'] for item in items1}
        materials2 = {item['name']: item['stock'] for item in items2}
        
        # Encontrar materiales comunes
        common_names = set(materials1.keys()) & set(materials2.keys())
        
        common_materials = []
        for name in common_names:
            common_materials.append((name, materials1[name], materials2[name]))
        
        # Ordenar por diferencia de stock (mayor diferencia primero)
        common_materials.sort(key=lambda x: abs(x[1] - x[2]), reverse=True)
        
        return common_materials
    
    def calculate_metrics(self, items):
        """Calcular métricas de una obra"""
        if not items:
            return {
                'total_items': 0,
                'total_stock': 0,
                'avg_stock': 0.0,
                'no_stock': 0,
                'low_stock': 0
            }
        
        total_items = len(items)
        total_stock = sum(item['stock'] for item in items)
        avg_stock = total_stock / total_items if total_items > 0 else 0
        no_stock = len([item for item in items if item['stock'] == 0])
        low_stock = len([item for item in items if 0 < item['stock'] < 10])
        
        return {
            'total_items': total_items,
            'total_stock': total_stock,
            'avg_stock': avg_stock,
            'no_stock': no_stock,
            'low_stock': low_stock
        }

class MaterialTransferWidget(ttk.Frame):
    def __init__(self, parent, data_manager, warehouse_id):
        super().__init__(parent)
        self.data_manager = data_manager
        self.warehouse_id = warehouse_id
        
        # Frame de instrucciones
        instructions_frame = ttk.LabelFrame(self, text="Instrucciones", padding=10)
        instructions_frame.pack(fill=tk.X, pady=(0, 10))
        
        instructions_text = (
            "1. Escanee el código de barras del material a transferir\n"
            "2. Seleccione la obra de destino\n"
            "3. Ingrese la cantidad a transferir\n"
            "4. Confirme la transferencia"
        )
        
        ttk.Label(
            instructions_frame,
            text=instructions_text,
            font=('Arial', 10),
            justify=tk.LEFT
        ).pack(anchor=tk.W)
        
        # Frame principal de transferencia
        transfer_frame = ttk.LabelFrame(self, text="Transferir Material", padding=10)
        transfer_frame.pack(fill=tk.BOTH, expand=True)
        
        # Información actual
        self.info_label = ttk.Label(
            transfer_frame,
            text="Escanee un código de barras para comenzar",
            font=('Arial', 12),
            foreground='blue'
        )
        self.info_label.pack(pady=(0, 10))
        
        # Frame de entrada
        entry_frame = ttk.Frame(transfer_frame)
        entry_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Scanner
        ttk.Label(entry_frame, text="Código de Barras:", font=('Arial', 10)).grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.barcode_var = tk.StringVar()
        barcode_entry = ttk.Entry(entry_frame, textvariable=self.barcode_var, font=('Arial', 12), width=30)
        barcode_entry.grid(row=0, column=1, pady=5, padx=(10, 5), sticky=tk.W)
        barcode_entry.bind('<Return>', self.on_barcode_scan)
        
        scan_button = ttk.Button(entry_frame, text="🔍 Buscar", command=self.on_barcode_scan)
        scan_button.grid(row=0, column=2, pady=5, padx=(5, 0))
        
        # Obra destino
        ttk.Label(entry_frame, text="Obra Destino:", font=('Arial', 10)).grid(row=1, column=0, sticky=tk.W, pady=5)
        
        self.dest_obra_var = tk.StringVar()
        self.dest_obra_combo = ttk.Combobox(entry_frame, textvariable=self.dest_obra_var, 
                                           font=('Arial', 10), width=30, state='readonly')
        self.dest_obra_combo.grid(row=1, column=1, pady=5, padx=(10, 0), sticky=tk.W)
        
        # Cantidad
        ttk.Label(entry_frame, text="Cantidad:", font=('Arial', 10)).grid(row=2, column=0, sticky=tk.W, pady=5)
        
        self.quantity_var = tk.StringVar(value="1")
        quantity_spinbox = ttk.Spinbox(entry_frame, textvariable=self.quantity_var, 
                                      from_=1, to=9999, font=('Arial', 10), width=10)
        quantity_spinbox.grid(row=2, column=1, pady=5, padx=(10, 0), sticky=tk.W)
        
        # Notas
        ttk.Label(entry_frame, text="Notas:", font=('Arial', 10)).grid(row=3, column=0, sticky=tk.W, pady=5)
        
        self.notes_var = tk.StringVar()
        notes_entry = ttk.Entry(entry_frame, textvariable=self.notes_var, font=('Arial', 10), width=30)
        notes_entry.grid(row=3, column=1, pady=5, padx=(10, 0), sticky=tk.W)
        
        # Botones
        buttons_frame = ttk.Frame(transfer_frame)
        buttons_frame.pack(pady=10)
        
        self.transfer_button = ttk.Button(
            buttons_frame,
            text="🔄 Transferir",
            command=self.execute_transfer,
            state=tk.DISABLED
        )
        self.transfer_button.pack(side=tk.LEFT, padx=(0, 10))
        
        clear_button = ttk.Button(
            buttons_frame,
            text="🧹 Limpiar",
            command=self.clear_form
        )
        clear_button.pack(side=tk.LEFT)
        
        # Variables
        self.current_item = None
        
        # Cargar obras
        self.load_obras()
        
        # Focus en entrada
        barcode_entry.focus()
    
    def load_obras(self):
        """Cargar obras disponibles"""
        obras = self.data_manager.get_obras_by_warehouse(self.warehouse_id)
        self.dest_obra_combo['values'] = obras
    
    def on_barcode_scan(self, event=None):
        """Manejar escaneo de código de barras"""
        barcode = self.barcode_var.get().strip()
        if not barcode:
            return
        
        # Buscar item
        item = self.data_manager.get_item_by_barcode(barcode)
        if item and str(item['warehouse_id']) == str(self.warehouse_id):
            self.current_item = item
            
            # Actualizar información
            info_text = (
                f"Material: {item['name']}\n"
                f"Obra Actual: {item['obra']}\n"
                f"Stock Disponible: {item['stock']}\n"
                f"Código: {item['barcode']}"
            )
            self.info_label.config(text=info_text, foreground='green')
            
            # Habilitar transferencia
            self.transfer_button.config(state=tk.NORMAL)
            
            # Actualizar rango del spinbox
            if hasattr(self, 'quantity_spinbox'):
                self.quantity_spinbox.config(to=item['stock'])
        else:
            self.info_label.config(text="Material no encontrado en esta bodega", foreground='red')
            self.transfer_button.config(state=tk.DISABLED)
            self.current_item = None
    
    def execute_transfer(self):
        """Ejecutar transferencia"""
        if not self.current_item:
            return
        
        dest_obra = self.dest_obra_var.get()
        if not dest_obra:
            tk.messagebox.showwarning("Advertencia", "Debe seleccionar una obra de destino")
            return
        
        if dest_obra == self.current_item['obra']:
            tk.messagebox.showwarning("Advertencia", "La obra de destino debe ser diferente a la actual")
            return
        
        try:
            quantity = int(self.quantity_var.get())
            if quantity <= 0 or quantity > self.current_item['stock']:
                tk.messagebox.showerror("Error", f"Cantidad inválida. Disponible: {self.current_item['stock']}")
                return
        except ValueError:
            tk.messagebox.showerror("Error", "Ingrese una cantidad válida")
            return
        
        # Confirmar transferencia
        if tk.messagebox.askyesno(
            "Confirmar Transferencia",
            f"¿Transferir {quantity} unidades de '{self.current_item['name']}'?\n\n"
            f"De: {self.current_item['obra']}\n"
            f"A: {dest_obra}\n\n"
            f"Esta acción no se puede deshacer."
        ):
            # Ejecutar transferencia
            success = self.data_manager.transfer_item_between_obras(
                str(self.current_item['id']),
                self.current_item['obra'],
                dest_obra,
                quantity,
                self.notes_var.get()
            )
            
            if success:
                tk.messagebox.showinfo("Éxito", "Transferencia realizada exitosamente")
                self.clear_form()
            else:
                tk.messagebox.showerror("Error", "Error al realizar la transferencia")
    
    def clear_form(self):
        """Limpiar formulario"""
        self.barcode_var.set("")
        self.dest_obra_var.set("")
        self.quantity_var.set("1")
        self.notes_var.set("")
        self.current_item = None
        self.transfer_button.config(state=tk.DISABLED)
        self.info_label.config(text="Escanee un código de barras para comenzar", foreground='blue')