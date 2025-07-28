import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from PIL import Image, ImageTk
import qrcode
from io import BytesIO
from frontend.data_manager import DataManager
from datetime import datetime

class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Inventario Multi-Bodega")
        self.root.geometry("1024x768")
        self.root.configure(bg='#f0f0f0')
        
        # Data manager
        self.data_manager = DataManager()
        
        # Current page
        self.current_frame = None
        
        # Show login page
        self.show_login()
    
    def clear_frame(self):
        """Clear current frame"""
        if self.current_frame:
            self.current_frame.destroy()
    
    def show_login(self):
        """Show login page"""
        self.clear_frame()
        
        self.current_frame = tk.Frame(self.root, bg='#f0f0f0')
        self.current_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = tk.Label(
            self.current_frame,
            text="Sistema de Inventario Multi-Bodega",
            font=('Arial', 24, 'bold'),
            bg='#f0f0f0',
            fg='#2c3e50'
        )
        title_label.pack(pady=50)
        
        # Login frame
        login_frame = tk.Frame(self.current_frame, bg='white', relief=tk.RAISED, bd=2)
        login_frame.pack(pady=20)
        
        # Username
        tk.Label(login_frame, text="Usuario:", font=('Arial', 14), bg='white').pack(pady=10)
        self.username_entry = tk.Entry(login_frame, font=('Arial', 14), width=20)
        self.username_entry.pack(pady=5)
        
        # Password
        tk.Label(login_frame, text="Contraseña:", font=('Arial', 14), bg='white').pack(pady=10)
        self.password_entry = tk.Entry(login_frame, font=('Arial', 14), width=20, show='*')
        self.password_entry.pack(pady=5)
        
        # Login button
        login_btn = tk.Button(
            login_frame,
            text="Iniciar Sesión",
            font=('Arial', 14, 'bold'),
            bg='#3498db',
            fg='white',
            width=15,
            command=self.login
        )
        login_btn.pack(pady=20)
        
        # Bind Enter key
        self.password_entry.bind('<Return>', lambda e: self.login())
        
        # Focus on username
        self.username_entry.focus()
    
    def login(self):
        """Handle login"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showerror("Error", "Por favor ingrese usuario y contraseña")
            return
        
        if self.data_manager.verify_login(username, password):
            self.show_warehouse_selection()
        else:
            messagebox.showerror("Error", "Credenciales incorrectas")
    
    def show_warehouse_selection(self):
        """Show warehouse selection page"""
        self.clear_frame()
        
        self.current_frame = tk.Frame(self.root, bg='#f0f0f0')
        self.current_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header_frame = tk.Frame(self.current_frame, bg='#2c3e50', height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        user = self.data_manager.get_current_user()
        welcome_label = tk.Label(
            header_frame,
            text=f"Bienvenido, {user.get('full_name', 'Usuario')}",
            font=('Arial', 18, 'bold'),
            bg='#2c3e50',
            fg='white'
        )
        welcome_label.pack(side=tk.LEFT, padx=20, pady=25)
        
        logout_btn = tk.Button(
            header_frame,
            text="Cerrar Sesión",
            font=('Arial', 12),
            bg='#e74c3c',
            fg='white',
            command=self.logout
        )
        logout_btn.pack(side=tk.RIGHT, padx=20, pady=25)
        
        # Main content
        main_frame = tk.Frame(self.current_frame, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=50, pady=50)
        
        # Title
        title_label = tk.Label(
            main_frame,
            text="Seleccione su Bodega",
            font=('Arial', 20, 'bold'),
            bg='#f0f0f0',
            fg='#2c3e50'
        )
        title_label.pack(pady=30)
        
        # Warehouse buttons
        warehouses = self.data_manager.get_warehouses()
        
        if not warehouses:
            tk.Label(
                main_frame,
                text="No hay bodegas disponibles",
                font=('Arial', 14),
                bg='#f0f0f0',
                fg='#e74c3c'
            ).pack(pady=20)
            return
        
        for warehouse in warehouses:
            btn = tk.Button(
                main_frame,
                text=f"{warehouse['name']}\n{warehouse.get('location', '')}",
                font=('Arial', 14, 'bold'),
                bg='#3498db',
                fg='white',
                width=30,
                height=3,
                command=lambda w=warehouse: self.select_warehouse(w)
            )
            btn.pack(pady=10)
    
    def select_warehouse(self, warehouse):
        """Select warehouse and show main menu"""
        self.data_manager.set_current_warehouse(warehouse)
        self.show_main_menu()
    
    def show_main_menu(self):
        """Show main menu"""
        self.clear_frame()
        
        self.current_frame = tk.Frame(self.root, bg='#f0f0f0')
        self.current_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        self.create_header()
        
        # Main content
        main_frame = tk.Frame(self.current_frame, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=50, pady=30)
        
        warehouse = self.data_manager.get_current_warehouse()
        title_label = tk.Label(
            main_frame,
            text=f"Bodega: {warehouse['name']}",
            font=('Arial', 20, 'bold'),
            bg='#f0f0f0',
            fg='#2c3e50'
        )
        title_label.pack(pady=30)
        
        # Menu buttons
        buttons_frame = tk.Frame(main_frame, bg='#f0f0f0')
        buttons_frame.pack(expand=True)
        
        # Inventory button
        inventory_btn = tk.Button(
            buttons_frame,
            text="📦\nInventario",
            font=('Arial', 16, 'bold'),
            bg='#3498db',
            fg='white',
            width=15,
            height=4,
            command=self.show_inventory
        )
        inventory_btn.pack(side=tk.LEFT, padx=20)
        
        # Withdrawals button
        withdrawals_btn = tk.Button(
            buttons_frame,
            text="📤\nRetiros",
            font=('Arial', 16, 'bold'),
            bg='#27ae60',
            fg='white',
            width=15,
            height=4,
            command=self.show_withdrawals
        )
        withdrawals_btn.pack(side=tk.LEFT, padx=20)
        
        # History button
        history_btn = tk.Button(
            buttons_frame,
            text="📋\nHistorial",
            font=('Arial', 16, 'bold'),
            bg='#f39c12',
            fg='white',
            width=15,
            height=4,
            command=self.show_history
        )
        history_btn.pack(side=tk.LEFT, padx=20)
    
    def create_header(self):
        """Create header with navigation"""
        header_frame = tk.Frame(self.current_frame, bg='#2c3e50', height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        # Back button
        back_btn = tk.Button(
            header_frame,
            text="← Volver",
            font=('Arial', 12),
            bg='#34495e',
            fg='white',
            command=self.show_main_menu
        )
        back_btn.pack(side=tk.LEFT, padx=20, pady=25)
        
        # Title
        warehouse = self.data_manager.get_current_warehouse()
        title_label = tk.Label(
            header_frame,
            text=f"Bodega: {warehouse['name']}",
            font=('Arial', 16, 'bold'),
            bg='#2c3e50',
            fg='white'
        )
        title_label.pack(side=tk.LEFT, padx=20, pady=25)
        
        # Logout button
        logout_btn = tk.Button(
            header_frame,
            text="Cerrar Sesión",
            font=('Arial', 12),
            bg='#e74c3c',
            fg='white',
            command=self.logout
        )
        logout_btn.pack(side=tk.RIGHT, padx=20, pady=25)
    
    def show_inventory(self):
        """Show inventory page"""
        self.clear_frame()
        
        self.current_frame = tk.Frame(self.root, bg='#f0f0f0')
        self.current_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        self.create_header()
        
        # Main content
        main_frame = tk.Frame(self.current_frame, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title and controls
        controls_frame = tk.Frame(main_frame, bg='#f0f0f0')
        controls_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            controls_frame,
            text="Inventario",
            font=('Arial', 18, 'bold'),
            bg='#f0f0f0',
            fg='#2c3e50'
        ).pack(side=tk.LEFT)
        
        # Add item button
        add_btn = tk.Button(
            controls_frame,
            text="+ Agregar Item",
            font=('Arial', 12, 'bold'),
            bg='#27ae60',
            fg='white',
            command=self.show_add_item_dialog
        )
        add_btn.pack(side=tk.RIGHT, padx=10)
        
        # Refresh button
        refresh_btn = tk.Button(
            controls_frame,
            text="🔄 Actualizar",
            font=('Arial', 12),
            bg='#3498db',
            fg='white',
            command=self.refresh_inventory
        )
        refresh_btn.pack(side=tk.RIGHT)
        
        # Search frame
        search_frame = tk.Frame(main_frame, bg='#f0f0f0')
        search_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(search_frame, text="Buscar:", font=('Arial', 12), bg='#f0f0f0').pack(side=tk.LEFT)
        self.search_entry = tk.Entry(search_frame, font=('Arial', 12), width=30)
        self.search_entry.pack(side=tk.LEFT, padx=10)
        self.search_entry.bind('<KeyRelease>', self.search_items)
        
        # Items list
        list_frame = tk.Frame(main_frame, bg='white', relief=tk.SUNKEN, bd=2)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Treeview for items
        columns = ('Nombre', 'Código', 'Stock', 'Obra', 'Factura')
        self.items_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.items_tree.heading(col, text=col)
            self.items_tree.column(col, width=150)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.items_tree.yview)
        self.items_tree.configure(yscrollcommand=scrollbar.set)
        
        self.items_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Load items
        self.refresh_inventory()
    
    def refresh_inventory(self):
        """Refresh inventory list"""
        # Clear existing items
        for item in self.items_tree.get_children():
            self.items_tree.delete(item)
        
        # Load items
        items = self.data_manager.get_items()
        for item in items:
            self.items_tree.insert('', tk.END, values=(
                item['name'],
                item['barcode'],
                item['stock'],
                item['obra'],
                item['n_factura']
            ))
    
    def search_items(self, event=None):
        """Search items"""
        query = self.search_entry.get().strip()
        
        # Clear existing items
        for item in self.items_tree.get_children():
            self.items_tree.delete(item)
        
        if query:
            items = self.data_manager.search_items(query)
        else:
            items = self.data_manager.get_items()
        
        for item in items:
            self.items_tree.insert('', tk.END, values=(
                item['name'],
                item['barcode'],
                item['stock'],
                item['obra'],
                item['n_factura']
            ))
    
    def show_add_item_dialog(self):
        """Show add item dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Agregar Item")
        dialog.geometry("400x500")
        dialog.configure(bg='#f0f0f0')
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center dialog
        dialog.geometry("+%d+%d" % (self.root.winfo_rootx() + 50, self.root.winfo_rooty() + 50))
        
        # Form fields
        fields = {}
        
        tk.Label(dialog, text="Agregar Nuevo Item", font=('Arial', 16, 'bold'), bg='#f0f0f0').pack(pady=20)
        
        # Name
        tk.Label(dialog, text="Nombre:", font=('Arial', 12), bg='#f0f0f0').pack(anchor=tk.W, padx=20)
        fields['name'] = tk.Entry(dialog, font=('Arial', 12), width=40)
        fields['name'].pack(padx=20, pady=5)
        
        # Description
        tk.Label(dialog, text="Descripción:", font=('Arial', 12), bg='#f0f0f0').pack(anchor=tk.W, padx=20)
        fields['description'] = tk.Entry(dialog, font=('Arial', 12), width=40)
        fields['description'].pack(padx=20, pady=5)
        
        # Barcode
        tk.Label(dialog, text="Código de Barras:", font=('Arial', 12), bg='#f0f0f0').pack(anchor=tk.W, padx=20)
        fields['barcode'] = tk.Entry(dialog, font=('Arial', 12), width=40)
        fields['barcode'].pack(padx=20, pady=5)
        
        # Stock
        tk.Label(dialog, text="Stock Inicial:", font=('Arial', 12), bg='#f0f0f0').pack(anchor=tk.W, padx=20)
        fields['stock'] = tk.Entry(dialog, font=('Arial', 12), width=40)
        fields['stock'].insert(0, "0")
        fields['stock'].pack(padx=20, pady=5)
        
        # Unit price
        tk.Label(dialog, text="Precio Unitario:", font=('Arial', 12), bg='#f0f0f0').pack(anchor=tk.W, padx=20)
        fields['unit_price'] = tk.Entry(dialog, font=('Arial', 12), width=40)
        fields['unit_price'].pack(padx=20, pady=5)
        
        # Obra
        tk.Label(dialog, text="Obra:", font=('Arial', 12), bg='#f0f0f0').pack(anchor=tk.W, padx=20)
        fields['obra'] = tk.Entry(dialog, font=('Arial', 12), width=40)
        warehouse = self.data_manager.get_current_warehouse()
        fields['obra'].insert(0, warehouse['name'])
        fields['obra'].pack(padx=20, pady=5)
        
        # Factura
        tk.Label(dialog, text="Número de Factura:", font=('Arial', 12), bg='#f0f0f0').pack(anchor=tk.W, padx=20)
        fields['n_factura'] = tk.Entry(dialog, font=('Arial', 12), width=40)
        fields['n_factura'].insert(0, warehouse['code'])
        fields['n_factura'].pack(padx=20, pady=5)
        
        # Buttons
        buttons_frame = tk.Frame(dialog, bg='#f0f0f0')
        buttons_frame.pack(pady=20)
        
        def save_item():
            try:
                item_data = {
                    'name': fields['name'].get().strip(),
                    'description': fields['description'].get().strip(),
                    'barcode': fields['barcode'].get().strip(),
                    'stock': int(fields['stock'].get() or 0),
                    'unit_price': float(fields['unit_price'].get()) if fields['unit_price'].get().strip() else None,
                    'obra': fields['obra'].get().strip() or warehouse['name'],
                    'n_factura': fields['n_factura'].get().strip() or warehouse['code']
                }
                
                if not item_data['name'] or not item_data['barcode']:
                    messagebox.showerror("Error", "Nombre y código de barras son obligatorios")
                    return
                
                if self.data_manager.add_item(item_data):
                    messagebox.showinfo("Éxito", "Item agregado correctamente")
                    dialog.destroy()
                    self.refresh_inventory()
                else:
                    messagebox.showerror("Error", "No se pudo agregar el item")
            except ValueError:
                messagebox.showerror("Error", "Stock debe ser un número entero")
            except Exception as e:
                messagebox.showerror("Error", f"Error al agregar item: {str(e)}")
        
        tk.Button(
            buttons_frame,
            text="Guardar",
            font=('Arial', 12, 'bold'),
            bg='#27ae60',
            fg='white',
            width=10,
            command=save_item
        ).pack(side=tk.LEFT, padx=10)
        
        tk.Button(
            buttons_frame,
            text="Cancelar",
            font=('Arial', 12),
            bg='#95a5a6',
            fg='white',
            width=10,
            command=dialog.destroy
        ).pack(side=tk.LEFT, padx=10)
        
        # Focus on name field
        fields['name'].focus()
    
    def show_withdrawals(self):
        """Show withdrawals page"""
        self.clear_frame()
        
        self.current_frame = tk.Frame(self.root, bg='#f0f0f0')
        self.current_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        self.create_header()
        
        # Main content
        main_frame = tk.Frame(self.current_frame, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        tk.Label(
            main_frame,
            text="Retiros",
            font=('Arial', 18, 'bold'),
            bg='#f0f0f0',
            fg='#2c3e50'
        ).pack(pady=10)
        
        # Scanner frame
        scanner_frame = tk.Frame(main_frame, bg='white', relief=tk.RAISED, bd=2)
        scanner_frame.pack(fill=tk.X, pady=10, padx=10)
        
        tk.Label(
            scanner_frame,
            text="Escanear Código de Barras:",
            font=('Arial', 14, 'bold'),
            bg='white'
        ).pack(pady=10)
        
        barcode_frame = tk.Frame(scanner_frame, bg='white')
        barcode_frame.pack(pady=10)
        
        self.barcode_entry = tk.Entry(barcode_frame, font=('Arial', 14), width=30)
        self.barcode_entry.pack(side=tk.LEFT, padx=10)
        self.barcode_entry.bind('<Return>', self.scan_barcode)
        
        scan_btn = tk.Button(
            barcode_frame,
            text="Escanear",
            font=('Arial', 12, 'bold'),
            bg='#3498db',
            fg='white',
            command=self.scan_barcode
        )
        scan_btn.pack(side=tk.LEFT, padx=10)
        
        # Obra frame
        obra_frame = tk.Frame(scanner_frame, bg='white')
        obra_frame.pack(pady=10)
        
        tk.Label(obra_frame, text="Obra:", font=('Arial', 12), bg='white').pack(side=tk.LEFT)
        self.obra_entry = tk.Entry(obra_frame, font=('Arial', 12), width=30)
        self.obra_entry.pack(side=tk.LEFT, padx=10)
        
        # Withdrawal items list
        list_frame = tk.Frame(main_frame, bg='white', relief=tk.SUNKEN, bd=2)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        tk.Label(
            list_frame,
            text="Items para Retiro:",
            font=('Arial', 14, 'bold'),
            bg='white'
        ).pack(pady=10)
        
        # Treeview for withdrawal items
        columns = ('Item', 'Cantidad', 'Stock Disponible', 'Obra', 'Factura')
        self.withdrawal_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=10)
        
        for col in columns:
            self.withdrawal_tree.heading(col, text=col)
            self.withdrawal_tree.column(col, width=150)
        
        # Scrollbar
        withdrawal_scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.withdrawal_tree.yview)
        self.withdrawal_tree.configure(yscrollcommand=withdrawal_scrollbar.set)
        
        self.withdrawal_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        withdrawal_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Buttons frame
        buttons_frame = tk.Frame(main_frame, bg='#f0f0f0')
        buttons_frame.pack(fill=tk.X, pady=10)
        
        # Remove item button
        remove_btn = tk.Button(
            buttons_frame,
            text="Quitar Item",
            font=('Arial', 12),
            bg='#e74c3c',
            fg='white',
            command=self.remove_withdrawal_item
        )
        remove_btn.pack(side=tk.LEFT, padx=10)
        
        # Clear all button
        clear_btn = tk.Button(
            buttons_frame,
            text="Limpiar Todo",
            font=('Arial', 12),
            bg='#95a5a6',
            fg='white',
            command=self.clear_withdrawal
        )
        clear_btn.pack(side=tk.LEFT, padx=10)
        
        # Confirm withdrawal button
        confirm_btn = tk.Button(
            buttons_frame,
            text="Confirmar Retiro",
            font=('Arial', 14, 'bold'),
            bg='#27ae60',
            fg='white',
            command=self.confirm_withdrawal
        )
        confirm_btn.pack(side=tk.RIGHT, padx=10)
        
        # Initialize withdrawal items list
        self.withdrawal_items = []
        
        # Focus on barcode entry
        self.barcode_entry.focus()
    
    def scan_barcode(self, event=None):
        """Scan barcode and add to withdrawal"""
        barcode = self.barcode_entry.get().strip()
        if not barcode:
            return
        
        # Get item by barcode
        item = self.data_manager.get_item_by_barcode(barcode)
        if not item:
            messagebox.showerror("Error", "Item no encontrado")
            self.barcode_entry.delete(0, tk.END)
            return
        
        # Check if item belongs to current warehouse
        warehouse = self.data_manager.get_current_warehouse()
        if str(item['warehouse_id']) != str(warehouse['id']):
            messagebox.showerror("Error", "El item no pertenece a esta bodega")
            self.barcode_entry.delete(0, tk.END)
            return
        
        # Check stock
        if item['stock'] <= 0:
            messagebox.showerror("Error", f"El item {item['name']} no tiene stock disponible")
            self.barcode_entry.delete(0, tk.END)
            return
        
        # Ask for quantity
        quantity = simpledialog.askinteger(
            "Cantidad",
            f"Cantidad a retirar de {item['name']}:\n(Stock disponible: {item['stock']})",
            minvalue=1,
            maxvalue=item['stock']
        )
        
        if quantity:
            # Check if item already in withdrawal list
            existing_item = None
            for wi in self.withdrawal_items:
                if wi['item']['id'] == item['id']:
                    existing_item = wi
                    break
            
            if existing_item:
                new_quantity = existing_item['quantity'] + quantity
                if new_quantity > item['stock']:
                    messagebox.showerror("Error", f"Cantidad total ({new_quantity}) mayor al stock disponible ({item['stock']})")
                else:
                    existing_item['quantity'] = new_quantity
            else:
                self.withdrawal_items.append({
                    'item': item,
                    'quantity': quantity
                })
            
            self.update_withdrawal_list()
        
        self.barcode_entry.delete(0, tk.END)
        self.barcode_entry.focus()
    
    def update_withdrawal_list(self):
        """Update withdrawal items list"""
        # Clear existing items
        for item in self.withdrawal_tree.get_children():
            self.withdrawal_tree.delete(item)
        
        # Add withdrawal items
        for wi in self.withdrawal_items:
            item = wi['item']
            self.withdrawal_tree.insert('', tk.END, values=(
                item['name'],
                wi['quantity'],
                item['stock'],
                item['obra'],
                item['n_factura']
            ))
    
    def remove_withdrawal_item(self):
        """Remove selected item from withdrawal"""
        selection = self.withdrawal_tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Seleccione un item para quitar")
            return
        
        # Get selected item index
        item_index = self.withdrawal_tree.index(selection[0])
        
        # Remove from list
        del self.withdrawal_items[item_index]
        
        # Update display
        self.update_withdrawal_list()
    
    def clear_withdrawal(self):
        """Clear all withdrawal items"""
        if self.withdrawal_items and messagebox.askyesno("Confirmar", "¿Limpiar todos los items del retiro?"):
            self.withdrawal_items.clear()
            self.update_withdrawal_list()
            self.obra_entry.delete(0, tk.END)
    
    def confirm_withdrawal(self):
        """Confirm withdrawal"""
        if not self.withdrawal_items:
            messagebox.showwarning("Advertencia", "No hay items para retirar")
            return
        
        obra = self.obra_entry.get().strip()
        if not obra:
            messagebox.showerror("Error", "Debe especificar la obra")
            return
        
        if messagebox.askyesno("Confirmar", f"¿Confirmar retiro de {len(self.withdrawal_items)} items para la obra '{obra}'?"):
            if self.data_manager.process_withdrawal(self.withdrawal_items, obra):
                messagebox.showinfo("Éxito", "Retiro procesado correctamente")
                # Clear withdrawal
                self.withdrawal_items.clear()
                self.update_withdrawal_list()
                self.obra_entry.delete(0, tk.END)
                self.barcode_entry.focus()
            else:
                messagebox.showerror("Error", "No se pudo procesar el retiro")
    
    def show_history(self):
        """Show history page"""
        self.clear_frame()
        
        self.current_frame = tk.Frame(self.root, bg='#f0f0f0')
        self.current_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        self.create_header()
        
        # Main content
        main_frame = tk.Frame(self.current_frame, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title and controls
        controls_frame = tk.Frame(main_frame, bg='#f0f0f0')
        controls_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            controls_frame,
            text="Historial de Movimientos",
            font=('Arial', 18, 'bold'),
            bg='#f0f0f0',
            fg='#2c3e50'
        ).pack(side=tk.LEFT)
        
        # Refresh button
        refresh_btn = tk.Button(
            controls_frame,
            text="🔄 Actualizar",
            font=('Arial', 12),
            bg='#3498db',
            fg='white',
            command=self.refresh_history
        )
        refresh_btn.pack(side=tk.RIGHT)
        
        # History list
        list_frame = tk.Frame(main_frame, bg='white', relief=tk.SUNKEN, bd=2)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Treeview for history
        columns = ('Fecha', 'Acción', 'Item', 'Cantidad', 'Obra', 'Usuario')
        self.history_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=20)
        
        for col in columns:
            self.history_tree.heading(col, text=col)
            self.history_tree.column(col, width=150)
        
        # Scrollbar
        history_scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=history_scrollbar.set)
        
        self.history_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        history_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Load history
        self.refresh_history()
    
    def refresh_history(self):
        """Refresh history list"""
        # Clear existing items
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        # Load history
        history = self.data_manager.get_history()
        for record in history:
            # Parse date
            try:
                action_date = datetime.fromisoformat(record['action_date'].replace('Z', '+00:00'))
                date_str = action_date.strftime('%d/%m/%Y %H:%M')
            except:
                date_str = record['action_date']
            
            # Action type translation
            action_type = record['action_type']
            if action_type == 'withdrawal':
                action_type = 'Retiro'
            elif action_type == 'addition':
                action_type = 'Ingreso'
            elif action_type == 'adjustment':
                action_type = 'Ajuste'
            
            self.history_tree.insert('', tk.END, values=(
                date_str,
                action_type,
                record['item_name'],
                record['quantity'],
                record['obra'],
                record['user_name']
            ))
    
    def logout(self):
        """Logout user"""
        if messagebox.askyesno("Confirmar", "¿Cerrar sesión?"):
            self.data_manager.logout()
            self.show_login()

def main():
    root = tk.Tk()
    app = InventoryApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()