from django.core.management.base import BaseCommand
from scraper.utils.ScraperSQLiteAPI import ScraperSQLiteAPI
from scraper.utils.ClassificatorSQLiteAPI import ClassificatorSQLiteAPI
from scraper.utils.MatchingUtil import MatchingUtil
from sentence_transformers import CrossEncoder
from sentence_transformers.readers import InputExample
import numpy as np
from datetime import datetime
from torch.utils.data import DataLoader
from sentence_transformers.cross_encoder.evaluation import CEBinaryClassificationEvaluator
import math

class Command(BaseCommand):
        
    help = '--------------------------------------------------------\n--------------- SCRAPER LAUNCHER UTILITY ---------------\n--------------------------------------------------------\n'

    def handle(self, *args, **options):
        
        #model_name = "bert-base-uncased"
        model_name = "distilroberta-base"

        classificator_api = ClassificatorSQLiteAPI()
        
        possible_matches = classificator_api.get_possible_matches()

        train, test = np.split(possible_matches, [int(.8*len(possible_matches))])

        print("Total: " + str(len(possible_matches)))
        print("Train: " + str(len(train)))
        print("Test: " + str(len(test)))

        train_samples = []
        test_samples = []

        for match in train:
            train_samples.append(InputExample(texts=[match[1], match[2]], label=int(match[3])))

        for match in test:
            test_samples.append(InputExample(texts=[match[1], match[2]], label=int(match[3])))

        #Configuration
        train_batch_size = 16
        num_epochs = 4
        model_save_path = 'scripts/output/kununua-'+datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        model = CrossEncoder(model_name, num_labels=1)
        print("Modelo cargado.")

        train_dataloader = DataLoader(train_samples, shuffle=True, batch_size=train_batch_size)

        evaluator = CEBinaryClassificationEvaluator.from_input_examples(test_samples, name='kununua-model-performance')

        # Configure the training
        warmup_steps = math.ceil(len(train_dataloader) * num_epochs * 0.1) #10% of train data for warm-up
        print("Warmup-steps: {}".format(warmup_steps))

        model.fit(train_dataloader=train_dataloader,
          evaluator=evaluator,
          epochs=num_epochs,
          evaluation_steps=5000,
          warmup_steps=warmup_steps,
          output_path=model_save_path)