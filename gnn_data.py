import torch
from torch_geometric.data import Data
import networkx as nx

def graph_to_pyg(G):
    node_map = {n: i for i, n in enumerate(G.nodes())}

    edge_index = []
    edge_attr = []

    for u, v, data in G.edges(data=True):
        edge_index.append([node_map[u], node_map[v]])
        edge_attr.append([data["amount"]])

    edge_index = torch.tensor(edge_index, dtype=torch.long).t().contiguous()
    edge_attr = torch.tensor(edge_attr, dtype=torch.float)

    # node features: [in_degree, out_degree]
    x = []
    for node in G.nodes():
        x.append([G.in_degree(node), G.out_degree(node)])

    x = torch.tensor(x, dtype=torch.float)

    return Data(x=x, edge_index=edge_index, edge_attr=edge_attr)
