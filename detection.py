import networkx as nx
from collections import defaultdict
from datetime import timedelta

# -----------------------------
# PEELING CHAIN DETECTION
# -----------------------------
def detect_peeling_chain(G):
    """
    Peeling chain:
    - exactly 1 incoming edge
    - exactly 1 outgoing edge
    """
    peeling_wallets = set()

    for node in G.nodes():
        if G.in_degree(node) == 1 and G.out_degree(node) == 1:
            peeling_wallets.add(node)

    return peeling_wallets


# -----------------------------
# FAN-IN DETECTION
# -----------------------------
def detect_fan_in(G, threshold=3):
    """
    Fan-in:
    - many wallets send to one wallet
    """
    fan_in_wallets = set()

    for node in G.nodes():
        if G.in_degree(node) >= threshold:
            fan_in_wallets.add(node)

    return fan_in_wallets


# -----------------------------
# FAN-OUT DETECTION
# -----------------------------
def detect_fan_out(G, threshold=3):
    """
    Fan-out:
    - one wallet sends to many wallets
    """
    fan_out_wallets = set()

    for node in G.nodes():
        if G.out_degree(node) >= threshold:
            fan_out_wallets.add(node)

    return fan_out_wallets


# -----------------------------
# FAST TRANSFER DETECTION
# -----------------------------
def detect_fast_transfers(G, time_limit_minutes=60):
    """
    Detect wallets involved in fast consecutive transfers
    """
    fast_wallets = set()

    for node in G.nodes():
        timestamps = []

        for _, _, data in G.out_edges(node, data=True):
            timestamps.append(data["timestamp"])

        timestamps.sort()

        for i in range(1, len(timestamps)):
            if timestamps[i] - timestamps[i - 1] <= timedelta(minutes=time_limit_minutes):
                fast_wallets.add(node)
                break

    return fast_wallets


# -----------------------------
# SUSPICION SCORE CALCULATION
# -----------------------------
def calculate_scores(G):
    """
    Assign suspicion scores to wallets based on detected patterns
    """

    scores = {node: 0 for node in G.nodes()}
    reasons = defaultdict(list)

    peeling = detect_peeling_chain(G)
    fan_in = detect_fan_in(G)
    fan_out = detect_fan_out(G)
    fast = detect_fast_transfers(G)

    for node in peeling:
        scores[node] += 40
        reasons[node].append("Peeling chain detected")

    for node in fan_in:
        scores[node] += 30
        reasons[node].append("Fan-in pattern detected")

    for node in fan_out:
        scores[node] += 30
        reasons[node].append("Fan-out pattern detected")

    for node in fast:
        scores[node] += 20
        reasons[node].append("Fast consecutive transfers")

    # Cap scores at 100
    for node in scores:
        scores[node] = min(scores[node], 100)

    return scores, reasons
