from readmdict import MDX, MDD
from Levenshtein import distance
from urllib.parse import urlparse
import os
import re

from src.settings import Settings
from src.dict import Dict
from src.logger import Logger

class Search:
    def __init__(self, root, dir):
        self.root = root
        self.dir = dir
        self.settings = Settings()
        self.logger = Logger(__name__, self.root.options.log_level, 
                             self.settings.PATHS['search_log']
                             )
        self.dicts: list[Dict] = []
        self.headwords = []
        self.dict_state = 'loading'
        self.logger.debug('Search module initialized')
        
    def load(self):
        """Load dicts
        """
        if not os.path.exists(self.dir):
            self.logger.error(f'Dict Folder not found: {self.dir}')
            self.root.set_dict_icon(2)
            self.dict_state = 'error'
            return
        else:
            paths = os.listdir(self.dir)
            dicts = []
            for i in range(len(paths)):
                path = paths[i]
                path = os.path.abspath(os.path.join(self.dir, path))
                if os.path.isfile(path) and (os.path.splitext(path)[-1].lower() == '.mdx'):
                    dicts.append(path)
            
            self.root.set_dict_icon(1, (0,len(dicts)))
            
            for i in range(len(dicts)):
                tmp = Dict(self.root, dicts[i])
                self.dicts.append(tmp)
                self.headwords += tmp.headwords
                self.logger.info(f'Loaded dict: {str(tmp)} ({i+1}/{len(dicts)})')
                self.root.set_dict_icon(1, (i+1,len(dicts)))
        self.headwords = set(self.headwords)
        self.root.set_dict_icon(0)
        self.dict_state = 'ready'
        self.logger.info('All dicts loaded!')

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

    def on_repl_scr(self, word: str):
        print(word.string[:20])
        if word.string.startswith('entry://'):
            return word
        else:
            return 'src=\"\"'
    
    def on_repl_href(self, word: str):
        print(word.string[:20])
        if word.string.startswith('entry://'):
            return word
        else:
            return 'href=\"\"'

    def search(self, word: str) -> str|list[str]:
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
                
                
                """ links = set()
                src_links = re.findall('src=\".+?\"', result)
                for link in src_links:
                    link = link[5:-1]
                    if not link.startswith('entry://'):
                        tmp = urlparse(link)
                        link = tmp.netloc + tmp.path
                        result.replace(tmp.scheme, '')
                        self.logger.debug(f'Find link: {link}')
                        links.add(link)
                        
                href_links = re.findall('href=\".+?\"', result)
                for link in href_links:
                    link = link[6:-1]
                    if not link.startswith('entry://'):
                        tmp = urlparse(link)
                        link = tmp.netloc + tmp.path
                        result.replace(tmp.scheme, '')
                        self.logger.debug(f'Find link: {link}')
                        links.add(link)
                        
                for link in links:
                    # self.logger.debug(link)
                    dict.get_res(f'\{link}')
                    result = result.replace(link,
                                        f'http://{self.settings.HOST}:{self.settings.PORT}/res/dict/{link}', 
                                        ) """
                results += f'''
                            <h3 style="color: red;">{name}</h3>
                            <hr color="red" size="3"/>
                            {result}
                            '''
            else:
                self.logger.info(f'Not found')
            
        if results=='':
            results = f'<h2>Sorry, No definition for "{word}"...<br>Are you looking for:</h2>'
            self.logger.info(f'No definition for \"{word}\"')
            similar_words = self.get_similar_words(word)
            for word in similar_words:
                results += f'''
                            <font size=\"4\">
                                    <a href=\"http://{self.settings.HOST}:{self.settings.PORT}/entry/{word}\">{word}</a>
                            </font>
                            <br>
                            '''
        
        return results
    
    def clear_res(self):
        pass
