from kivy.uix.screenmanager import Screen

from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRectangleFlatButton

class App(MDApp):
    def build(self):
        screen = Screen()

        screen.add_widget(
            MDRectangleFlatButton(
                text="Hello World",
                pos_hint={"center_x": 0.5, "center_y": 0.5}
            )
        )

        return screen