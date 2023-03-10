from kivy.properties import ObjectProperty, StringProperty
from kivy.clock import mainthread
from kivy.utils import platform
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen

from camera4kivy import Preview
from PIL import Image

from pyzbar.pyzbar import decode


class WindowManager(ScreenManager):
    pass


class InfoScreen(MDScreen):
    item_name = StringProperty("Empty")


class ScanScreen(MDScreen):
    def search_item(self):
        print('ok')
        self.manager.get_screen('second').item_name = self.ids.ti.text

    def on_kv_post(self, obj):
        self.ids.preview.connect_camera(enable_analyze_pixels=True, default_zoom=0.0)

    @mainthread
    def got_result(self, result):
        self.ids.ti.text = str(result[0].decode("utf-8"))


class ScanAnalyze(Preview):
    extracted_data = ObjectProperty(None)

    def analyze_pixels_callback(self, pixels, image_size, image_pos, scale, mirror):
        pimage = Image.frombytes(mode='RGBA', size=image_size, data=pixels)
        list_of_all_barcodes = decode(pimage)

        if list_of_all_barcodes:
            if self.extracted_data:
                self.extracted_data(list_of_all_barcodes[0])
            else:
                print("Not found")


class Me_App(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Yellow"
        if platform == 'android':
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.CAMERA])  # , Permission.RECORD_AUDIO


if __name__ == '__main__':
    Me_App().run()
