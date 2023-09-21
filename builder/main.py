import re
import sys
import json
import datetime

import serial
import serial.tools.list_ports

from kivy.lang import Builder

from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.list import OneLineAvatarIconListItem

import builder

class MainApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen = Builder.load_file('./layout.kv')

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.title = "TMA-1 Configuration Tool"
        return self.screen

    # read build_config.json and init checkboxes on startup
    def on_start(self, **kwargs):
        with open("build_config.json", "r") as file:
            build_config = json.load(file)

            self.screen.ids.telemetry.state = 'down' if build_config["STM32"]["output"]["telemetry"] else 'normal'
            self.screen.ids.serial.state    = 'down' if build_config["STM32"]["output"]["serial"] else 'normal'

            self.screen.ids.can.state           = 'down' if build_config["STM32"]["sensor"]["can"] else 'normal'
            self.screen.ids.digital.state       = 'down' if build_config["STM32"]["sensor"]["digital"] else 'normal'
            self.screen.ids.analog.state        = 'down' if build_config["STM32"]["sensor"]["analog"] else 'normal'
            self.screen.ids.pulse.state         = 'down' if build_config["STM32"]["sensor"]["pulse"] else 'normal'
            self.screen.ids.accelerometer.state = 'down' if build_config["STM32"]["sensor"]["accelerometer"] else 'normal'
            self.screen.ids.gps.state           = 'down' if build_config["STM32"]["sensor"]["gps"] else 'normal'

            self.screen.ids.debug_mode.state    = 'down' if build_config["STM32"]["debug"]["debug_mode"] else 'normal'
            self.screen.ids.release_build.state = 'down' if build_config["STM32"]["debug"]["release_build"] else 'normal'


    # update build_config.json on checkbox event
    def on_checkbox_active(self, checkbox, value):
        if checkbox in self.screen.ids.values():
            id = list(self.screen.ids.keys())[list(self.screen.ids.values()).index(checkbox)]

            build_config = ''
            with open("build_config.json", "r+") as file:
                build_config = json.load(file)

                if id in build_config["STM32"]["output"]:
                    build_config["STM32"]["output"][id] = value

                elif id in build_config["STM32"]["sensor"]:
                    build_config["STM32"]["sensor"][id] = value

                elif id in build_config["STM32"]["debug"]:
                    build_config["STM32"]["debug"][id] = value

                file.seek(0)
                json.dump(build_config, file, indent=2)
                file.truncate()

    def flash(self):
        builder.clean()
        ret = builder.build()

        if ret == 0:
            self.dialog = MDDialog(text=f'[font=consola.ttf][color=00ff00]&bl;OK&br;[/color] [color=ffffff]flashing successfully finished.[/color][/font]', buttons=[MDFlatButton(text='OK', on_release=self.close_dialog)])
            self.dialog.open()
        else:
            self.dialog = MDDialog(text=f'[font=consola.ttf][color=ff0000]&bl;FAIL&br;[/color] [color=ffffff]flashing failed. please check the console output.[/color][/font]', buttons=[MDFlatButton(text='OK', on_release=self.close_dialog)])
            self.dialog.open()

    def sync_rtc(self):
        ports = sorted([port for port in serial.tools.list_ports.comports()], key=lambda s: int(re.search(r'\d+', s.name).group()))
        ports = list(map(lambda x: OneLineAvatarIconListItem(text=f'[font=Malgun.ttf]{x.description}[/font]', id=x.name, on_release=self.select_port), ports))

        self.dialog = MDDialog(title='[font=consola.ttf]Select UART COM port[/font]', type='confirmation', items=ports, buttons=[MDFlatButton(text='Cancel', on_release=self.close_dialog)])
        self.dialog.open()

    def close_dialog(self, inst):
        self.dialog.dismiss()

    def select_port(self, inst):
        self.dialog.dismiss()

        now = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S").encode()
        checksum = (sum(now) & 0xff).to_bytes()
        now += checksum

        print(f'\nINFO: synchronizing system time to TMA-1 at {inst.id}: {now}\n')

        try:
            target = serial.Serial(port=inst.id, baudrate=115200, timeout=1)
            target.write(now)
            res = target.read(size=3).decode()
            if res == 'ACK':
                print(f'INFO: TMA-1 RTC unit successfully synced with host system time')
                self.dialog = MDDialog(text=f'[font=consola.ttf][color=00ff00]&bl;OK&br;[/color] [color=ffffff]TMA-1 RTC unit successfully synced.[/color][/font]', buttons=[MDFlatButton(text='OK', on_release=self.close_dialog)])
                self.dialog.open()
            elif len(res) == 0:
                print(f'ERROR: RTC sync ACK timeout reached')
                self.dialog = MDDialog(text=f'[font=consola.ttf][color=ff0000]&bl;FAIL&br;[/color] [color=ffffff]RTC sync timed out.[/color][/font]', buttons=[MDFlatButton(text='OK', on_release=self.close_dialog)])
                self.dialog.open()
            else:
                print(f'ERROR: corrupt RTC sync ACK')
                self.dialog = MDDialog(text=f'[font=consola.ttf][color=ff0000]&bl;FAIL&br;[/color] [color=ffffff]RTC sync ACK from TMA-1 is corrrupt.[/color][/font]', buttons=[MDFlatButton(text='OK', on_release=self.close_dialog)])
                self.dialog.open()

            target.close()
        except serial.serialutil.SerialException as e:
            print(f'{e}\nERROR: serial communication failed. please check COM port number or re-plug the adapter.')


if __name__ == "__main__":
    MainApp().run()