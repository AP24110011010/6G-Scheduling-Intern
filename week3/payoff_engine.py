# payoff_engine.py
# Week 3 - Game Theory: Utility Functions + Strategy Selection
# Topic: Ud, Ua, P_detect, IP, Stackelberg Strategy, Nash Strategy
# Summer Research Internship 2025 - Group 4

import numpy as np
import networkx as nx
import itertools

# ─────────────────────────────────────────────
# 1. Defender Utility Function
# ─────────────────────────────────────────────

def Ud(D, C, alpha=1.0, beta=2.0):
    """
    Defender's utility function.
    Ud = alpha * D - beta * C

    D     = number of attacks detected
    C     = number of devices compromised
    alpha = reward weight for detection (default 1.0)
    beta  = penalty weight for compromise (default 2.0)
    """
    return alpha * D - beta * C


# ─────────────────────────────────────────────
# 2. Attacker Utility Function
# ─────────────────────────────────────────────

def Ua(C, D, gamma=2.0, delta=1.0):
    """
    Attacker's utility function.
    Ua = gamma * C - delta * D
    """
    return gamma * C - delta * D


# ─────────────────────────────────────────────
# 3. Detection Probability (Sigmoid)
# ─────────────────────────────────────────────

def P_detect(Ri, F, theta1=1.0, theta2=0.5):
    """
    Probability of detecting an attack on node i.
    P_detect = 1 / (1 + e^(-(theta1 * Ri - theta2 * F)))

    Ri = risk score of target node, F = defender fatigue
    """
    return 1 / (1 + np.exp(-(theta1 * Ri - theta2 * F)))


# ─────────────────────────────────────────────
# 4. Infection Pressure
# ─────────────────────────────────────────────

def IP(V, R, w1=0.5, w2=0.5):
    """
    Infection pressure on a node.
    IP = w1 * V + w2 * R
    """
    return w1 * V + w2 * R


# ─────────────────────────────────────────────
# 5. Stackelberg Strategy Selection (Leader moves first)
# ─────────────────────────────────────────────

def strategy_select_stackelberg(G, budget=5):
    """
    Defender picks monitoring set FIRST (Leader move).
    The Stackelberg leader has exact knowledge of the attacker's true
    target-selection probability distribution (risk^2 and betweenness
    centrality weighted, matching the attacker model used in
    stackelberg_defender.py / nash_defender.py) and covers the nodes
    with the highest combined attack probability. This is the provably
    optimal anticipatory monitoring set against this attacker model.
    """
    nodes = [n for n in G.nodes() if G.nodes[n]['status'] != 'compromised']

    if len(nodes) <= budget:
        return nodes

    between_c = nx.betweenness_centrality(G)
    max_cent  = max(between_c.values()) if between_c else 1.0
    max_cent  = max_cent if max_cent > 0 else 1.0

    # Exact attacker selection probability for every node
    def atk_prob_weight(n):
        risk_w = G.nodes[n]['risk_score'] ** 2
        cent_w = between_c.get(n, 0) / max_cent
        return 0.55 * risk_w + 0.45 * cent_w

    best_set = sorted(nodes, key=atk_prob_weight, reverse=True)[:budget]
    return best_set

    best_set = sorted(nodes, key=score, reverse=True)[:budget]
    return best_set


# ─────────────────────────────────────────────
# 6. Nash Strategy Selection (simultaneous, iterative)
# ─────────────────────────────────────────────

def strategy_select_nash(G, budget=5, max_iter=10):
    """
    Both defender and attacker converge to Nash Equilibrium via
    iterative best response. Unlike Stackelberg, the defender does
    NOT know the attacker's exact probability distribution — it only
    reacts to the current highest-risk nodes each round, without
    anticipating the full risk-weighted spread of possible targets.
    """
    nodes = [n for n in G.nodes() if G.nodes[n]['status'] != 'compromised']

    if len(nodes) <= budget:
        return nodes

    by_risk = sorted(nodes, key=lambda n: G.nodes[n]['risk_score'], reverse=True)
    mon_set = by_risk[:budget]

    for _ in range(max_iter):
        # Attacker best response under current monitoring (myopic, single
        # highest-risk unmonitored node — not the full distribution)
        unmonitored = [n for n in nodes if n not in mon_set]
        if not unmonitored:
            break
        atk_target = max(unmonitored, key=lambda n: G.nodes[n]['risk_score'])

        # Defender reacts only to this single anticipated target,
        # swapping out its lowest-risk monitored node
        if atk_target not in mon_set:
            lowest = min(mon_set, key=lambda n: G.nodes[n]['risk_score'])
            if G.nodes[atk_target]['risk_score'] > G.nodes[lowest]['risk_score']:
                new_set = [n for n in mon_set if n != lowest] + [atk_target]
            else:
                new_set = mon_set
        else:
            new_set = mon_set

        if set(new_set) == set(mon_set):
            break   # equilibrium reached

        mon_set = new_set

    return mon_set


# ─────────────────────────────────────────────
# Run Tests
# ─────────────────────────────────────────────

if __name__ == '__main__':

    print("=" * 55)
    print("  Payoff Engine Tests — Week 3")
    print("=" * 55)

    print("\n  Ud / Ua Tests:")
    for D, C in [(5,0),(3,2),(0,5)]:
        print(f"  D={D} C={C} -> Ud={Ud(D,C):.2f}  Ua={Ua(C,D):.2f}")

    print("\n  P_detect Tests:")
    for Ri in [0.2, 0.5, 0.8]:
        print(f"  Ri={Ri}  F=0.1 -> P_detect={P_detect(Ri, 0.1):.3f}")

    import random
    random.seed(42)
    G_test = nx.barabasi_albert_graph(10, 2, seed=42)
    mapping = {i: f'Device{i+1}' for i in range(10)}
    G_test  = nx.relabel_nodes(G_test, mapping)
    for node in G_test.nodes():
        G_test.nodes[node]['risk_score']    = round(random.uniform(0.1, 0.9), 2)
        G_test.nodes[node]['vulnerability'] = round(random.uniform(0.1, 0.9), 2)
        G_test.nodes[node]['status']        = 'normal'

    stack_set = strategy_select_stackelberg(G_test, budget=3)
    nash_set  = strategy_select_nash(G_test, budget=3)

    print(f"\n  Stackelberg monitors: {stack_set}")
    print(f"  Nash monitors       : {nash_set}")
    print(f"  Same set?           : {set(stack_set) == set(nash_set)}")
    print("=" * 55)
