import tkinter as tk
from tkinter import filedialog
import json
import os

from src.settings import Settings
from src.logger import Logger

class Options:
    def __init__(self, root):
        self.root = root
        self.settings = Settings()
        self.load_options()
        self.logger = Logger(__name__, self.log_level, 
                             self.settings.PATHS['options_log']
                             )
        self.options_win_open = False

    def load_options(self):
        """Load from options file
        """        
        with open(self.settings.PATHS['options'], 'r', encoding='utf-8') as f:
            self.options = json.load(f)
        self.dict_path = self.options['dict_path']
        levels = {
            'NOTSET': 0,
            'DEBUG': 10,
            'INFO': 20,
            'WARNING': 30,
            'ERROR': 40,
            'CRITICAL': 50,
        }
        self.log_level = levels[self.options['log_level']]
        self.always_on_top = self.options['always_on_top']
        self.default_stray = self.options['default_stray']

    def set_options(self):
        def apply_options():
            self.options['dict_path'] = dict_path_entry.get()
            self.options['log_level'] = log_level.get()
            self.options['always_on_top'] = {'Yes':True, 'No':False}[always_on_top.get()]
            self.options['default_stray'] = default_stray.get()

            with open(self.settings.PATHS['options'], 'w') as f:
                json.dump(self.options, f, indent=4)

            self.logger.info(f'New options saved: {self.options}')

        def on_close(apply=False):
            if apply:
                apply_options()
            self.root.win.attributes("-topmost", True)
            self.options_win_open = False
            self.options_win.destroy()

        def load(options: dict):
            set_dict_sentry(options['dict_path'], True)
            log_level.set(options['log_level'])
            always_on_top.set({True: 'Yes', False:'No'}[options['always_on_top']])
            default_stray.set(options['default_stray'])

        def reset():
            self.logger.info('Reset options')
            with open(self.settings.DATA_PATHS['default_options'], 'r') as f:
                default_options = json.load(f)
            load(default_options)

        def open_dir() -> str:
            path = filedialog.askdirectory(parent=self.options_win)
            self.logger.debug(f'Open dict dir: {path}')
            if not os.path.exists(path) and path != '':
                os.makedirs(path)
            return path
        
        def set_dict_sentry(path, blank=False):
            if path != '' or blank:
                dict_path_entry.delete(0, 'end')
                dict_path_entry.insert('end', path)
        if not self.options_win_open:
            self.options_win_open = True
            self.root.win.attributes("-topmost", False)
            self.options_win = tk.Toplevel(self.root.win)
            self.options_win.attributes("-topmost", True)
            self.options_win.protocol('WM_DELETE_WINDOW', on_close)
            self.options_win.focus_set()

            self.options_win.iconbitmap(self.settings.DATA_PATHS['icon'])
            self.options_win.title('Options')

            fr = tk.Frame(self.options_win)
            fr.pack(fill='x', expand=True, padx=5,pady=5)
            
            lbl = tk.Label(fr, text='Dictionary Path')
            lbl.pack(side='left', fill='both', expand=True, padx=(0,5))
            
            dict_path_entry = tk.Entry(fr)
            dict_path_entry.pack(side='left', fill='both', expand=True)

            dict_path_btn = tk.Button(fr, text='...', command=lambda: set_dict_sentry(open_dir()))
            dict_path_btn.pack(side='left', fill='both', padx=(5,0))

            fr = tk.Frame(self.options_win)
            fr.pack(fill='x', expand=True, padx=5,pady=5)
            
            lbl = tk.Label(fr, text='Log Level')
            lbl.pack(side='left', fill='both', expand=True, padx=(0,5))

            log_level = tk.StringVar()
            log_level_menu = tk.OptionMenu(fr,log_level, 
                                        'NOTSET', 'DEBUG',
                                        'INFO', 'WARNING',
                                        'ERROR', 'CRITICAL')
            log_level_menu.pack(side='left', fill='both', expand=True)

            fr = tk.Frame(self.options_win)
            fr.pack(fill='x', expand=True, padx=5,pady=5)
            
            lbl = tk.Label(fr, text='Always on Top')
            lbl.pack(side='left', fill='both', expand=True, padx=(0,5))

            always_on_top = tk.StringVar()
            always_on_top_menu = tk.OptionMenu(fr, always_on_top,
                                            'Yes', 'No')
            always_on_top_menu.pack(side='left', fill='both', expand=True)

            fr = tk.Frame(self.options_win)
            fr.pack(fill='x', expand=True, padx=5,pady=5)

            lbl = tk.Label(fr, text='On stray click')
            lbl.pack(side='left', fill='both', expand=True, padx=(0,5))

            default_stray = tk.StringVar()
            
            default_stray_menu = tk.OptionMenu(fr, default_stray,
                                            'window', 'search')
            default_stray_menu.pack(side='left', fill='both', expand=True)

            fr = tk.Frame(self.options_win)
            fr.pack(fill='x', expand=True, padx=5,pady=(20,5))


            apply_btn = tk.Button(fr, text='Apply', command=lambda: apply_options())
            apply_btn.pack(side='right', fill='both', padx=(15, 0))

            cancel_btn = tk.Button(fr, text='Cancel', command=lambda: on_close(False))
            cancel_btn.pack(side='right', fill='both', padx=(15, 0))

            ok_btn = tk.Button(fr, text='OK', command=lambda: on_close(True))
            ok_btn.pack(side='right', fill='both')

            reset_btn  = tk.Button(fr, text='Reset', command=lambda: reset())
            reset_btn.pack(side='left', fill='both')


            load(self.options)

            self.options_win.mainloop()
        else:
            self.options_win.focus_set()