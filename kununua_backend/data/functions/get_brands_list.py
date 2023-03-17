def get_brands_list(path):
    
    result = []
    
    with open(path, 'r', encoding='utf-8') as f:
        result = [line.rstrip('\n') for line in f]
        
    return result