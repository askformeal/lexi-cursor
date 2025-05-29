import logging
import logging.handlers
import re
import os

from scr.settings import Settings

class Logger(logging.Logger):
    def __init__(self, name: str, level: int, path: str):
        """Init logger

        Args:
            name (str): name of logger
            level (int): level of logging:
                0 -> NOTSET
                10 -> DEBUG
                20 -> INFO
                30 -> WARNING
                40 -> ERROR
                50 -> CRITICAL
            path (str): path to log file
        """        
        super().__init__(name, level)
        self.path = path
        self.settings = Settings()
        handler = logging.handlers.RotatingFileHandler(self.path,
                                                    maxBytes=self.settings.LOG_MAX_BYTES,
                                                    backupCount=self.settings.LOG_BACKUP_CNT
                                                    )
        formatter = logging.Formatter('[%(asctime)s] - [%(name)s] - [%(levelname)s] - %(message)s')
        handler.setFormatter(formatter)
        self.addHandler(handler)
        
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        self.addHandler(handler)
        self.debug(f'Logger module \"{self.name}\" initialized')
        
    def clear(self):
        for file in os.listdir('./'):
            if re.match(f'{os.path.basename(self.path)}(\\.[0-9]+)$', file) != None:
                self.info(f'Delete log: {file}')
                try:
                    os.remove(file)
                except PermissionError as e:
                    self.error(f'Failed to delete log: {file}')
        with open(self.path, 'w') as f:
            ...
        self.info(f'Clear log: {self.path}')