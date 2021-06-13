import torch
# from pytorch_pretrained_bert import BertModel
import torch.nn as nn
from .encoder import TransformerInterEncoder
D_MODEL_BERT = 26*3
D_FFN = 128
HEAD = 6
DROPOUT = 0.1
NUM_TLAYER = 10
MAX_LEN_DOCUMENT= 2500

class Summarizer(nn.Module):
    def __init__(self, device):
        super(Summarizer, self).__init__()
        self.device =device
        self.encoder = TransformerInterEncoder(D_MODEL_BERT, D_FFN, HEAD, DROPOUT, NUM_TLAYER)

        self.position_ids=torch.arange(MAX_LEN_DOCUMENT).to(self.device)

        self.to(self.device)
        
    def load_cp(self, pt):
        self.load_state_dict(pt['model'], strict=True)

    def forward(self, X):
        
        Y = torch.sum(X,dim=-1)
        mask_cls = torch.ones_like(Y, dtype=torch.int8)
        mask_cls[Y==0]=0
        mask_cls = mask_cls.bool().to(self.device)

        sent_scores = self.encoder(X, mask_cls).squeeze(-1)
        return sent_scores