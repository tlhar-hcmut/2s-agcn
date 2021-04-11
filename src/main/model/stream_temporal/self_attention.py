import torch
from torch import nn 
import torch.nn.functional as F

class SelfAttention(nn.Module):
    def __init__(self, len_feature_input, len_feature_new, dropout = 0, **kwargs):

        self.len_feature_new = len_feature_new
        super(SelfAttention, self).__init__(**kwargs)
        self.W_k =nn.Linear(len_feature_input, len_feature_new)
        self.W_q =nn.Linear(len_feature_input, len_feature_new)
        self.W_v =nn.Linear(len_feature_input, len_feature_new)

        self.dropout = nn.Dropout(dropout)
    def forward(self, X):
        K = self.W_k(X)
        Q = self.W_q(X)
        V = self.W_v(X)

        K_T = torch.permute(0,2,1)
        scores = torch.matmul(Q,K_T)/torch.sqrt(self.len_feature_new)
        scores = F.softmax(scores, -1)
        scores = self.dropout(scores)
        
        #len_seq x len_feature_new
        attention = torch.matmul(scores, V)
        return attention


        