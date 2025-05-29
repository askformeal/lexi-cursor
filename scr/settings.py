import sys
import os

class Settings:
    def __init__(self):
        self.VERSION = 'v0.0.0'
        self.WIDTH = 300
        self.HEIGHT = 500
        self.WIN_PADX = 100
        self.WIN_PADY = 100
        self.BG = 'DeepSkyBlue'

        self.PATHS = {
            'main_log': './main.log',
            'search_log': './search.log',
        }

        self.DATA_PATHS = {
            'options': './data/options.json',
            'default_options': './data/default_options.json',
            'home': './data/html/home.html',
            'icon': './data/icon.ico'
        }
        for k,v in self.DATA_PATHS.items():
            self.DATA_PATHS[k] = self.resource_path(v)
            
        self.LOG_MAX_BYTES = 1024
        self.LOG_BACKUP_CNT = 1
        self.SIMILAR_WORD_SHOWN = 10

    def resource_path(self, relative_path):
        if hasattr(sys, '_MEIPASS'):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)