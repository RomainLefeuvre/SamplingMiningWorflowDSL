import grpc

from google.protobuf.field_mask_pb2 import FieldMask

import swh.graph.grpc.swhgraph_pb2 as swhgraph
import swh.graph.grpc.swhgraph_pb2_grpc as swhgraph_grpc

GRAPH_GRPC_SERVER = "localhost:50091"

with grpc.insecure_channel(GRAPH_GRPC_SERVER) as channel:
    stub = swhgraph_grpc.TraversalServiceStub(channel)
    swhid = "swh:1:cnt:0000000000000000000000000000000000000001"
    response = stub.GetNode(swhgraph.GetNodeRequest(swhid=swhid))
    print(response)


