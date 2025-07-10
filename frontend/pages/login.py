import flet as ft
from frontend.utils.api_client import api_client
from frontend.utils.session_state import session_state
from frontend.config import config

class LoginPage(ft.UserControl):
    def __init__(self, on_login_success):
        super().__init__()
        self.on_login_success = on_login_success
        self.username_field = None
        self.password_field = None
        self.error_text = None
        self.login_button = None
    
    def build(self):
        self.username_field = ft.TextField(
            label="Usuario",
            hint_text="Ingrese su nombre de usuario",
            prefix_icon=ft.icons.PERSON,
            height=60,
            text_size=16,
            autofocus=True
        )
        
        self.password_field = ft.TextField(
            label="Contraseña",
            hint_text="Ingrese su contraseña",
            prefix_icon=ft.icons.LOCK,
            password=True,
            can_reveal_password=True,
            height=60,
            text_size=16,
            on_submit=self._on_login
        )
        
        self.login_button = ft.ElevatedButton(
            text="Iniciar Sesión",
            icon=ft.icons.LOGIN,
            on_click=self._on_login,
            height=60,
            width=300,
            style=ft.ButtonStyle(
                text_style=ft.TextStyle(size=18),
                bgcolor=config.PRIMARY_COLOR
            )
        )
        
        self.error_text = ft.Text(
            "",
            color=config.ERROR_COLOR,
            size=14,
            visible=False
        )
        
        return ft.Container(
            content=ft.Column([
                ft.Container(height=50),
                ft.Icon(
                    ft.icons.WAREHOUSE,
                    size=80,
                    color=config.PRIMARY_COLOR
                ),
                ft.Text(
                    config.APP_TITLE,
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Container(height=30),
                ft.Container(
                    content=ft.Column([
                        self.username_field,
                        self.password_field,
                        self.error_text,
                        ft.Container(height=20),
                        self.login_button
                    ], spacing=15),
                    width=350,
                    padding=30,
                    bgcolor=ft.colors.WHITE,
                    border_radius=10,
                    shadow=ft.BoxShadow(
                        spread_radius=1,
                        blur_radius=15,
                        color=ft.colors.BLUE_GREY_300,
                        offset=ft.Offset(0, 0),
                        blur_style=ft.ShadowBlurStyle.OUTER,
                    )
                )
            ], 
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20),
            alignment=ft.alignment.center,
            bgcolor=config.BACKGROUND_COLOR,
            expand=True
        )
    
    def _on_login(self, e):
        username = self.username_field.value
        password = self.password_field.value
        
        if not username or not password:
            self._show_error("Por favor ingrese usuario y contraseña")
            return
        
        try:
            self.login_button.disabled = True
            self.login_button.text = "Iniciando sesión..."
            self.update()
            
            response = api_client.login(username, password)
            session_state.current_user = response["user"]
            
            self.on_login_success()
            
        except Exception as ex:
            self._show_error(f"Error de autenticación: {str(ex)}")
        finally:
            self.login_button.disabled = False
            self.login_button.text = "Iniciar Sesión"
            self.update()
    
    def _show_error(self, message: str):
        self.error_text.value = message
        self.error_text.visible = True
        self.update()