import os
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx

from graph_utils import build_graph
from detection import calculate_scores

# =============================
# SETUP
# =============================
os.makedirs("outputs", exist_ok=True)

# =============================
# LOAD DATA
# =============================
df = pd.read_csv("data.csv")
df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")

print("Total transactions:", len(df))
print(
    "Unique wallets:",
    len(set(df["Source_Wallet_ID"]).union(set(df["Dest_Wallet_ID"])))
)

# =============================
# BUILD GRAPH
# =============================
G = build_graph(df)
print("Graph nodes:", G.number_of_nodes())
print("Graph edges:", G.number_of_edges())

# =============================
# HEURISTIC DETECTION
# =============================
scores, reasons = calculate_scores(G)

# attach scores to graph (IMPORTANT)
nx.set_node_attributes(G, scores, "suspicion_score")

# =============================
# EXPORT SUSPICION SCORES
# =============================
rows = []

for wallet in G.nodes():
    score = float(scores.get(wallet, 0))
    reason_list = reasons.get(wallet, [])

    if score >= 70:
        level = "High"
    elif score >= 40:
        level = "Medium"
    else:
        level = "Low"

    rows.append({
        "Wallet_ID": wallet,
        "Suspicion_Score": score,
        "Risk_Level": level,
        "Reason": ", ".join(reason_list) if reason_list else "Normal behavior"
    })

score_df = pd.DataFrame(rows).sort_values(
    "Suspicion_Score", ascending=False
)

score_df.to_csv("outputs/suspicion_scores.csv", index=False)
print("✅ Exported outputs/suspicion_scores.csv")

# =============================
# GRAPH VISUALIZATION
# =============================
node_colors = []
node_sizes = []

for n in G.nodes():
    s = scores.get(n, 0)

    if s >= 70:
        node_colors.append("red")
    elif s >= 40:
        node_colors.append("orange")
    else:
        node_colors.append("green")

    node_sizes.append(300 + s * 8)

plt.figure(figsize=(14, 10))
pos = nx.spring_layout(G, seed=42, k=0.6)

nx.draw(
    G,
    pos,
    node_color=node_colors,
    node_size=node_sizes,
    edge_color="gray",
    alpha=0.8,
    with_labels=False
)

plt.title("Wallet Transaction Graph\n(Red = High Risk, Orange = Medium)")
plt.axis("off")
plt.show()

# =============================
# WALLET SUMMARY (FOR REPORT)
# =============================
wallet_summary = []

for wallet in G.nodes():
    incoming = df[df["Dest_Wallet_ID"] == wallet]
    outgoing = df[df["Source_Wallet_ID"] == wallet]

    wallet_summary.append({
        "Wallet_ID": wallet,
        "Incoming_Tx_Count": len(incoming),
        "Outgoing_Tx_Count": len(outgoing),
        "Total_Received": incoming["Amount"].sum(),
        "Total_Sent": outgoing["Amount"].sum(),
        "Net_Flow": incoming["Amount"].sum() - outgoing["Amount"].sum(),
        "Unique_Senders": incoming["Source_Wallet_ID"].nunique(),
        "Unique_Receivers": outgoing["Dest_Wallet_ID"].nunique(),
        "Suspicion_Score": scores.get(wallet, 0),
        "Risk_Level": (
            "High" if scores.get(wallet, 0) >= 70 else
            "Medium" if scores.get(wallet, 0) >= 40 else
            "Low"
        ),
        "Reason": ", ".join(reasons.get(wallet, []))
    })

summary_df = pd.DataFrame(wallet_summary).sort_values(
    "Suspicion_Score", ascending=False
)

summary_df.to_csv("outputs/wallet_summary.csv", index=False)
print("✅ Exported outputs/wallet_summary.csv")

# =============================
# OPTIONAL: GNN (KEEP DISABLED FOR SUBMISSION)
# =============================

from gnn_data import graph_to_pyg
from gnn_model import WalletGNN
from train_gnn import train

data = graph_to_pyg(G)
model = WalletGNN()
gnn_scores = train(model, data)

gnn_wallet_scores = {
    wallet: float(gnn_scores[i])
    for i, wallet in enumerate(G.nodes())
}

print("GNN scores (sample):", list(gnn_wallet_scores.items())[:5])

