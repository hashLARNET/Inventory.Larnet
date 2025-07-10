import flet as ft
from frontend.utils.api_client import api_client
from frontend.utils.session_state import session_state
from frontend.config import config
from datetime import datetime

class HistoryPage(ft.UserControl):
    def __init__(self, on_navigate):
        super().__init__()
        self.on_navigate = on_navigate
        self.history_list = None
        self.history_records = []
    
    def build(self):
        # History list
        self.history_list = ft.ListView(
            expand=True,
            spacing=10,
            padding=ft.padding.all(10)
        )
        
        # Load history
        self._load_history()
        
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
                            f"Historial - {session_state.current_warehouse['name']}",
                            size=20,
                            weight=ft.FontWeight.BOLD
                        ),
                        ft.ElevatedButton(
                            text="Actualizar",
                            icon=ft.icons.REFRESH,
                            on_click=lambda e: self._load_history(),
                            style=ft.ButtonStyle(
                                bgcolor=config.PRIMARY_COLOR
                            )
                        )
                    ], 
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    padding=20,
                    bgcolor=ft.colors.WHITE,
                    border_radius=10
                ),
                
                # History list
                ft.Container(
                    content=self.history_list,
                    expand=True,
                    padding=ft.padding.symmetric(horizontal=20)
                )
            ]),
            bgcolor=config.BACKGROUND_COLOR,
            expand=True
        )
    
    def _load_history(self):
        try:
            warehouse_id = session_state.current_warehouse["id"]
            self.history_records = api_client.get_history_by_warehouse(warehouse_id)
            self._update_history_list()
        except Exception as e:
            print(f"Error loading history: {e}")
    
    def _update_history_list(self):
        self.history_list.controls.clear()
        
        for record in self.history_records:
            # Parse date
            action_date = datetime.fromisoformat(record["action_date"].replace("Z", "+00:00"))
            date_str = action_date.strftime("%d/%m/%Y")
            time_str = action_date.strftime("%H:%M:%S")
            
            # Action type color
            action_color = config.ERROR_COLOR if record["action_type"] == "withdrawal" else config.SUCCESS_COLOR
            
            history_card = ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Container(
                                content=ft.Text(
                                    record["action_type"].upper(),
                                    color=ft.colors.WHITE,
                                    size=12,
                                    weight=ft.FontWeight.BOLD
                                ),
                                bgcolor=action_color,
                                padding=ft.padding.symmetric(horizontal=8, vertical=4),
                                border_radius=4
                            ),
                            ft.Text(
                                f"{date_str} - {time_str}",
                                size=12,
                                color=config.SECONDARY_COLOR
                            )
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        
                        ft.Row([
                            ft.Text(
                                record["item_name"],
                                size=16,
                                weight=ft.FontWeight.BOLD
                            ),
                            ft.Text(
                                f"Cantidad: {record['quantity']}",
                                size=14,
                                color=action_color
                            )
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        
                        ft.Row([
                            ft.Text(f"Obra: {record['obra']}", size=12),
                            ft.Text(f"Factura: {record['n_factura']}", size=12),
                            ft.Text(f"Usuario: {record['user_name']}", size=12)
                        ], spacing=20)
                    ], spacing=8),
                    padding=15
                )
            )
            self.history_list.controls.append(history_card)
        
        if not self.history_records:
            self.history_list.controls.append(
                ft.Container(
                    content=ft.Text(
                        "No hay registros de historial",
                        size=16,
                        text_align=ft.TextAlign.CENTER,
                        color=config.SECONDARY_COLOR
                    ),
                    alignment=ft.alignment.center,
                    padding=50
                )
            )
        
        self.update()