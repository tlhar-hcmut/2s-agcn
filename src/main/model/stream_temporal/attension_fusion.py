from torch import nn
import torch
import torch.nn.functional as F

class AttentionFusion(nn.Module):
    def __init__(self, input_size, dropout, **kwargs):
        super(AttentionFusion, self).__init__(**kwargs)
        self.dropout = nn.Dropout(dropout)
        self.ln = nn.LayerNorm(input_size)

    def forward(self, *X):
        X_out = torch.empty(X[0].size)
        
        for X_ in X:
            X_out+=self.dropout(X_)

        return self.ln(X_out)