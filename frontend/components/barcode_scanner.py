import flet as ft
from typing import Callable, Optional

class BarcodeScanner(ft.UserControl):
    def __init__(self, on_scan: Callable[[str], None], placeholder: str = "Escanear código de barras"):
        super().__init__()
        self.on_scan = on_scan
        self.placeholder = placeholder
        self.barcode_input = None
    
    def build(self):
        self.barcode_input = ft.TextField(
            label=self.placeholder,
            hint_text="Escanee o ingrese el código de barras",
            autofocus=True,
            on_submit=self._on_submit,
            height=60,
            text_size=16,
            border_radius=8,
            prefix_icon=ft.icons.QR_CODE_SCANNER
        )
        
        scan_button = ft.ElevatedButton(
            text="Escanear",
            icon=ft.icons.QR_CODE_SCANNER,
            on_click=self._on_scan_click,
            height=60,
            style=ft.ButtonStyle(
                text_style=ft.TextStyle(size=16)
            )
        )
        
        return ft.Row([
            ft.Container(
                content=self.barcode_input,
                expand=True
            ),
            scan_button
        ], spacing=10)
    
    def _on_submit(self, e):
        if self.barcode_input.value:
            self.on_scan(self.barcode_input.value.strip())
            self.barcode_input.value = ""
            self.barcode_input.update()
    
    def _on_scan_click(self, e):
        if self.barcode_input.value:
            self.on_scan(self.barcode_input.value.strip())
            self.barcode_input.value = ""
            self.barcode_input.update()
    
    def clear(self):
        if self.barcode_input:
            self.barcode_input.value = ""
            self.barcode_input.update()
    
    def focus(self):
        if self.barcode_input:
            self.barcode_input.focus()