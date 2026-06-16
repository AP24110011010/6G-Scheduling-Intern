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

    Positive Ud = defender is winning
    Negative Ud = attacker is winning
    """
    return alpha * D - beta * C


# ─────────────────────────────────────────────
# 2. Attacker Utility Function
# ─────────────────────────────────────────────

def Ua(C, D, gamma=2.0, delta=1.0):
    """
    Attacker's utility function.
    Ua = gamma * C - delta * D

    C     = number of successful compromises
    D     = number of attacks detected (penalty)
    gamma = reward weight for compromise (default 2.0)
    delta = penalty weight for detection (default 1.0)

    Higher Ua = more successful attack
    """
    return gamma * C - delta * D


# ─────────────────────────────────────────────
# 3. Detection Probability (Sigmoid)
# ─────────────────────────────────────────────

def P_detect(Ri, F, theta1=1.0, theta2=0.5):
    """
    Probability of detecting an attack on node i.
    Uses sigmoid function from seniors' paper.

    P_detect = 1 / (1 + e^(-(theta1 * Ri - theta2 * F)))

    Ri     = risk score of the target node (0 to 1)
    F      = defender fatigue factor (0 to 1)
    theta1 = risk sensitivity (default 1.0)
    theta2 = fatigue sensitivity (default 0.5)
    """
    return 1 / (1 + np.exp(-(theta1 * Ri - theta2 * F)))


# ─────────────────────────────────────────────
# 4. Infection Pressure
# ─────────────────────────────────────────────

def IP(V, R, w1=0.5, w2=0.5):
    """
    Infection pressure on a node.
    IP = w1 * V + w2 * R

    V  = vulnerability score of the node (0 to 1)
    R  = current risk score of the node (0 to 1)
    """
    return w1 * V + w2 * R


# ─────────────────────────────────────────────
# 5. Stackelberg Strategy Selection
# ─────────────────────────────────────────────

def strategy_select_stackelberg(G, budget=5):
    """
    Defender picks monitoring set FIRST (Leader move).
    Evaluates attacker's best response to each candidate monitoring set.
    Chooses the set that maximises Ud assuming rational attacker.

    Steps:
    1. Generate candidate monitoring sets from top-12 high-risk nodes
    2. For each candidate set: simulate attacker's best response
    3. Estimate Ud for that outcome
    4. Return the monitoring set with highest Ud

    This is the Stackelberg equilibrium strategy.
    """
    nodes = [n for n in G.nodes() if G.nodes[n]['status'] != 'compromised']

    if len(nodes) <= budget:
        return nodes

    # Candidate pool: top-12 highest-risk nodes (full enumeration too slow for 50 nodes)
    by_risk = sorted(nodes, key=lambda n: G.nodes[n]['risk_score'], reverse=True)
    pool    = by_risk[:12]

    best_set = None
    best_Ud  = -999

    # Evaluate all combinations of size 'budget' from pool
    for mon_set in itertools.combinations(pool, budget):
        mon_set = list(mon_set)

        # Attacker's best response: pick highest-risk UNMONITORED node
        unmonitored = [n for n in nodes if n not in mon_set]
        if not unmonitored:
            continue

        atk_target  = max(unmonitored, key=lambda n: G.nodes[n]['risk_score'])
        risk_target = G.nodes[atk_target]['risk_score']

        # Estimate detection probability
        p_det = P_detect(risk_target, F=0.1)

        # Estimate Ud under this outcome
        est_D  = p_det        # expected detections
        est_C  = 1 - p_det    # expected compromises
        ud_val = Ud(est_D, est_C)

        if ud_val > best_Ud:
            best_Ud  = ud_val
            best_set = mon_set

    return best_set if best_set else by_risk[:budget]


# ─────────────────────────────────────────────
# 6. Nash Strategy Selection
# ─────────────────────────────────────────────

def strategy_select_nash(G, budget=5, max_iter=10):
    """
    Both defender and attacker converge to Nash Equilibrium.
    Uses iterative best response — each player updates strategy
    based on the other's last move until no change occurs.

    Nash condition: Ui(s*i, s*j) >= Ui(si, s*j) for both players.
    Neither can improve by changing strategy alone.

    Steps:
    1. Start with defender monitoring top-budget risk nodes
    2. Attacker best response: pick highest-risk unmonitored node
    3. Defender best response: shift monitoring toward attacker's target
    4. Repeat until strategies stabilise (equilibrium reached)
    """
    nodes = [n for n in G.nodes() if G.nodes[n]['status'] != 'compromised']

    if len(nodes) <= budget:
        return nodes

    # Initial defender strategy: highest-risk nodes
    by_risk = sorted(nodes, key=lambda n: G.nodes[n]['risk_score'], reverse=True)
    mon_set = by_risk[:budget]

    for iteration in range(max_iter):
        # Attacker best response to current defender strategy
        unmonitored = [n for n in nodes if n not in mon_set]
        if not unmonitored:
            break
        atk_target = max(unmonitored, key=lambda n: G.nodes[n]['risk_score'])

        # Defender best response: include attacker's likely target, re-rank
        new_set = sorted(
            nodes,
            key=lambda n: (
                G.nodes[n]['risk_score'] + (0.3 if n == atk_target else 0.0)
            ),
            reverse=True
        )[:budget]

        # Check convergence
        if set(new_set) == set(mon_set):
            break   # Nash equilibrium reached

        mon_set = new_set

    return mon_set


# ─────────────────────────────────────────────
# Run Tests
# ─────────────────────────────────────────────

if __name__ == '__main__':

    print("=" * 55)
    print("  Payoff Engine Tests — Week 3 (Updated)")
    print("=" * 55)

    # Basic function tests
    print("\n  Ud / Ua Tests:")
    for D, C in [(5,0),(3,2),(0,5)]:
        print(f"  D={D} C={C} -> Ud={Ud(D,C):.2f}  Ua={Ua(C,D):.2f}")

    print("\n  P_detect Tests:")
    for Ri in [0.2, 0.5, 0.8]:
        print(f"  Ri={Ri}  F=0.1 -> P_detect={P_detect(Ri, 0.1):.3f}")

    # Strategy selection tests on a small test graph
    print("\n  Strategy Selection Tests (10-node test network):")
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

    print(f"  Stackelberg monitors: {stack_set}")
    print(f"  Nash monitors       : {nash_set}")
    print(f"  Same set?           : {set(stack_set) == set(nash_set)}")
    print("\n  Note: Stackelberg anticipates attacker move.")
    print("  Nash converges to equilibrium without anticipation.")
    print("=" * 55)
