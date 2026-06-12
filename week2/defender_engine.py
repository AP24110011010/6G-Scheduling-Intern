# defender_engine.py
# Week 2 - Defender Engine: Betweenness-Guided Monitoring
# Topic: Graph Theory applied to Network Defence Strategy
# Summer Research Internship 2025 - Group 4

import networkx as nx

# ─────────────────────────────────────────────
# 1. Select Nodes to Monitor
# ─────────────────────────────────────────────

def get_monitored_nodes(G, k=5):
    """
    Returns top-k nodes ranked by betweenness centrality.
    These are the most critical relay nodes in the network.
    High betweenness = if compromised, disrupts most paths.
    """
    between_c = nx.betweenness_centrality(G)
    top_k     = sorted(between_c, key=between_c.get, reverse=True)[:k]
    return top_k

# ─────────────────────────────────────────────
# 2. Monitor and Detect
# ─────────────────────────────────────────────

def monitor_node(G, attack_log, monitored_nodes, prev_risks):
    """
    Checks monitored nodes for risk increases since last round.
    If risk increased by more than threshold -> DETECTED.
    Applies partial risk recovery to detected nodes.
    Updates the attack log entry with detected=True if caught.
    """
    if attack_log is None:
        return False

    entries      = attack_log if isinstance(attack_log, list) else [attack_log]
    detected_any = False
    threshold    = 0.10

    for entry in entries:
        node = entry['target']
        if node in monitored_nodes:
            prev = prev_risks.get(node, 0.0)
            curr = G.nodes[node]['risk_score']
            if curr > prev + threshold:
                entry['detected']         = True
                G.nodes[node]['risk_score'] = max(0.1, curr - 0.15)
                detected_any              = True

    return detected_any

# ─────────────────────────────────────────────
# 3. Network Statistics per Round
# ─────────────────────────────────────────────

def network_stats(G, t):
    """
    Computes network-wide security metrics for the current round.
    Returns a dict used for logging and plotting.
    """
    total    = G.number_of_nodes()
    comp     = sum(1 for n in G.nodes() if G.nodes[n]['status'] == 'compromised')
    avg_risk = sum(G.nodes[n]['risk_score'] for n in G.nodes()) / total

    return {
        'time':              t,
        'compromised':       comp,
        'compromised_ratio': round(comp / total, 4),
        'avg_risk':          round(avg_risk, 4),
    }
