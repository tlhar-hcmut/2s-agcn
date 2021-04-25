import torch
from torch import nn

from .add_norm import AddNorm
from .encoder_block import EncoderBlock
from .multi_head_attention import MultiHeadAttention
from .position import PositionalEncoding
from .position_wise_ffn import PositionWiseFFN
from .self_attention import SelfAttention
from .transformer import TransformerEncoder


class StreamTemporalGCN(torch.nn.Module):
    def __init__(
        self, num_joint: int, num_channel: int,
    ):
        super(StreamTemporalGCN, self).__init__()

        input_size = (num_joint * num_channel, num_joint * num_channel)
        # input: N, C, T, V
        self.conv1 = nn.Conv2d(
            in_channels=3,
            out_channels=3,
            kernel_size=(4, 1),
            stride=(4, 1),
            padding=(0, 0),  # poolling and equal padding
            dilation=1,
            groups=1,
            bias=True,
            padding_mode="zeros",  # 'zeros', 'reflect', 'replicate', 'circular'
        )  # 3, 300, 25 -> 3, 150, 25

        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # N, 300, 128
        self.transformer = TransformerEncoder(
            device, input_size=input_size, len_seq=input_size[-1]
        )

        self.conv2 = nn.Conv2d(
            in_channels=1,
            out_channels=1,
            kernel_size=(2, 4),
            stride=(2, 4),
            padding=(0, 0),
            dilation=1,
            groups=1,
            bias=True,
            padding_mode="zeros",  # 'zeros', 'reflect', 'replicate', 'circular'
        )

    def forward(self, x):
        # stream transformer
        N_0, C, T, V, M_0 = x.size()

        # -> N-T, C, V
        stream_transformer = (
            x.permute(0, 4, 2, 1, 3).contiguous().view(N_0 * M_0, T, C, V)
        )

        # N T, C , V => N C, T, V
        stream_transformer = stream_transformer.permute(0, 2, 1, 3)

        # N, 3, 300, 25 ->N, 3, 150, 25
        stream_transformer = self.conv1(stream_transformer)

        # N C, T, V => N T, C , V
        stream_transformer = stream_transformer.permute(0, 2, 1, 3)

        N, T, C, V = stream_transformer.size()

        # N, 150, 3, 25  -> N, 150, 75
        stream_transformer = stream_transformer.contiguous().view(N, T, C * V)
        # N, 150, 75  -> N, 150, 128
        stream_transformer = self.transformer(stream_transformer)

        # N, 150, 128 -> N, 75, 32
        stream_transformer = stream_transformer.unsqueeze(1)
        stream_transformer = self.conv2(stream_transformer).squeeze()

        # N, 75, 32 -> N, 75
        stream_transformer = torch.mean(stream_transformer, dim=-1)

        stream_transformer = stream_transformer.view(N_0, M_0, 37)
        stream_transformer = stream_transformer.mean(1)

        return stream_transformer
