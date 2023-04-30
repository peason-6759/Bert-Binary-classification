import torch
from CofactsDataTest.bertCofactsDataset import CofactsDataset
from CofactsDataTest.bertCofactsDataLoader import token_data_batchs
from CofactsDataTest.nlp_prediction import test_predictions
from torch.utils.data import DataLoader
from transformers import BertTokenizerFast
from transformers import BertForSequenceClassification

tokenizer = BertTokenizerFast.from_pretrained('bert-base-chinese')
testset = CofactsDataset("test", tokenizer, train_percentage=0.8) 

BATCH_SIZE = 10
NUM_LABELS = 2

testloader = DataLoader(testset, batch_size = BATCH_SIZE, 
                         collate_fn = token_data_batchs)

LOADED_MODEL_NAME = 'data/cofacts_saved_binary_classification'
model = BertForSequenceClassification.from_pretrained(
    LOADED_MODEL_NAME, num_labels=NUM_LABELS)

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
print("device:", device)
model = model.to(device)
#validation
_, acc, loss = test_predictions(model, dataloader = testloader)
print(acc)
print(loss)