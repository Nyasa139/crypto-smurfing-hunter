import networkx as nx

def build_graph(tx_df):
    """
    Build a directed transaction graph.
    Nodes   : Wallets
    Edges   : Transactions (with temporal + behavioral features)
    """
    G = nx.DiGraph()

    for _, row in tx_df.iterrows():
        src = row["Source_Wallet_ID"]
        dst = row["Dest_Wallet_ID"]

        G.add_edge(
            src,
            dst,
            amount=float(row["Amount"]),
            timestamp_unix=int(row["timestamp_unix"]),
            token=row["Token_Type"],
            time_delta=float(row["time_delta"]),
            repeat_dest=int(row["repeat_dest"]),
            self_transfer=int(row["self_transfer"]),
            tx_count_10min=int(row["tx_count_10min"]),
            is_small_tx=int(row["is_small_tx"]),
        )

    return G
