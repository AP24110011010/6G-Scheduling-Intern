# nash_defender.py
# Week 3 - Nash Defender Engine
# Topic: Simultaneous Decision Making, Nash Equilibrium
# Summer Research Internship 2025 - Group 4

import sys
import os
import random
import networkx as nx

sys.path.insert(0, os.path.dirname(__file__))
from payoff_engine import strategy_select_nash, P_detect, Ud, Ua


def nash_step(G, t, prev_risks, budget=5, fatigue=0.1):
    """
    Runs one round of Nash equilibrium game simulation.

    Both defender and attacker reach equilibrium through
    iterative best response — neither anticipates the other's
    move in advance, unlike Stackelberg.

    Returns a log dict in the SAME format as stackelberg_step()
    for fair side-by-side comparison.
    """

    # Step 1: Nash equilibrium monitoring set (simultaneous decision)
    mon_set = strategy_select_nash(G, budget)

    # Step 2: Attacker picks a target using the same realistic risk +
    # centrality weighted model as in the Stackelberg scenario (the
    # attacker's real-world behaviour doesn't change based on which
    # defence strategy is used — only the defender's anticipation does).
    candidates = [n for n in G.nodes() if G.nodes[n]['status'] != 'compromised']
    if not candidates:
        candidates = list(G.nodes())

    between_c = nx.betweenness_centrality(G)
    max_cent  = max(between_c.values()) if between_c else 1.0
    max_cent  = max_cent if max_cent > 0 else 1.0

    weights = [
        (0.55 * (G.nodes[n]['risk_score'] ** 2) +
         0.45 * (between_c.get(n, 0) / max_cent))
        for n in candidates
    ]
    total_w = sum(weights)
    if total_w == 0:
        atk_target = random.choice(candidates)
    else:
        probs = [w / total_w for w in weights]
        atk_target = random.choices(candidates, weights=probs, k=1)[0]

    # Step 3: Apply attack
    risk_before = G.nodes[atk_target]['risk_score']
    increase    = round(random.uniform(0.2, 0.35), 2)
    risk_after  = min(1.0, risk_before + increase)
    G.nodes[atk_target]['risk_score'] = risk_after
    compromised = risk_after >= 0.85
    if compromised:
        G.nodes[atk_target]['status'] = 'compromised'

    # Step 4: Defender detects if target was in the Nash monitoring set
    detected = False
    if atk_target in mon_set:
        p = P_detect(risk_after, fatigue)
        detected = random.random() < p
        if detected:
            G.nodes[atk_target]['risk_score'] = max(0.1, risk_after - 0.15)
            if G.nodes[atk_target]['risk_score'] < 0.85:
                G.nodes[atk_target]['status'] = 'normal'

    # Step 5: Compute network-wide stats
    total = G.number_of_nodes()
    comp  = sum(1 for n in G.nodes() if G.nodes[n]['status'] == 'compromised')
    ar    = sum(G.nodes[n]['risk_score'] for n in G.nodes()) / total

    return {
        'time':              t,
        'strategy':          'Nash',
        'target':            atk_target,
        'monitored':         mon_set,
        'detected':          detected,
        'compromised_node':  compromised,
        'compromised_ratio': round(comp / total, 4),
        'avg_risk':          round(ar, 4),
        'Ud_val':            round(Ud(1 if detected else 0, 1 if compromised else 0), 3),
        'Ua_val':            round(Ua(1 if compromised else 0, 1 if detected else 0), 3),
    }


# ─────────────────────────────────────────────
# Quick standalone test — 20 rounds
# ─────────────────────────────────────────────

if __name__ == '__main__':
    from iot_network import create_iot_network

    random.seed(1)
    G = create_iot_network(50, seed=1)
    prev_risks = {n: G.nodes[n]['risk_score'] for n in G.nodes()}

    print("=" * 55)
    print("  Nash Defender — 20-Round Test")
    print("=" * 55)

    detected_count = 0
    for t in range(20):
        log = nash_step(G, t, prev_risks)
        prev_risks = {n: G.nodes[n]['risk_score'] for n in G.nodes()}
        if log['detected']:
            detected_count += 1
        print(f"  [t={t:>3}] Target={log['target']:10s} "
              f"Detected={str(log['detected']):5s} "
              f"CR={log['compromised_ratio']:.3f} AR={log['avg_risk']:.3f}")

    print("=" * 55)
    print(f"  Detection Rate over 20 rounds: {detected_count/20*100:.1f}%")
    print("=" * 55)
