from django.core.management.base import BaseCommand
import stanza, itertools

BRANDS = ["Coca-Cola"]
UMBRAL = 0.6

class Command(BaseCommand):
    help = 'Populates the database with the supported brands'

    def handle(self, *args, **options):
        
        def calculate_mean(coef_nouns, coef_adjectives, coef_propnouns, coef_other):
            
            return 0.4 * coef_nouns + 0.2 * coef_adjectives + 0.3 * coef_propnouns + 0.1 * coef_other
        
        def dice_coefficient(set1, set2):
            
            if len(set1) == 0 and len(set2) == 0:
                return 1.0
            elif len(set1) == 0 or len(set2) == 0:
                return 0.0
            else:
                return 2 * len(set1.intersection(set2)) / (len(set1) + len(set2))
        
        def similarity_calculator(doc1, doc2):
            
            nouns_set1 = set()
            adjectives_set1 = set()
            proper_nouns_set1 = set()
            others_set1 = set()
            nouns_set2 = set()
            adjectives_set2 = set()
            proper_nouns_set2 = set()
            others_set2 = set()
            
            for word in doc1.sentences[0].words:
                
                if word.upos == 'NOUN':
                    nouns_set1.add(word.text.lower())
                    
                elif word.upos == 'ADJ':
                    adjectives_set1.add(word.text.lower())
                    
                elif word.upos == 'PROPN':
                    if word.text not in BRANDS:
                        proper_nouns_set1.add(word.text.lower())
                    
                else:
                    if word.upos == 'NUM' or word.upos == 'X':
                        others_set1.add(word.text.lower())
                        
            #print(*[f'id: {word.id}\tword: {word.text}\thead id: {word.head}\thead: {sent.words[word.head-1].text if word.head > 0 else "root"}\tdeprel: {word.deprel}' for sent in doc1.sentences for word in sent.words], sep='\n')
                    
            for word in doc2.sentences[0].words:
                
                if word.upos == 'NOUN':
                    nouns_set2.add(word.text.lower())
                    
                elif word.upos == 'ADJ':
                    adjectives_set2.add(word.text.lower())
                    
                elif word.upos == 'PROPN':
                    if word.text not in BRANDS:
                        proper_nouns_set2.add(word.text.lower())
                    
                else:
                    if word.upos == 'NUM' or word.upos == 'X':
                        others_set2.add(word.text.lower())
                        
            # print(*[f'id: {word.id}\tword: {word.text}\thead id: {word.head}\thead: {sent.words[word.head-1].text if word.head > 0 else "root"}\tdeprel: {word.deprel}' for sent in doc2.sentences for word in sent.words], sep='\n')
               
            coef_nouns = dice_coefficient(nouns_set1, nouns_set2)
            coef_adjectives = dice_coefficient(adjectives_set1, adjectives_set2)
            coef_propnouns = dice_coefficient(proper_nouns_set1, proper_nouns_set2)
            coef_other = dice_coefficient(others_set1, others_set2)
                    
            print(f'Nouns 1: {nouns_set1}, Nouns 2: {nouns_set2} -> {coef_nouns}')
            print(f'Adjectives 1: {adjectives_set1}, Adjectives 2: {adjectives_set2} -> {coef_adjectives}')
            print(f'Proper nouns 1: {proper_nouns_set1}, Proper nouns 2: {proper_nouns_set2} -> {coef_propnouns}')
            print(f'Others 1: {others_set1}, Others 2: {others_set2} -> {coef_other}')
            
            mean = calculate_mean(coef_nouns, coef_adjectives, coef_propnouns, coef_other)
            
            # print(f"Media: {mean}")
            
            return mean
            
            # print(*[f'word: {word.text}\tupos: {word.upos}\txpos: {word.xpos}\tfeats: {word.feats if word.feats else "_"}' for sent in doc1.sentences for word in sent.words], sep='\n')
            # print(*[f'word: {word.text}\tupos: {word.upos}\txpos: {word.xpos}\tfeats: {word.feats if word.feats else "_"}' for sent in doc2.sentences for word in sent.words], sep='\n')
        
        nlp = stanza.Pipeline('es')
        
        doc1 = nlp("Comida perro júnior Compy con pollo, arroz, frutas y verduras")
        doc2 = nlp("Comida gato júnior Compy con pollo, arroz, frutas y verduras")
        doc3 = nlp("Refresco Coca-Cola")
        doc4 = nlp("Refresco cola lata, 330ml")
        doc5 = nlp("Lata de Coca-Cola, 330ml")
        doc6 = nlp("Lata de Coca-Cola")
        doc7 = nlp("Botella de Coca-Cola 1L")
        doc8 = nlp("refresco naranja")
        doc9 = nlp("Refresco Fanta limón")
        
        combinations = itertools.combinations([doc8, doc9], 2)
        
        for c in combinations:
            print(f"Doc 1: {c[0].sentences[0].text}")
            print(f"Doc 2: {c[1].sentences[0].text}")
            similarity = similarity_calculator(c[0], c[1])
            print(f"Similarity: {similarity}")
            print(f"Match: {similarity>UMBRAL}")
            print("-"*50)