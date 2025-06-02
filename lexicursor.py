import os
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinterweb import HtmlFrame
import webbrowser
from time import sleep
import sys

from PIL import Image, ImageTk
from pystray import Menu, MenuItem, Icon
import pyautogui
import pyperclip
import keyboard

from src.settings import Settings
from src.options import Options
from src.logger import Logger
from src.search import Search
from src.html import Html
from src.listener import Listener
from src.tools import Tools

class LexiCursor:
    def __init__(self):
        self.settings = Settings()
        self.options = Options(self)
        self.options.load_options()


        self.code = 0

        self.logger = Logger(__name__, self.options.log_level, 
                             self.settings.PATHS['main_log'])
        
        if hasattr(sys, '_MEIPASS'):
            self.logger.debug('Environment: Application')
        else:
            self.logger.debug('Environment: Developing')
            
        self.tools = Tools(self, self.logger)

        self.win = tk.Tk()
        
        if self.options.default_stray == 'window':
            menu = (
                    MenuItem('Show Window', self.show_win, default=True),
                    MenuItem('Search Clipboard', self.search_clip),
                    )
        else:
            menu = (
                    MenuItem('Search Clipboard', self.search_clip, default=True),
                    MenuItem('Show Window', self.show_win), 
                    )
        menu += (
                Menu.SEPARATOR, 
                MenuItem('Exit', lambda: self.exit())
                )
        image = Image.open(self.settings.DATA_PATHS['icon'])
        self.icon = Icon('lexicursor', image, 
                    'LexiCursor', menu)
        
        self.search = Search(self, self.options.dict_path)
        self.tools.start_thread(target=self.search.load)

        self.html = Html(self)

        self.listener = Listener(self)

        self.setup_win()

        keyboard.add_hotkey(self.settings.SEARCH_HOTKEY, self.search_clip)

        self.logger.debug('Main module initialized')

    def on_search(self, word: str|None=None):
        """Handle searching
        """
        if self.search.dict_state == 'loading':
            messagebox.showinfo('INFO', 'Please wait until all the dictionaries are loaded')
            return
        elif self.search.dict_state == 'error':
            messagebox.showerror('ERROR', 'Failed to load dictionaries:\n'\
                                 f'Path not found: \"{self.options.dict_path}\"')
            return
        if not word:
            word = self.search_entry.get()
            self.search_entry.delete(0, 'end')
        self.page.load_url(f'http://{self.settings.HOST}:{self.settings.PORT}/entry/{word}')

    def search_clip(self):
        self.on_search(pyperclip.paste())
        self.show_win()

    def clear_logs(self):
        """Clear log files
        """        
        self.logger.clear()
        self.search.logger.clear()
        self.html.logger.clear()
        self.listener.logger.clear()
        self.options.logger.clear()

    def show_win(self):
        """Show window
        """        
        self.logger.info('Show window')
        self.win.deiconify()
        if not self.options.always_on_top:
            self.win.attributes("-topmost", True)
            self.win.attributes("-topmost", False)
        self.win.focus_set()
        
    def hide_win(self, event=None):
        """Hide window
        """        
        if self.win.state() == 'normal':
            self.logger.info('Hide window')
            self.win.withdraw()

    def set_dict_icon(self, code, progress: tuple[int, int]|None=None):
        """
        codes:\n
        0 -> ready\n
        1 -> loading\n
        2 -> error\n
        """
        if code == 0:
            image = Image.open(self.settings.DATA_PATHS['dict_ready'])
        elif code == 1:
            image = Image.open(self.settings.DATA_PATHS['dict_loading'])
        elif code == 2:
            image = Image.open(self.settings.DATA_PATHS['dict_error'])
        image = image.resize(self.settings.DICT_ICON_SIZE)
        self.dict_icon_img = ImageTk.PhotoImage(image)
        self.dict_icon.config(image=self.dict_icon_img)

        if progress:
            self.dict_progress.config(text=f'{progress[0]}/{progress[1]}')

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
        self.win.bind('<Control-p>', lambda event: self.options.set_options())
        if self.options.always_on_top:
            self.win.attributes("-topmost", True)

        menubar = tk.Menu(self.win)
        self.win.config(menu=menubar)

        file_menu = tk.Menu(self.win, tearoff=False)
        file_menu.add_command(label='Open homepage', 
                              command=lambda: self.page.load_url(
                                  f'http://{self.settings.HOST}:{self.settings.PORT}'
                                  ),
                                  underline=0)
        file_menu.add_separator()
        file_menu.add_command(label='Exit', command=self.exit, underline=0)

        edit_menu = tk.Menu(self.win, tearoff=False)
        edit_menu.add_command(label='Clear log', command=self.clear_logs, underline=0)
        edit_menu.add_separator()
        edit_menu.add_command(label='Options', accelerator='Ctrl+P',
                              command=self.options.set_options, underline=0)

        help_menu = tk.Menu(self.win, tearoff=False)
        help_menu.add_command(label='Open GitHub repo', 
                              command=lambda: webbrowser.open(self.settings.GITHUB_REPO),
                              underline=0)
        help_menu.add_separator()
        help_menu.add_command(label='About',
                              command=lambda: messagebox.showinfo('About', f'LexiCursor {self.settings.VERSION}\n'\
                                                                  'By Demons1014\n'\
                                                                    'License: GPL v3.0'),
                              underline=0)

        menubar.add_cascade(label='File', menu=file_menu, underline=0)
        menubar.add_cascade(label='Edit', menu=edit_menu, underline=0)
        menubar.add_cascade(label='Help', menu=help_menu, underline=0)

        fr = tk.Frame(self.win, bg=self.settings.BG)
        fr.pack(fill='x',padx=2, pady=2)

        self.search_entry = tk.Entry(fr)
        self.search_entry.bind('<Return>', lambda event: self.on_search())
        self.search_entry.pack(side='left', fill='both', expand=True)

        btn = tk.Button(fr, text='Search', command=self.on_search)
        btn.pack(side='left', fill='both', expand=True, padx=(3,0))
        
        fr = tk.Frame(self.win, bg=self.settings.BG)
        fr.pack(side='bottom', anchor='sw')
        
        self.dict_icon = tk.Label(fr, bg=self.settings.BG)
        self.dict_icon.pack(side='left', fill='both', expand=True)

        self.dict_progress = tk.Label(fr, bg=self.settings.BG)
        self.dict_progress.pack(side='left', fill='both', expand=True, padx=(5,0))

        self.page = HtmlFrame(self.win, messages_enabled=False)

        self.page.pack(fill='both', expand=True)

        

        self.logger.debug('Windows setup completed')

    def exit(self, code = 0):
        """Exit LexiCursor

        Args:
            code (int, optional): exit code. Defaults to 0.
        """
        self.code = code
        try:
            if code == 0:
                self.logger.info(f'Exit with code {code}')
            else:
                self.logger.error(f'Exit with code {code}')
            self.win.destroy()
            self.win.quit()
        except AttributeError:
            sys.exit(1)

    def start(self) -> int:
        """Start LexiCursor

        Returns:
            int: exit code:
                0 -> ok
        """ 
        self.logger.info('Start LexiCursor')
        self.tools.start_thread(self.icon.run)
        self.listener.start()
        self.page.load_url(f'http://{self.settings.HOST}:{self.settings.PORT}')
        self.win.mainloop()
        return self.code
        
if __name__ == '__main__':
    lexi_cursor = LexiCursor()
    code = lexi_cursor.start()
    sys.exit(code)