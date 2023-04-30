import torch

def test_predictions(model, dataloader):

    predictions = None
    correct, total = 0, 0
    count, total_loss = 0, 0
    loss_fn = torch.nn.CrossEntropyLoss()
    
    with torch.no_grad():
        for data in dataloader: #一次放很多筆(batchs), 一個data為一個batch

            #move tensors to cuda
            if next(model.parameters()).is_cuda:
                data = [t.to("cuda:0") for t in data if t is not None]

            tokens_tensors, segments_tensors, masks_tensors = data[:3]
            try:
                outputs = model(input_ids=tokens_tensors, 
                                token_type_ids=segments_tensors, 
                                attention_mask=masks_tensors)
            except:
                print("the torch size may exceed 512 and raise an error")
                continue

            logits = outputs[0]
            prob_scores = torch.sigmoid(logits)
            binary_prediction = (prob_scores > 0.5 ).int()

            labels = data[3]
            total += labels.size(0)
            correct += (binary_prediction[:,1] == labels[:,1]).sum().item()

            loss = loss_fn(outputs.logits, labels)
            count += len(labels)
            total_loss += loss.item()

            if predictions is None:
                predictions = binary_prediction
            else:
                predictions = torch.cat((predictions, binary_prediction))

        acc = correct/total
        total_loss = total_loss/count
        return predictions, acc, total_loss
