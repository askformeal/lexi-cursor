from src.logger import Logger
from src.settings import Settings

class Html():
    def __init__(self, root):
        self.root = root
        self.settings = Settings()
        self.logger = Logger(__name__, root.options.log_level, 
                             self.settings.PATHS['html_log'],
                             )
        self.paths = {
            'home': self.settings.DATA_PATHS['home']
        }
        self.logger.debug('Html module initialized')

    def get(self, name: str, *args: tuple[(str, str)]) -> str:
        """load a html file and replace placeholders

        Args:
            path (str): path to html file
            args (tuple[(str, str)]): replacements

        Returns:
            str: loaded and replaced html
        """        
        with open(self.paths[name], 'r') as f:
            data = f.read()
        data = data.replace('%V', self.settings.VERSION)
        data = data.replace('%GR', self.settings.GITHUB_REPO)
        data = data.replace('%BG', self.settings.BG)
        data = data.replace('%I', self.settings.DATA_PATHS['icon'])
        data = data.replace('%A', f'http://{self.settings.HOST}:{self.settings.PORT}')
        for replacement in args:
            data = data.replace(replacement[0], replacement[1])
        return data