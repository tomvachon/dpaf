#!/usr/bin/env python
"""Author: Thomas Vachon"""

import subprocess
import json
import os
import re
import sys

from functools import partial
from fuzzywuzzy import fuzz

os.environ["KIVY_NO_CONSOLELOG"] = "1"
os.environ["KIVY_NO_ARGS"] = "1"
import kivy
kivy.require('1.10.0')


from kivy.config import Config
Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '350')

from kivy.app import App
from kivy.logger import Logger
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.core.window import Window









OP_COMMAND = '/usr/local/bin/op'
CONFIDENCE_THRESHOLD = 45


class LoginScreen(Screen):

    def test_login(self, master_password, op_subdomain):
        #Window.size = (150, 75)
        self.token = ObjectProperty()

        try:

            Logger.debug('Checking for OS Environ Value')

            p = subprocess.Popen([OP_COMMAND, "signin", op_subdomain, "--output=raw"], 
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            token_raw, errs = p.communicate(str.encode(master_password))
            self.token = token_raw.decode("utf-8").rstrip()

            if len(self.token) <= 5:
                Logger.debug("Password is invalid")
                close_button = Button(text='Exit')
                popup = Popup(title='Incorrect Password',
                          content=close_button,
                          auto_dismiss=False)
                close_button.bind(on_press=self.handle_error)
                popup.open()
                        
            Logger.debug("Token is: {}".format(self.token))

        except subprocess.CalledProcessError as err:
            Logger.debug('Error: {}'.format(err))
            Logger.debug('Error calling login')
            close_button = Button(text='Exit')
            popup = Popup(title='Error logging into 1Password CLI',
                          content=close_button,
                          auto_dismiss=False)
            close_button.bind(on_press=self.handle_error)
            popup.open()

        if re.match('Invalid', self.token):
            Logger.debug('Password was incorrect')
            close_button = Button(text='Exit')
            popup = Popup(title='Master Password was incorrect',
                            content=close_button,
                            auto_dismiss=False)
            close_button.bind(on_press=self.handle_error)
            popup.open()

        try:
            Logger.debug("Testing token value via op with token: {}".format(self.token))
            p = subprocess.Popen([OP_COMMAND,
                                            "list",
                                            "vaults",
                                            "--session=" + self.token], 
                                            stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            out, err = p.communicate()
            Logger.debug("OP Login was: {}".format(out.decode("utf-8").rstrip()))
        except subprocess.CalledProcessError:
            Logger.debug('Unable to log into 1pass cli using token')
            close_button = Button(text='Exit')
            popup = Popup(title='Error Listing 1Password Vaults - Run "op signin my" then try again',
                        content=close_button,
                        auto_dismiss=False)
            close_button.bind(on_press=self.handle_error)
            popup.open()
             
        self.op_get_list(token=self.token)
        presentation.current = 'search'
    
    def handle_error(self, *args, **kwargs):
        app = App.get_running_app().stop()


    def op_get_list(self, token):
        """Function to get the JSON list of items from OP"""
        p = subprocess.Popen([OP_COMMAND, "list", "items", "--session=" + token],
                            stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        op_items_raw, err = p.communicate()

        #op_items_raw = TEST_JSON
        try:
            self.json_data = ObjectProperty()
            self.json_data = json.loads(op_items_raw.rstrip())

        except json.JSONDecodeError as err:
            print_err("Failed to pase JSON: {0}".format(err))

class SearchScreen(Screen):
    
    def op_search(self, user_filter):
        """Function to fuzzy search the OP JSON Structures"""
        Logger.debug('Search screen presented')
        #Window.size = (300, 300)
        possible_matches = []
        for item in self.parent.get_screen(name='login').json_data:
            search_field = item['overview']['title']
            if fuzz.ratio(user_filter, search_field) >= CONFIDENCE_THRESHOLD:
                possible_matches.append(search_field)
        self.matches = ObjectProperty()
        self.matches = possible_matches
        if len(possible_matches) > 1:
            presentation.current = 'select'

   
class SelectScreen(Screen):

    def user_select(self):
        """Function to have the user select from multiple close matches"""
        Logger.debug('Select Screen presented')
        #Window.size = (350,400)
        matches = self.parent.get_screen(name='search').matches
        for match in matches:
            button = Button(text=match, id=match)
            button.bind(on_press=partial(self.button_select, match))
            self.ids.grid.add_widget(button)

    def button_select(self, *args):
        title = args[0]
        app = App.get_running_app()
        token = self.parent.get_screen(name='login').token
        app.get_password(title=title, token=token)

presentation = Builder.load_file("main.kv")

def print_err(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

class OpCli(App):

    def build(self):
        self.title = 'iTerm OP'
        return presentation

    def get_password(self, title, token):
        Logger.debug('Get Password running')
        password = self.do_get_password(entry=title, token=token)
        self.return_password(password)
    

    def do_get_password(self, entry, token):
        Logger.debug('do get passeord running')
        p = subprocess.Popen([OP_COMMAND, "get", "item", entry,
                            "--session=" + token], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        item_details_raw, errs = p.communicate()                    
        
        try:
            item_details = json.loads(item_details_raw.decode("utf-8").rstrip())
            for field in item_details['details']['fields']:
                if field['name'] == 'password' or field['designation'] == 'password':
                    password = field['value']
                    return password
        except json.JSONDecodeError:
            print_err("Unable to parse details!")
            sys.exit(2)

    def return_password(self, password):
        Logger.debug('Returning password')
        sys.stdout.write("{}\n".format(password))
        sys.stdout.flush()
        sys.exit(0)

if __name__ == '__main__':
    OpCli().run()
