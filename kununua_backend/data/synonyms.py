from scipy.spatial.distance import cosine
import numpy as np
from deep_translator import GoogleTranslator
from django.utils.translation import gettext_lazy as _
from products.models import Category
import os, shelve, shlex, re

ROOT_PATH = "./data/"
PATH_SHELVE = ROOT_PATH + "shelves/language_model.dat"
PATH_MODEL = ROOT_PATH + "datasets/models/words_vectors.txt"
KEY = "dict"
NOISE = ["and", "or"]

class CategoryFinder():
    def __init__(self):
        self.mem = {}
        self.dict = self._init_dict()
        
    def _init_dict(self):
        if os.path.exists(PATH_SHELVE):
            return self._read_shelve()
        return self._create_dict()
        
    def _create_dict(self):
        words = {}
        with open(PATH_MODEL) as f:
            while True:
                try:
                    row = next(f).split()
                    word = row[0]
                    vector = np.array([float(x) for x in row[1:]])
                    words[word] = vector
                except StopIteration:
                    self._create_shelve(words)
                    return words
    
    @staticmethod
    def _read_shelve():
        shelf = shelve.open(PATH_SHELVE)
        words = shelf[KEY]
        shelf.close()
        return words
    
    @staticmethod
    def _create_shelve(words):
        shelf = shelve.open(PATH_SHELVE)
        shelf[KEY] = words
        shelf.close()
    
    def _compute_synonyms(self, title, word1, word2):
        title = title.lower().strip()
        word1 = word1.lower().strip()
        word2 = word2.lower().strip()
        
        if word1 == word2:
            return 0.0
        
        title_words = [word.strip() for word in shlex.shlex(title) if word.strip() not in NOISE and re.match("\w", word.strip())]
        words = [word.strip() for word in shlex.shlex(word1) if word.strip() not in NOISE and re.match("\w", word.strip())]
        target_words = [word.strip() for word in shlex.shlex(word2) if word.strip() not in NOISE and re.match("\w", word.strip())]
        vector1 = None
        vector2 = None
        for w in title_words:
            try:
                try:
                    vector1 += self.dict[w]
                except TypeError:
                    vector1 = self.dict[w]
            except KeyError:
                print(_(f'{w} not in dict'))
                continue #Revisar
        
        for w in words:
            try:
                try:
                    vector1 += self.dict[w]
                except TypeError:
                    vector1 = self.dict[w]
            except KeyError:
                #raise KeyError(_(f'{w} not in dict'))
                print(_(f'{w} not in dict')) #Revisar
                continue
        
        for w in target_words:
            try:
                try:
                    vector2 += self.dict[w]
                except TypeError:
                    vector2 = self.dict[w]
            except KeyError:
                #raise KeyError(_(f'{w} not in dict'))
                print(_(f'{w} not in dict'))#Revisar
                continue
        if vector1 is None or vector2 is None: #Revisar
            return float("inf")
        result = self._distance(vector1, vector2)
        
        return result
    
    @staticmethod
    def _distance(vector1, vector2):
        return cosine(vector1, vector2)

    def _closest_words(self, embedding, size=20):
        distances = {
            w: self._distance(embedding, self.dict[w])
            for w in self.dict
        }
        return sorted(distances, key=lambda w: distances[w])[:size]

    def _closest_word(self, embedding):
        return self._closest_words(embedding, size=1)

    def find_category(self, title, category, code="es"):
        if not isinstance(title, str):
            raise TypeError(_("title must be a string"))
        if not isinstance(category, str):
            raise TypeError(_("category must be a string"))
        if not isinstance(code, str):
            raise TypeError(_("code must be a string"))
        
        title = title.lower().strip()
        category = category.lower().strip()
        code = code.lower().strip()
        
        if not title:
            raise ValueError(_("title must not be empty"))
        if not category:
            raise ValueError(_("category must not be empty"))
        if len(code) != 3 and len(code) != 2:
            raise ValueError(_("code must be a 3-character string"))
        if len(code) != 2:
            code = code[:-1]
            
        if category in self.mem and title in self.mem[category]:
            return self.mem[category][title]
        
        categories = Category.objects.all()
        categories_filtered = categories.filter(name=category)
        
        if categories_filtered.exists():
            if category not in self.mem:
                self.mem[category] = {}
            final_category = categories_filtered[0]
            self.mem[category][title] = final_category
            return final_category
        
        if code != 'en':
            translator = GoogleTranslator(source=code, target='en')
            title = translator.translate(title).lower().strip()
            category = translator.translate(category).lower().strip()
            
        if category in self.mem and title in self.mem[category]:
            return self.mem[category][title]
        
        result = []   
        for cat in categories:
            cat_name = translator.translate(cat.name).lower().strip()
            score = self._compute_synonyms(title, category, cat_name)
            result.append((cat, score))
        result = sorted(result, key=lambda x: x[1], reverse=False)
        
        if not result: #Revisar
            return None
        print(result)
        category_result = result[0][0]
        if category not in self.mem:
            self.mem[category] = {}
        self.mem[category][title] = category_result
        
        return category_result