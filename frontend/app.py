import flet as ft
from frontend.pages.login import LoginPage
from frontend.pages.home import HomePage
from frontend.pages.inventory import InventoryPage
from frontend.pages.withdrawals import WithdrawalsPage
from frontend.pages.history import HistoryPage
from frontend.utils.session_state import session_state
from frontend.config import config

class InventoryApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = config.APP_TITLE
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.window_width = 1024
        self.page.window_height = 768
        self.page.window_resizable = True
        
        # Touch-friendly settings
        self.page.scroll = ft.ScrollMode.AUTO
        
        self.current_page = None
        self.navigate_to("login")
    
    def navigate_to(self, page_name: str):
        self.page.controls.clear()
        
        if page_name == "login":
            self.current_page = LoginPage(on_login_success=lambda: self.navigate_to("home"))
        elif page_name == "home":
            if not session_state.is_authenticated:
                self.navigate_to("login")
                return
            self.current_page = HomePage(on_navigate=self.navigate_to)
        elif page_name == "inventory":
            if not session_state.is_authenticated:
                self.navigate_to("login")
                return
            self.current_page = InventoryPage(on_navigate=self.navigate_to)
        elif page_name == "withdrawals":
            if not session_state.is_authenticated:
                self.navigate_to("login")
                return
            self.current_page = WithdrawalsPage(on_navigate=self.navigate_to)
        elif page_name == "history":
            if not session_state.is_authenticated:
                self.navigate_to("login")
                return
            self.current_page = HistoryPage(on_navigate=self.navigate_to)
        
        self.page.add(self.current_page)
        self.page.update()

def main(page: ft.Page):
    app = InventoryApp(page)

if __name__ == "__main__":
    ft.app(target=main)