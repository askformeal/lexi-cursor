from readmdict import MDX, MDD
from Levenshtein import distance
import os 

from scr.settings import Settings
from scr.dict import Dict
from scr.logger import Logger

class Search:
    def __init__(self, root, dir):
        self.root = root
        self.dir = dir
        self.settings = Settings()
        self.logger = Logger(__name__, self.root.log_level, 
                             self.settings.PATHS['search_log']
                             )
        self.dicts: list[Dict] = []
        self.headwords = []
        self.logger.debug('Search module initialized')
        
    def load(self):
        """Load dicts
        """        
        if not os.path.exists(self.dir):
            self.logger.error(f'Dict Folder not found: {self.dir}')
        else:
            paths = os.listdir(self.dir)
            for i in range(len(paths)):
                path = paths[i]
                path = os.path.abspath(os.path.join(self.dir, path))
                if os.path.isfile(path) and (os.path.splitext(path)[-1].lower() == '.mdx'):
                    tmp = Dict(path)
                    self.dicts.append(tmp)
                    self.headwords += tmp.headwords
                    self.logger.info(f'Loaded dict: {str(tmp)} ({i+1}/{len(paths)})')
        self.headwords = set(self.headwords)

    def get_similar_words(self, word: str) -> list[str]:
        """Get similar words

        Args:
            word (str): query word

        Returns:
            list[str]: a list of similar words
        """        
        similar_words = {}
        for headword in self.headwords:
            headword = headword.decode('utf-8')
            sim = distance(word, headword)
            if len(similar_words) < self.settings.SIMILAR_WORD_SHOWN:
                similar_words[headword] = sim
            else:
                similar_words = dict(sorted(similar_words.items(), key=lambda item: item[1]))
                del similar_words[list(similar_words.keys())[-1]]
                similar_words[headword] = sim
        return list(similar_words.keys())

    def search(self, word: str) -> str|list[int]:
        """search a word

        Args:
            word (str): query word

        Returns:
            str: html of the definition
            list[str]: a list of similar words
        """        
        results = ''
        for dict in self.dicts:
            name = dict.name
            self.logger.info(f'Searching \"{word}\" in {name}...')
            result = dict.search(word)
            if result:
                self.logger.info(f'Found')
                results += f'''
                            <h3 style="color: red;">{name}</h3>
                            <hr color="red" size="3"/>
                            {result}
                            '''
            else:
                self.logger.info(f'Not found')
        if result=='':
            self.logger.log(f'No definition for \"{word}\"')
            return self.get_similar_words(word, self.headwords)
        else:
            return results
