import torch
import sqlalchemy
from sqlalchemy.orm  import sessionmaker
from torch.utils.data import Dataset
from CofactsDataTest.importData import Articles

engine = sqlalchemy.create_engine("mariadb+mariadbconnector://root:@127.0.0.1:3306/cofacts_testdata")

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

class CofactsDataset(Dataset):

    def __init__(self, mode, tokenizer, train_percentage) :
        assert mode in ["train", "test"]
        self.train_percentage = train_percentage
        self.mode = mode
        self.tokenizer = tokenizer
        self.label_map = {'rumor':1, 'fact':0} #應該用不到
        self.cofacts_data_amount =  session.query(Articles).count()
        if mode =="train":
            self.len = int(train_percentage * self.cofacts_data_amount)
        else:
            self.len = self.cofacts_data_amount - int(train_percentage * self.cofacts_data_amount)
        
    def __getitem__(self, idx):
        #尚未處理[sep]，待研究
        if self.mode =="train":
            article_row = session.query(Articles).filter_by(id = 1 + idx).first()
        else:
            article_row = session.query(Articles).filter_by(id = 1 + idx + int(self.train_percentage * self.cofacts_data_amount) ).first()
            
        rumor = int(article_row.rumor_status)

        if rumor == 0:
            label_tensor = torch.tensor([1,0], dtype=torch.float)
        else:
            label_tensor = torch.tensor([0,1], dtype=torch.float)

        text = article_row.article  
        token = self.tokenizer.tokenize(text)
        word_pieces = ["[CLS]"]  
        word_pieces += token
        ids = self.tokenizer.convert_tokens_to_ids(word_pieces)
        token_tensor = torch.tensor(ids)
        segments_tensor = torch.tensor([0]*len(ids))
        return (token_tensor, segments_tensor, label_tensor)
        

    def __len__(self):
        return self.len
