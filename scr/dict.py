from readmdict import MDX, MDD
import os 

class Dict:
    def __init__(self, path: str):
        self.name = os.path.basename(path)
        self.headwords = [*MDX(path, encoding='utf-8')]
        self.items = [*MDX(path, encoding='utf-8').items()]
        mdd_path = path[:-4]+'.mdd'
        if os.path.exists(mdd_path):
            self.mdd_headwords = [*MDD(mdd_path)]
            self.mdd_items = [*MDD(mdd_path).items()]

        
    
    def search(self, word: str):
        """Search a word

        Args:
            word (str): query word

        Returns:
            None: not found
            str: definition of the query word (html)
        """        
        word = word.strip()
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
    
    def __str__(self):
        return self.name