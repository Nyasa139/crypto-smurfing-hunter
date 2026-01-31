import pandas as pd

df = pd.read_csv("data.csv")

# -----------------------------
# WALLET-LEVEL AGGREGATION
# -----------------------------
wallets = set(df["Source_Wallet_ID"]).union(set(df["Dest_Wallet_ID"]))

rows = []

for w in wallets:
    outgoing = df[df["Source_Wallet_ID"] == w]
    incoming = df[df["Dest_Wallet_ID"] == w]

    tx_sent = len(outgoing)
    tx_received = len(incoming)

    small_tx_ratio = outgoing["is_small_tx"].mean() if tx_sent > 0 else 0
    burst_tx = outgoing["tx_count_10min"].max() if tx_sent > 0 else 0
    repeat_dest = outgoing["repeat_dest"].sum()
    self_tx = outgoing["self_transfer"].sum()

    # -----------------------------
    # RISK SCORE
    # -----------------------------
    score = 0
    score += small_tx_ratio * 30
    score += min(burst_tx, 10) * 3
    score += repeat_dest * 2
    score += self_tx * 10

    if tx_sent >= 5 and small_tx_ratio > 0.6:
        score += 20   # smurfing
    if tx_received >= 5 and tx_sent <= 1:
        score += 15   # fan-in mule

    score = min(round(score, 1), 100)

    # -----------------------------
    # COLOR LABEL
    # -----------------------------
    if score >= 70:
        color = "RED"
    elif score >= 40:
        color = "YELLOW"
    else:
        color = "GREEN"

    rows.append({
        "Wallet_ID": w,
        "Tx_Sent": tx_sent,
        "Tx_Received": tx_received,
        "Risk_Score": score,
        "Risk_Color": color
    })

wallet_df = pd.DataFrame(rows)
wallet_df.to_csv("wallet_risk_labeled.csv", index=False)

print(wallet_df["Risk_Color"].value_counts())
