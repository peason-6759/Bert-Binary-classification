import torch
from CofactsDataTest.bertCofactsDataset import CofactsDataset
from CofactsDataTest.bertCofactsDataLoader import token_data_batchs
from CofactsDataTest.nlp_prediction import test_predictions
from CofactsDataTest.nlp_train import train_epochs
from transformers import BertTokenizerFast
from transformers import BertForSequenceClassification
from torch.utils.data import DataLoader
tokenizer = BertTokenizerFast.from_pretrained('bert-base-chinese')
trainset = CofactsDataset("test", tokenizer, train_percentage = 0.8) #test是沒有label的

# token_tensor, segments_tensor, label_tensor = trainset[40]
# tokens = tokenizer.convert_ids_to_tokens(token_tensor.tolist())

BATCH_SIZE = 5 #32,64
trainloader = DataLoader(trainset, batch_size = BATCH_SIZE, 
                         collate_fn = token_data_batchs)

# data = next(iter(trainloader))
# tokens_tensors, segments_tensors, \
#     masks_tensors, label_ids = data
    
# print(f"""
# tokens_tensors.shape   = {tokens_tensors.shape} 
# {tokens_tensors}
# ------------------------
# segments_tensors.shape = {segments_tensors.shape}
# {segments_tensors}
# ------------------------
# masks_tensors.shape    = {masks_tensors.shape}
# {masks_tensors}
# ------------------------
# label_ids.shape        = {label_ids.shape}
# {label_ids}
# """)


PRETRAINED_MODEL_NAME = "bert-base-chinese"
NUM_LABELS = 2
model = BertForSequenceClassification.from_pretrained(
    PRETRAINED_MODEL_NAME, num_labels=NUM_LABELS)
# for module in model.named_children():
#     print(module)
# model.config


device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
print("device:", device)
model = model.to(device)

# # only test model
# try:
#     _, acc = test_predictions(model, trainloader)
# except ValueError:
#     print("the tensor size exceed 512")
# print("classification acc:", acc)


model.train()
optimizer = torch.optim.Adam(model.parameters(), lr = 1e-5)
train_epochs(model, dataloader = trainloader, lr = 1e-5 , optimizer=optimizer, epoch_size=8, device=device)
model.save_pretrained('data/cofacts_saved_binary_classification/')
