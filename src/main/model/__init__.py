from .stream_spatial import *
from .stream_temporal import *


class TKNet(nn.Module):
    def __init__(
        self,
        input_size=(3, 300, 25, 2),
        num_class=60,
        cls_graph=None,
        graph_args=dict(),
    ):
        super(TKNet, self).__init__()

        if cls_graph is None:
            raise ValueError()
        else:
            self.graph = cls_graph(**graph_args)

        
        self.stream_spatial = StreamSpatialGCN(input_size=input_size, cls_graph=cls_graph)
        
        self.stream_temporal = StreamTemporalGCN(input_size=input_size, cls_graph=cls_graph)

        num_unit_spatial = 64
        num_unit_temporal = 300

        self.fc1 = nn.Linear(num_unit_spatial+num_unit_temporal, (num_unit_spatial+num_unit_temporal)//2)
        
        self.fc2 = nn.Linear((num_unit_spatial+num_unit_temporal)//2, num_class)

    def forward(self, x):
        output_stream_spatial = self.stream_spatial(x)
        output_stream_temporal = self.stream_temporal(x)
        output_concat = torch.cat((output_stream_spatial, output_stream_temporal), dim=1)
        return self.fc2(self.fc1(output_concat))
