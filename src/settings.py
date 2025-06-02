import sys
import os

class Settings:
    def __init__(self):
        self.VERSION = 'v0.0.1'
        self.GITHUB_REPO = 'https://github.com/askformeal/lexi-cursor'
        self.WIDTH = 500
        self.HEIGHT = 700
        self.WIN_PADX = 100
        self.WIN_PADY = 100
        self.BG = 'White'

        self.SEARCH_HOTKEY = 'shift+alt+c'

        self.DICT_ICON_SIZE = (35,35)

        self.PATHS = {
            'options': './options.json',
            'log_dir': './logs',
            'main_log': './logs/main.log',
            'options_log': './logs/options.log',
            'search_log': './logs/search.log',
            'html_log': './logs/html.log',
            'listener_log': './logs/listener.log',
            'dict_log': './logs/dict.log',
            'tools_log': './logs/tools.log',
        }

        self.DATA_PATHS = {
            'res': './data/res',
            'dict_res': './data/res/dict',
            'entries': './data/html/entry',
            'default_options': './data/default_options.json',
            'home': './data/html/home.html',
            'icon': './data/icon.ico',
            'dict_ready': './data/dict_ready.png',
            'dict_loading': './data/dict_loading.png',
            'dict_error': './data/dict_error.png'
        }
        for k,v in self.DATA_PATHS.items():
            self.DATA_PATHS[k] = self.resource_path(v)
            
        self.LOG_MAX_BYTES = 1024*1024
        self.LOG_BACKUP_CNT = 3
        self.SIMILAR_WORD_SHOWN = 10
        
        self.HOST = '127.0.0.1'
        self.PORT = 8080
        self.MAX_LISTEN = 5

        self.HEADER200 = 'HTTP/1.1 200 OK\r\n' \
                    'Content-Type: %CT; charset=UTF-8\r\n' \
                    'Content-Length: %CL\r\n\r\n'
        
    def resource_path(self, relative_path):
        if hasattr(sys, '_MEIPASS'):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")
        path = os.path.join(base_path, relative_path)
        return path