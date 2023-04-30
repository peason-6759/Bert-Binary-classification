'''
    samples in dataloader fn makes dataloader turns a loader for batch size
    example: trainset = dataloader  ->the trainset contain a data
            but if in  DataLoader(trainset, batch_size=BATCH_SIZE, 
                         collate_fn=create_mini_batch)
                                    ->the trainset contain a list of batch siez of data using collate_fn

'''
import torch
from torch.nn.utils.rnn import pad_sequence ##使tensors長度一致

def token_data_batchs(samples):

    tokens_tensors = [s[0] for s in samples]
    segments_tensors = [s[1] for s in samples]

    tokens_tensors = pad_sequence(tokens_tensors, batch_first=True)
    segments_tensors = pad_sequence(segments_tensors, batch_first=True)

    if samples[0][2] is not None:
        label_ids = torch.stack([s[2] for s in samples])
    else:
        label_ids = None
    
    #bert需要關注(將每個字分別遮起來，設1的代表torch需要遮的)
    #遇到問題:有些句子太長(>512)，要處理
    masks_tensors = torch.zeros(tokens_tensors.shape)
    masks_tensors = masks_tensors.masked_fill(
        tokens_tensors != 0, 1) 
    # print(tokens_tensors)
    # print(segments_tensors)
    # print( masks_tensors)
    # print(label_ids)
    return tokens_tensors, segments_tensors, masks_tensors, label_ids


