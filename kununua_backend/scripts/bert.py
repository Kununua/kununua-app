from sentence_transformers import CrossEncoder
import itertools

model_names = ["Alex-GF/bert-base-kununua-model",
               "Alex-GF/beto-base-kununua-model"]

sentences = ["Refresco Coca-Cola",
             "Refresco cola lata",
             "Lata de Coca-Cola",
             "refresco naranja",
             "Refresco Fanta limón"
]

for model_name in model_names:
    
    test_cases = itertools.combinations(sentences, 2)
    
    exp_name = model_name.split("/")[-1]
    
    print(f"----------------- {exp_name} ---------------")
    
    model = CrossEncoder(model_name)
    
    i = 1

    print("Experimento\t\tSentence_1\t\tSentence_2\t\t\tScore\t\t\tAre_Similar")

    for sentence in test_cases:
        score = model.predict([sentence])
        
        three_points_sentence_0 = "..." if len(sentence[0])>15 else ""
        three_points_sentence_1 = "..." if len(sentence[1])>15 else ""
        
        print(f"{i}\t\t{sentence[0][:15]}{three_points_sentence_0}\t\t{sentence[1][:15]}{three_points_sentence_1}\t\t{score[0]}\t\t{score[0] > 0.9}")
        
        i += 1
