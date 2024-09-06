from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDFlatButton
from kivymd.uix.picker import MDTimePicker
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.selectioncontrol import MDSwitch
from kivy.uix.switch import Switch
from kivy.uix.scrollview import ScrollView
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.card import MDSeparator

from kivymd.uix.button import MDIconButton                                                                                                            

KV = '''
MDScreen:

    MDToolbar:
        title: "My Toolbar"
        elevation: 10
        pos_hint: {"top": 1}
        left_action_items: [["menu", lambda x: app.callback()]]

    ScrollView:
        pos_hint: {"top": 0.9}
        MDGridLayout:
            id: grid_layout
            cols: 1
            adaptive_height: True
            spacing: dp(20)
            padding: dp(10)


            MDBoxLayout:
                size_hint_y: None
                height: dp(48)
                padding: dp(16)
                md_bg_color: 0.9, 0.9, 0.9, 1

                MDLabel:
                    text: "Example Text"
                    halign: "left"

                MDSwitch:
                    pos_hint: {"center_y": 0.5}

                    
                MDIconButton:
                    icon: "dots-vertical"
                    pos_hint: {"center_y": 0.5}
                    on_release: app.open_menu(self)

            MDSeparator:
                height: dp(1)
                    
    MDFloatingActionButtonSpeedDial:
        data: app.data
        root_button_anim: True
        callback: app.on_speed_dial
        anchor: 'right'
        pos_hint: {'center_x': 0.1, 'center_y': 0.9}
'''

class MyApp(MDApp):
    data = {
        'Alarm': 'alarm',
        'Timer': 'timer',
        'Voice Alarm': 'microphone'
    }

    def build(self):
        return Builder.load_string(KV)

    def callback(self):
        print("Menu button pressed")

    def on_speed_dial(self, instance):
        if instance.icon == 'alarm':
            self.show_time_picker()

    def show_time_picker(self):
        time_picker = MDTimePicker()
        time_picker.bind(on_save=self.save_time)
        time_picker.open()

    def save_time(self, instance, time):
        time_str = time.strftime("%H:%M")
        # Save the time to a text file
        with open("time_data.txt", "a") as file:
            file.write(time_str + "\n")
        # Add the time to the ScrollView
        self.add_time_to_scrollview(time_str)

    def add_time_to_scrollview(self, time_str):
        grid_layout = self.root.ids.grid_layout
        box_layout = MDBoxLayout(
            size_hint_y=None,
            height=(88),
            padding=(16),
            md_bg_color=(0.9, 0.9, 0.9, 1),
        )

        label = MDLabel(
            text=f"Time Set: {time_str}",
            halign="left",
        )
        switch = MDSwitch(pos_hint={"center_y": 0.5})
        icon_button = MDIconButton(
            icon="dots-vertical",
            pos_hint={"center_y": 0.5},
            on_release=lambda x: self.open_menu(icon_button),
        )
        divider=MDSeparator(
        height=1
        )
        
        box_layout.add_widget(label)
        box_layout.add_widget(switch)
        box_layout.add_widget(icon_button)
        
        grid_layout.add_widget(box_layout)
        grid_layout.add_widget(divider)

    def open_menu(self, caller):
        self.menu = MDDropdownMenu(
            caller=caller,
            items=[
                {
                    "text": "Edit",
                    "icon": "pencil",
                    "viewclass": "OneLineIconListItem",
                    "on_release": lambda x="Edit": self.menu_callback(x),
                },
                {
                    "text": "Delete",
                    "icon": "delete",
                    "viewclass": "OneLineIconListItem",
                    "on_release": lambda x="Delete": self.menu_callback(x),
                },
            ],
            width_mult=4,
        )
        self.menu.open()

    def menu_callback(self, action):
        if action == "Edit":
            self.show_edit_dialog()
        elif action == "Delete":
            self.delete_item()
        self.menu.dismiss()

    def show_edit_dialog(self):
        self.dialog = MDDialog(
            title="Edit Text",
            type="custom",
            content_cls=MDTextField(text="Example Text"),
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    on_release=self.close_dialog
                ),
                MDFlatButton(
                    text="OK",
                    on_release=self.update_text
                ),
            ],
        )
        self.dialog.open()

    def close_dialog(self, *args):
        self.dialog.dismiss()

    def update_text(self, *args):
        new_text = self.dialog.content_cls.text
        # Update the label text with new_text here
        self.dialog.dismiss()

    def delete_item(self):
        # Perform the deletion logic here
        pass

if __name__ == '__main__':
    MyApp().run()