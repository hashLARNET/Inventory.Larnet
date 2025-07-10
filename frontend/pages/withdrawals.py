import flet as ft
from frontend.utils.api_client import api_client
from frontend.utils.session_state import session_state
from frontend.config import config
from frontend.components.barcode_scanner import BarcodeScanner

class WithdrawalsPage(ft.UserControl):
    def __init__(self, on_navigate):
        super().__init__()
        self.on_navigate = on_navigate
        self.barcode_scanner = None
        self.obra_field = None
        self.withdrawal_items = []
        self.items_list = None
        self.confirm_button = None
    
    def build(self):
        # Barcode scanner
        self.barcode_scanner = BarcodeScanner(
            on_scan=self._on_barcode_scan,
            placeholder="Escanear código de barras para retiro"
        )
        
        # Obra field
        self.obra_field = ft.TextField(
            label="Obra",
            hint_text="Ingrese el nombre de la obra",
            height=60,
            text_size=16,
            prefix_icon=ft.icons.BUSINESS
        )
        
        # Items list for withdrawal
        self.items_list = ft.ListView(
            expand=True,
            spacing=10,
            padding=ft.padding.all(10)
        )
        
        # Confirm withdrawal button
        self.confirm_button = ft.ElevatedButton(
            text="Confirmar Retiro",
            icon=ft.icons.CHECK,
            on_click=self._confirm_withdrawal,
            height=60,
            style=ft.ButtonStyle(
                text_style=ft.TextStyle(size=18),
                bgcolor=config.SUCCESS_COLOR
            ),
            disabled=True
        )
        
        return ft.Container(
            content=ft.Column([
                # Header
                ft.Container(
                    content=ft.Row([
                        ft.IconButton(
                            icon=ft.icons.ARROW_BACK,
                            on_click=lambda e: self.on_navigate("home"),
                            icon_size=30
                        ),
                        ft.Text(
                            f"Retiros - {session_state.current_warehouse['name']}",
                            size=20,
                            weight=ft.FontWeight.BOLD
                        )
                    ]),
                    padding=20,
                    bgcolor=ft.colors.WHITE,
                    border_radius=10
                ),
                
                # Scanner and obra
                ft.Container(
                    content=ft.Column([
                        self.barcode_scanner,
                        ft.Container(height=10),
                        self.obra_field
                    ]),
                    padding=20,
                    bgcolor=ft.colors.WHITE,
                    border_radius=10
                ),
                
                # Items for withdrawal
                ft.Container(
                    content=ft.Column([
                        ft.Text(
                            "Items para Retiro",
                            size=16,
                            weight=ft.FontWeight.BOLD
                        ),
                        ft.Container(
                            content=self.items_list,
                            height=300,
                            border=ft.border.all(1, ft.colors.GREY_300),
                            border_radius=10
                        )
                    ], spacing=10),
                    padding=20
                ),
                
                # Confirm button
                ft.Container(
                    content=self.confirm_button,
                    padding=20,
                    alignment=ft.alignment.center
                )
            ]),
            bgcolor=config.BACKGROUND_COLOR,
            expand=True
        )
    
    def _on_barcode_scan(self, barcode: str):
        try:
            item = api_client.get_item_by_barcode(barcode)
            
            # Check if item belongs to current warehouse
            if item["warehouse_id"] != session_state.current_warehouse["id"]:
                self._show_error("El item no pertenece a esta bodega")
                return
            
            # Check if item has stock
            if item["stock"] <= 0:
                self._show_error(f"El item {item['name']} no tiene stock disponible")
                return
            
            # Show quantity selection dialog
            self._show_quantity_dialog(item)
            
        except Exception as e:
            self._show_error(f"Error al buscar item: {str(e)}")
    
    def _show_quantity_dialog(self, item):
        quantity_field = ft.TextField(
            label="Cantidad a retirar",
            value="1",
            height=60,
            text_size=16,
            keyboard_type=ft.KeyboardType.NUMBER
        )
        
        def add_to_withdrawal(e):
            try:
                quantity = int(quantity_field.value or 0)
                if quantity <= 0:
                    return
                
                if quantity > item["stock"]:
                    self._show_error(f"Cantidad solicitada ({quantity}) mayor al stock disponible ({item['stock']})")
                    return
                
                # Check if item already in withdrawal list
                existing_item = next(
                    (wi for wi in self.withdrawal_items if wi["item"]["id"] == item["id"]), 
                    None
                )
                
                if existing_item:
                    existing_item["quantity"] += quantity
                else:
                    self.withdrawal_items.append({
                        "item": item,
                        "quantity": quantity
                    })
                
                self._update_withdrawal_list()
                quantity_dialog.open = False
                self.page.update()
                
            except ValueError:
                self._show_error("Ingrese una cantidad válida")
        
        quantity_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"Retirar: {item['name']}"),
            content=ft.Container(
                content=ft.Column([
                    ft.Text(f"Stock disponible: {item['stock']}"),
                    ft.Text(f"Obra: {item['obra']}"),
                    ft.Text(f"Factura: {item['n_factura']}"),
                    ft.Container(height=10),
                    quantity_field
                ], spacing=10),
                width=300
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: setattr(quantity_dialog, 'open', False)),
                ft.ElevatedButton("Agregar", on_click=add_to_withdrawal)
            ]
        )
        
        self.page.dialog = quantity_dialog
        quantity_dialog.open = True
        self.page.update()
    
    def _update_withdrawal_list(self):
        self.items_list.controls.clear()
        
        for wi in self.withdrawal_items:
            item = wi["item"]
            quantity = wi["quantity"]
            
            item_card = ft.Card(
                content=ft.Container(
                    content=ft.Row([
                        ft.Column([
                            ft.Text(item["name"], weight=ft.FontWeight.BOLD),
                            ft.Text(f"Obra: {item['obra']}", size=12),
                            ft.Text(f"Factura: {item['n_factura']}", size=12)
                        ], expand=True),
                        ft.Column([
                            ft.Text(f"Cantidad: {quantity}", size=14),
                            ft.IconButton(
                                icon=ft.icons.DELETE,
                                on_click=lambda e, item_id=item["id"]: self._remove_from_withdrawal(item_id),
                                icon_color=config.ERROR_COLOR
                            )
                        ])
                    ]),
                    padding=15
                )
            )
            self.items_list.controls.append(item_card)
        
        # Enable/disable confirm button
        self.confirm_button.disabled = len(self.withdrawal_items) == 0
        self.update()
    
    def _remove_from_withdrawal(self, item_id: str):
        self.withdrawal_items = [wi for wi in self.withdrawal_items if wi["item"]["id"] != item_id]
        self._update_withdrawal_list()
    
    def _confirm_withdrawal(self, e):
        if not self.obra_field.value:
            self._show_error("Debe especificar la obra")
            return
        
        if not self.withdrawal_items:
            self._show_error("Debe agregar al menos un item")
            return
        
        try:
            withdrawal_data = {
                "obra": self.obra_field.value,
                "warehouse_id": session_state.current_warehouse["id"],
                "items": [
                    {
                        "item_id": wi["item"]["id"],
                        "quantity": wi["quantity"]
                    }
                    for wi in self.withdrawal_items
                ]
            }
            
            api_client.create_withdrawal(withdrawal_data)
            
            # Clear form
            self.withdrawal_items.clear()
            self.obra_field.value = ""
            self._update_withdrawal_list()
            self.barcode_scanner.clear()
            
            self._show_success("Retiro confirmado exitosamente")
            
        except Exception as ex:
            self._show_error(f"Error al confirmar retiro: {str(ex)}")
    
    def _show_error(self, message: str):
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(message),
            bgcolor=config.ERROR_COLOR
        )
        self.page.snack_bar.open = True
        self.page.update()
    
    def _show_success(self, message: str):
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(message),
            bgcolor=config.SUCCESS_COLOR
        )
        self.page.snack_bar.open = True
        self.page.update()