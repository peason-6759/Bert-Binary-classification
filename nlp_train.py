import torch
from CofactsDataTest.nlp_prediction import test_predictions

def train_epochs(model, dataloader, lr=0.01, optimizer=None, epoch_size=None, device = 'cuda:0'):
    
    optimizer = optimizer or torch.optim.Adam(model.parameters(), lr=lr)
    # model.train()
    loss_fn = torch.nn.CrossEntropyLoss()
    for epoch in range(epoch_size):
        total_loss, count = 0, 0

        for data in dataloader:

            tokens_tensors, segments_tensors, masks_tensors, labels = [t.to(device) for t in data]
            optimizer.zero_grad()
            outputs = model(input_ids=tokens_tensors, 
                                token_type_ids=segments_tensors, 
                                attention_mask=masks_tensors,
                                labels = labels)
            loss = loss_fn(outputs.logits, labels)
            loss.backward()
            optimizer.step()
            count += len(labels)
            print("len:%d, total_loss%f"%(count, loss.item()))
            total_loss += loss.item() #待處理:make loss to percentage

        
        _, acc, _ = test_predictions(model, dataloader) 
        print('[epoch %d] loss: %f, acc: %f' % (epoch + 1, total_loss/count, acc))
    
