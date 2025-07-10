import flet as ft
from frontend.utils.session_state import session_state
from frontend.utils.api_client import api_client
from frontend.config import config

class HomePage(ft.UserControl):
    def __init__(self, on_navigate):
        super().__init__()
        self.on_navigate = on_navigate
        self.warehouse_dropdown = None
        self.warehouses = []
    
    def build(self):
        # Load warehouses
        try:
            self.warehouses = api_client.get_warehouses()
        except Exception as e:
            print(f"Error loading warehouses: {e}")
        
        self.warehouse_dropdown = ft.Dropdown(
            label="Seleccionar Bodega",
            hint_text="Elija la bodega donde se encuentra",
            options=[
                ft.dropdown.Option(str(w["id"]), w["name"]) 
                for w in self.warehouses
            ],
            on_change=self._on_warehouse_change,
            height=60,
            text_size=16
        )
        
        # Main action buttons
        inventory_button = ft.ElevatedButton(
            text="Inventario",
            icon=ft.icons.INVENTORY,
            on_click=lambda e: self._navigate_to("inventory"),
            height=80,
            width=200,
            style=ft.ButtonStyle(
                text_style=ft.TextStyle(size=18),
                bgcolor=config.PRIMARY_COLOR
            ),
            disabled=True
        )
        
        withdrawals_button = ft.ElevatedButton(
            text="Retiros",
            icon=ft.icons.REMOVE_SHOPPING_CART,
            on_click=lambda e: self._navigate_to("withdrawals"),
            height=80,
            width=200,
            style=ft.ButtonStyle(
                text_style=ft.TextStyle(size=18),
                bgcolor=config.SUCCESS_COLOR
            ),
            disabled=True
        )
        
        history_button = ft.ElevatedButton(
            text="Historial",
            icon=ft.icons.HISTORY,
            on_click=lambda e: self._navigate_to("history"),
            height=80,
            width=200,
            style=ft.ButtonStyle(
                text_style=ft.TextStyle(size=18),
                bgcolor=config.SECONDARY_COLOR
            ),
            disabled=True
        )
        
        self.action_buttons = [inventory_button, withdrawals_button, history_button]
        
        return ft.Container(
            content=ft.Column([
                # Header
                ft.Container(
                    content=ft.Row([
                        ft.Text(
                            f"Bienvenido, {session_state.current_user.get('full_name', 'Usuario')}",
                            size=20,
                            weight=ft.FontWeight.BOLD
                        ),
                        ft.ElevatedButton(
                            text="Cerrar Sesión",
                            icon=ft.icons.LOGOUT,
                            on_click=self._logout,
                            style=ft.ButtonStyle(
                                bgcolor=config.ERROR_COLOR
                            )
                        )
                    ], 
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    padding=20,
                    bgcolor=ft.colors.WHITE,
                    border_radius=10
                ),
                
                ft.Container(height=30),
                
                # Warehouse selection
                ft.Container(
                    content=ft.Column([
                        ft.Text(
                            "Selección de Bodega",
                            size=18,
                            weight=ft.FontWeight.BOLD
                        ),
                        self.warehouse_dropdown
                    ], spacing=15),
                    padding=20,
                    bgcolor=ft.colors.WHITE,
                    border_radius=10,
                    width=400
                ),
                
                ft.Container(height=30),
                
                # Action buttons
                ft.Container(
                    content=ft.Column([
                        ft.Text(
                            "Opciones Disponibles",
                            size=18,
                            weight=ft.FontWeight.BOLD,
                            text_align=ft.TextAlign.CENTER
                        ),
                        ft.Row(
                            self.action_buttons,
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=20
                        )
                    ], 
                    spacing=20,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    padding=20,
                    bgcolor=ft.colors.WHITE,
                    border_radius=10
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20),
            padding=20,
            bgcolor=config.BACKGROUND_COLOR,
            expand=True
        )
    
    def _on_warehouse_change(self, e):
        if self.warehouse_dropdown.value:
            warehouse_id = int(self.warehouse_dropdown.value)
            selected_warehouse = next(
                (w for w in self.warehouses if w["id"] == warehouse_id), 
                None
            )
            if selected_warehouse:
                session_state.current_warehouse = selected_warehouse
                # Enable action buttons
                for button in self.action_buttons:
                    button.disabled = False
                self.update()
    
    def _navigate_to(self, page: str):
        if not session_state.current_warehouse:
            return
        self.on_navigate(page)
    
    def _logout(self, e):
        session_state.clear()
        self.on_navigate("login")