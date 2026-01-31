import networkx as nx

def build_graph(df):
    G = nx.DiGraph()

    for _, row in df.iterrows():
        G.add_edge(
            row["Source_Wallet_ID"],
            row["Dest_Wallet_ID"],
            amount=row["Amount"],
            timestamp=row["Timestamp"],
            token=row["Token_Type"]
        )
    return G
