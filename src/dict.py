import os 
import urllib.parse

from readmdict import MDX, MDD

from src.settings import Settings
from src.tools import Tools

class Dict:
    def __init__(self, root, path: str):
        self.root = root
        self.name = os.path.basename(path)[:-4]

        self.settings = Settings()

        """ self.logger = Logger(__name__, self.root.log_level,
                             self.settings.PATHS['dict_log']) """

        self.headwords = [*MDX(path, encoding='utf-8')]
        self.items = [*MDX(path, encoding='utf-8').items()]
        mdd_path = path[:-4]+'.mdd'
        self.has_mdd = False
        if os.path.exists(mdd_path):
            self.has_mdd = True
            self.mdd_headwords = [*MDD(mdd_path)]
            self.mdd_items = [*MDD(mdd_path).items()]
        self.tools = Tools(self.root, self.root.logger)

        
    
    def search(self, word: str):
        """Search a word

        Args:
            word (str): query word

        Returns:
            None: not found
            str: definition of the query word (html)
        """        
        word = urllib.parse.unquote(word.strip())
        try:
            index = self.headwords.index(word.encode('utf-8'))
        except ValueError:
            try:
                index = self.headwords.index(word.lower().encode('utf-8'))
            except ValueError:
                return None
            
        html = self.items[index][1]
        html = html.decode('utf-8')
        return html
    
    """ def get_res(self, name: str) -> str|None:
        if self.has_mdd:
            data = self.mdd_items[self.mdd_headwords.index(name.encode('utf-8'))][1]
            path = os.path.join(self.settings.DATA_PATHS['dict_res'], name[1:])
            self.tools.create_file(path)
            with open(path, 'wb') as f:
                f.write(data)
            return path """

    def __str__(self):
        return self.name