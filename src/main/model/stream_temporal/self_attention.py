import torch
from torch import nn 
import torch.nn.functional as F
import math

class SelfAttention(nn.Module):
    def __init__(self, device, len_feature_input, len_feature_new, dropout = 0, **kwargs):

        super(SelfAttention, self).__init__(**kwargs)
        self.len_feature_new = len_feature_new
        self.W_k =nn.Linear(len_feature_input, len_feature_new).to(device)
        self.W_q =nn.Linear(len_feature_input, len_feature_new).to(device)
        self.W_v =nn.Linear(len_feature_input, len_feature_new).to(device)

        self.dropout = nn.Dropout(dropout)
    def forward(self, X):
        K = self.W_k(X)
        Q = self.W_q(X)
        V = self.W_v(X)

        K_T = K.permute(0,2,1)
        scores = torch.matmul(Q,K_T)/math.sqrt(self.len_feature_new)
        scores = F.softmax(scores, -1)
        scores = self.dropout(scores)
        
        #len_seq x len_feature_new
        attention = torch.matmul(scores, V)
        return attention


        