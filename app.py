import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx

from graph_utils import build_graph
from detection import calculate_scores

# -----------------------------
# LOAD DATA
# -----------------------------
df = pd.read_csv("data.csv")
df["Timestamp"] = pd.to_datetime(df["Timestamp"])

# -----------------------------
# BUILD GRAPH
# -----------------------------
G = build_graph(df)
print("Nodes:", G.number_of_nodes())
print("Edges:", G.number_of_edges())

# -----------------------------
# DETECT & SCORE
# -----------------------------
scores, reasons = calculate_scores(G)

# -----------------------------
# PRINT SUSPICIOUS WALLETS
# -----------------------------
result = []
for wallet, score in scores.items():
    if score > 0:
        result.append((wallet, score, reasons[wallet]))

result.sort(key=lambda x: x[1], reverse=True)

print("\nSuspicious Wallets:")
for r in result:
    print(r)

# -----------------------------
# GRAPH VISUALIZATION
# -----------------------------
colors = []
for node in G.nodes():
    if scores[node] >= 70:
        colors.append("red")
    elif scores[node] >= 40:
        colors.append("orange")
    else:
        colors.append("green")

plt.figure(figsize=(12, 8))
nx.draw(
    G,
    with_labels=True,
    node_color=colors,
    node_size=800,
    font_size=8
)
plt.show()
import pandas as pd

rows = []

for wallet in scores:
    rows.append({
        "Wallet_ID": wallet,
        "Suspicion_Score": scores[wallet],
        "Risk_Level": (
            "High" if scores[wallet] >= 70 else
            "Medium" if scores[wallet] >= 40 else
            "Low"
        ),
        "Reason": ", ".join(reasons[wallet]) if reasons[wallet] else "Normal behavior"
    })

score_df = pd.DataFrame(rows)

# Sort by highest risk
score_df = score_df.sort_values(by="Suspicion_Score", ascending=False)

print(score_df.head(10))
# EXPORT RESULTS
score_df.to_csv("suspicion_scores.csv", index=False)
print("Suspicion scores exported to suspicion_scores.csv")
