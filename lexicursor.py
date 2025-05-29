import sys
import tkinter as tk
from tkinterweb import HtmlFrame
from threading import Thread
import json
import os
from typing import Callable

from PIL import Image
from pystray import Menu, MenuItem, Icon

from scr.settings import Settings
from scr.logger import Logger
from scr.search import Search

class LexiCursor:
    def __init__(self):
        self.settings = Settings()
        self.load_options()

        self.code = 0

        self.logger = Logger(__name__, self.log_level, 
                             self.settings.PATHS['main_log'])

        self.win = tk.Tk()
        
        self.setup_win()

        menu = (MenuItem('Show Window', self.show_win, default=True), 
                Menu.SEPARATOR, 
                MenuItem('Exit', lambda: self.exit())
                )
        image = Image.open('./data/icon.ico')
        self.icon = Icon('lexicursor', image, 
                    'LexiCursor', menu)
        
        self.search = Search(self, self.dict_path)
        self.start_thread(target=self.search.load)
        self.logger.debug('Main module initialized')

    def load_options(self):
        """Load from options file
        """        
        with open(self.settings.DATA_PATHS['options'], 'r', encoding='utf-8') as f:
            options = json.load(f)
        self.dict_path = options['dict_path']
        levels = {
            'NOTSET': 0,
            'DEBUG': 10,
            'INFO': 20,
            'WARNING': 30,
            'ERROR': 40,
            'CRITICAL': 50,
        }
        self.log_level = levels[options['log_level']]

    def start_thread(self, target: Callable, args=(), join=False) -> Thread:
        """Start a thread (daemon mode)

        Args:
            target (Callable): target function
            args (tuple, optional): parameter. Defaults to ().
            join (bool, optional): wait for the thread to complete. Defaults to False.

        Returns:
            Thread: started thread
        """        
        t = Thread(target=target, args=args, daemon=True)
        self.logger.debug(f'Start Thread: <{target.__qualname__}>')
        t.start()
        if join:
            t.join()
            self.logger.debug(f'Thread joined: <{target.__qualname__}>')
        return t

    def on_search(self):
        """Handle searching
        """
        result = self.search.search(self.search_entry.get())

    def clear_logs(self):
        """Clear log files
        """        
        self.logger.clear()
        self.search.logger.clear()

    def show_win(self):
        """Show window
        """        
        self.logger.info('Show window')
        self.win.deiconify()
        self.win.focus_set()
        
    def hide_win(self):
        """Hide window
        """        
        if self.win.state() == 'normal':
            self.logger.info('Hide window')
            self.win.withdraw()

    def setup_win(self):
        """Setup window
        """        
        settings = self.settings
        self.win.title(f'LexiCursor {settings.VERSION}')
        self.win.geometry(f'{settings.WIDTH}x{settings.HEIGHT}+{settings.WIN_PADX}+{settings.WIN_PADY}')
        self.win.iconbitmap(self.settings.DATA_PATHS['icon'])
        self.win.config(bg=self.settings.BG)
        self.win.protocol('WM_DELETE_WINDOW', self.hide_win)
        self.win.bind('<Unmap>', lambda event: self.hide_win)

        menubar = tk.Menu(self.win)
        self.win.config(menu=menubar)

        file_menu = tk.Menu(self.win, tearoff=False)
        file_menu.add_separator()
        file_menu.add_command(label='Exit', command=self.exit, underline=0)

        edit_menu = tk.Menu(self.win, tearoff=False)
        edit_menu.add_command(label='Clear log', command=self.clear_logs, underline=0)

        menubar.add_cascade(label='File', menu=file_menu, underline=0)
        menubar.add_cascade(label='Edit', menu=edit_menu, underline=0)

        fr = tk.Frame(self.win, bg=self.settings.BG)
        fr.pack(fill='x',padx=2, pady=2)

        self.search_entry = tk.Entry(fr)
        self.search_entry.pack(side='left', fill='both', expand=True)

        btn = tk.Button(fr, text='Search', command=self.on_search)
        btn.pack(side='left', fill='both', expand=True, padx=(3,0))

        self.page = HtmlFrame(self.win)
        self.page.load_file(self.settings.DATA_PATHS['home'])
        self.page.pack(fill='both', expand=True)

        self.logger.debug('Windows setup completed')

    def exit(self, code = 0):
        """Exit LexiCursor

        Args:
            code (int, optional): exit code. Defaults to 0.
        """        
        if code == 0:
            self.logger.info(f'Exit with code {code}')
        else:
            self.logger.error(f'Exit with code {code}')
        self.code = code
        self.win.destroy()
        self.win.quit()

    def start(self) -> int:
        """Start LexiCursor

        Returns:
            int: exit code:
                0 -> ok
        """        
        self.logger.info('Start LexiCursor')
        self.start_thread(self.icon.run)
        self.win.mainloop()
        return self.code
        
if __name__ == '__main__':
    lexi_cursor = LexiCursor()
    code = lexi_cursor.start()
    sys.exit(code)