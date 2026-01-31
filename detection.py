import networkx as nx

# -----------------------------
# SUSPICION SCORE CALCULATION
# -----------------------------
def calculate_scores(G):
    scores = {}
    reasons = {}

    for node in G.nodes():
        score = 0
        reason = []

        in_deg = G.in_degree(node)
        out_deg = G.out_degree(node)

        # Fan-out (smurf source)
        if out_deg >= 5:
            score += 40
            reason.append("Heavy fan-out")

        # Fan-in (collector)
        if in_deg >= 5:
            score += 40
            reason.append("Heavy fan-in")

        # Self transfers (wash trading)
        self_tx = sum(
            1 for _, _, d in G.out_edges(node, data=True)
            if d.get("self_transfer") == 1
        )
        if self_tx >= 2:
            score += 30
            reason.append("Wash trading")

        # Burst transactions
        burst_tx = sum(
            1 for _, _, d in G.out_edges(node, data=True)
            if d.get("tx_count_10min", 0) >= 3
        )
        if burst_tx >= 2:
            score += 30
            reason.append("Transaction bursts")

        # Small tx smurfing
        small_tx = sum(
            1 for _, _, d in G.out_edges(node, data=True)
            if d.get("is_small_tx") == 1
        )
        if small_tx >= 4:
            score += 30
            reason.append("Smurfing pattern")

        scores[node] = min(score, 100)
        reasons[node] = reason

    return scores, reasons
