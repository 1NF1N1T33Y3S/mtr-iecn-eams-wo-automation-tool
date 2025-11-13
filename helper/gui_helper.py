from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.core.window import Window
import core.core
from kivy.logger import Logger, LOG_LEVELS

Logger.disabled = True
Logger.setLevel(LOG_LEVELS["critical"])

Window.size = (250, 100)


class GuiHelper(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.login_button = None

    def build(self):
        layout = GridLayout(cols=1, padding=10, spacing=10, size_hint=(None, None), size=(250, 100))
        # Add a button
        self.login_button = Button(
            text='Complete\nCRCM WorkOrder',
            halign="center",
            valign="middle",
            text_size=(200, 50),  # Match button size or use self.size in dynamic layouts
            size_hint=(None, None),
            size=(200, 50)
        )
        self.login_button.bind(on_press=core.core.main)
        layout.add_widget(self.login_button)
        return layout
