from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle, Rectangle
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
import os
import subprocess
import re
import threading
from flask import Flask, request
import platform
import ipaddress
import requests
from colorama import Fore

class RoundedButton(Button):
    def __init__(self, **kwargs):
        super(RoundedButton, self).__init__(**kwargs)
        self.background_normal = ''
        self.background_color = (0, 0, 0, 0)
        with self.canvas.before:
            Color(0, 0, 1, 1)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[16])
            self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class RoundedLabel(Label):
    def __init__(self, **kwargs):
        super(RoundedLabel, self).__init__(**kwargs)
        with self.canvas.before:
            Color(0, 0, 0, 1) # white color
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[16])
            self.bind(pos=self.update_rect, size=self.update_rect)
            self.halign = 'left'
            self.valign = 'top'
            self.bind(size=self.on_size)
            self.color = (0, 1, 0, 1) # green color

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
        
    def on_size(self, *args):
        self.text_size = (self.width - 20, self.height - 20)

class MyApp(App):
    def build(self):
        layout = BoxLayout(orientation='horizontal', spacing=10, padding = 10)
        with layout.canvas.before:
            Color(1, 1, 1, 1) # red color
            self.rect = Rectangle(pos=layout.pos, size=layout.size)
            layout.bind(pos=self.update_rect, size=self.update_rect)
        button_layout = BoxLayout(orientation='vertical', size_hint=(0.5, 1), spacing=10)
        button_layout.add_widget(RoundedButton(text='Open Telegram', on_press=self.open_telegram, background_color=(0, 0, 1, 1)))
        button_layout.add_widget(RoundedButton(text='Start Tracking', on_press=self.start_tracking, background_color=(0, 0, 1, 1)))
        self.text_input = RoundedLabel(size_hint=(0.5, 1))
        layout.add_widget(button_layout)
        layout.add_widget(self.text_input)
        return layout

    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def open_telegram(self, instance):
        self.text_input.text += 'Opening Telegram Desktop...\n\n'
        os.system('cmd.exe /c start wsl /usr/bin/telegram-desktop')

    def start_tracking(self, instance):
        self.text_input.text += 'Tracking Started...\n'
        # Run the script to grab IP addresses and display them on a new screen
        subprocess.run(['wsl', 'sudo','tshark', '-i', 'any', '-w', 'data'])
        with open('ip.txt', 'w') as f:
            subprocess.run(['wsl', 'sudo','tshark', '-r', 'data'], stdout=f)
        with open('ip.txt', 'r') as f:
            data = f.read()
        ip_addresses = set(re.findall(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', data))
        os.remove('data')
        os.remove('ip.txt')
        output_text = ''
        for i in ip_addresses:
            city = subprocess.check_output(['wsl', 'curl', '-s', f'https://ipapi.co/{i}/city/']).decode()
            country = subprocess.check_output(['wsl', 'curl', '-s', f'https://ipapi.co/{i}/country/']).decode()
            org = subprocess.check_output(['wsl', 'curl', '-s', f'https://ipapi.co/{i}/org/']).decode()
            if org not in ['Telegram Messenger Inc','Undefined']:
                output_text += f'IP: {i}, City: {city}, Country: {country}, Org: {org}\n'
            
            print(Fore.RED + f"{i}", end = ', ')
            print(Fore.GREEN + subprocess.check_output(['curl', '-s', f'https://ipapi.co/{i}/city/']).decode(), end = ', ')
            print(Fore.GREEN + subprocess.check_output(['curl', '-s', f'https://ipapi.co/{i}/country/']).decode(), end = ', ')
            print(Fore.GREEN + subprocess.check_output(['curl', '-s', f'https://ipapi.co/{i}/org/']).decode())           
        
        self.text_input.text += output_text + '\n'

    def start_server(self, instance):
        threading.Thread(target=run_flask_app).start()
        self.text_input.text += 'Server started at http://localhost:5000\n'

if __name__ == '__main__':
    MyApp().run()