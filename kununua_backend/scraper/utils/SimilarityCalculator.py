import jellyfish

class SimilarityHelper(object):
    
    def __init__(self):
        self.mem = {}
    
    def compute_string_similarity(self, string1, string2):
        if not string1 and not string2:
            return 1.0
        
        if string1 in self.mem and string2 in self.mem[string1]:
            distance = self.mem[string1][string2]
        else:
            distance = jellyfish.levenshtein_distance(string1, string2)
            if string1 not in self.mem:
                self.mem[string1] = {}
            self.mem[string1][string2] = distance
        
        if len(string1) >= len(string2):
            return 1.0 - (distance/len(string1))
        else:
            return 1.0 - (distance/len(string2))