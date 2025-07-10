import flet as ft
from frontend.utils.api_client import api_client
from frontend.utils.session_state import session_state
from frontend.config import config
from frontend.components.barcode_scanner import BarcodeScanner

class InventoryPage(ft.UserControl):
    def __init__(self, on_navigate):
        super().__init__()
        self.on_navigate = on_navigate
        self.items_list = None
        self.search_field = None
        self.add_item_dialog = None
        self.items = []
    
    def build(self):
        # Search bar
        self.search_field = ft.TextField(
            label="Buscar items",
            hint_text="Buscar por nombre, código de barras o factura",
            prefix_icon=ft.icons.SEARCH,
            on_change=self._on_search,
            height=60,
            text_size=16
        )
        
        # Items list
        self.items_list = ft.ListView(
            expand=True,
            spacing=10,
            padding=ft.padding.all(10)
        )
        
        # Load initial items
        self._load_items()
        
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
                            f"Inventario - {session_state.current_warehouse['name']}",
                            size=20,
                            weight=ft.FontWeight.BOLD
                        ),
                        ft.ElevatedButton(
                            text="Agregar Item",
                            icon=ft.icons.ADD,
                            on_click=self._show_add_item_dialog,
                            style=ft.ButtonStyle(
                                bgcolor=config.SUCCESS_COLOR
                            )
                        )
                    ], 
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    padding=20,
                    bgcolor=ft.colors.WHITE,
                    border_radius=10
                ),
                
                # Search
                ft.Container(
                    content=self.search_field,
                    padding=ft.padding.symmetric(horizontal=20)
                ),
                
                # Items list
                ft.Container(
                    content=self.items_list,
                    expand=True,
                    padding=ft.padding.symmetric(horizontal=20)
                )
            ]),
            bgcolor=config.BACKGROUND_COLOR,
            expand=True
        )
    
    def _load_items(self):
        try:
            warehouse_id = session_state.current_warehouse["id"]
            self.items = api_client.get_items_by_warehouse(warehouse_id)
            self._update_items_list()
        except Exception as e:
            print(f"Error loading items: {e}")
    
    def _update_items_list(self):
        self.items_list.controls.clear()
        
        for item in self.items:
            item_card = ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Text(
                                item["name"],
                                size=16,
                                weight=ft.FontWeight.BOLD
                            ),
                            ft.Text(
                                f"Stock: {item['stock']}",
                                size=14,
                                color=config.SUCCESS_COLOR if item['stock'] > 0 else config.ERROR_COLOR
                            )
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        
                        ft.Row([
                            ft.Text(f"Código: {item['barcode']}", size=12),
                            ft.Text(f"Obra: {item['obra']}", size=12),
                            ft.Text(f"Factura: {item['n_factura']}", size=12)
                        ], spacing=20)
                    ], spacing=5),
                    padding=15
                )
            )
            self.items_list.controls.append(item_card)
        
        self.update()
    
    def _on_search(self, e):
        query = self.search_field.value
        if not query:
            self._load_items()
            return
        
        try:
            warehouse_id = session_state.current_warehouse["id"]
            self.items = api_client.search_items(query, warehouse_id)
            self._update_items_list()
        except Exception as ex:
            print(f"Error searching items: {ex}")
    
    def _show_add_item_dialog(self, e):
        name_field = ft.TextField(label="Nombre del item", height=60)
        description_field = ft.TextField(label="Descripción", height=60)
        barcode_field = ft.TextField(label="Código de barras", height=60)
        stock_field = ft.TextField(label="Stock inicial", value="0", height=60)
        price_field = ft.TextField(label="Precio unitario", height=60)
        obra_field = ft.TextField(label="Obra", height=60)
        factura_field = ft.TextField(label="Número de factura", height=60)
        
        def save_item(e):
            try:
                item_data = {
                    "name": name_field.value,
                    "description": description_field.value,
                    "barcode": barcode_field.value,
                    "stock": int(stock_field.value or 0),
                    "unit_price": float(price_field.value) if price_field.value else None,
                    "obra": obra_field.value or session_state.current_warehouse["name"],
                    "n_factura": factura_field.value or session_state.current_warehouse["code"],
                    "warehouse_id": session_state.current_warehouse["id"]
                }
                
                api_client.create_item(item_data)
                self.add_item_dialog.open = False
                self.page.update()
                self._load_items()
                
            except Exception as ex:
                print(f"Error creating item: {ex}")
        
        self.add_item_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Agregar Nuevo Item"),
            content=ft.Container(
                content=ft.Column([
                    name_field,
                    description_field,
                    barcode_field,
                    stock_field,
                    price_field,
                    obra_field,
                    factura_field
                ], spacing=10),
                width=400,
                height=500
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: setattr(self.add_item_dialog, 'open', False)),
                ft.ElevatedButton("Guardar", on_click=save_item)
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        
        self.page.dialog = self.add_item_dialog
        self.add_item_dialog.open = True
        self.page.update()