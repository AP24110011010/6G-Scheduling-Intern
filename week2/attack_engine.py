# attack_engine.py
# Week 2 - Attack Engine: Random, Targeted, Burst
# Topic: IoT Security Simulation — Attack Modes with CSV Logging
# Summer Research Internship 2025 - Group 4

import random
import csv
import os

random.seed(None)
os.makedirs('results', exist_ok=True)

# ─────────────────────────────────────────────
# Core Attack Logic
# ─────────────────────────────────────────────

def _apply_attack(G, node, attack_type, t):
    """
    Applies an attack to a single node.
    Increases risk score and marks node as compromised if risk >= 0.85.
    Returns a log dictionary for CSV recording.
    """
    risk_before = G.nodes[node]['risk_score']
    increase    = round(random.uniform(0.2, 0.4), 2)
    risk_after  = min(1.0, risk_before + increase)

    G.nodes[node]['risk_score'] = risk_after

    compromised = risk_after >= 0.85
    if compromised:
        G.nodes[node]['status'] = 'compromised'

    return {
        'time':        t,
        'target':      node,
        'attack_type': attack_type,
        'risk_before': risk_before,
        'risk_after':  risk_after,
        'compromised': compromised,
        'detected':    False,
    }

# ─────────────────────────────────────────────
# Attack Mode 1: Random
# ─────────────────────────────────────────────

def attack_random(G, t):
    """
    Selects a random non-compromised node and attacks it.
    Simulates an untargeted attacker with no network knowledge.
    """
    candidates = [n for n in G.nodes() if G.nodes[n]['status'] != 'compromised']
    if not candidates:
        return None
    target = random.choice(candidates)
    return _apply_attack(G, target, 'Random', t)

# ─────────────────────────────────────────────
# Attack Mode 2: Targeted
# ─────────────────────────────────────────────

def attack_targeted(G, t):
    """
    Selects the non-compromised node with the HIGHEST risk score.
    Simulates an intelligent attacker who has done Reconnaissance first.
    """
    candidates = {
        n: G.nodes[n]['risk_score']
        for n in G.nodes()
        if G.nodes[n]['status'] != 'compromised'
    }
    if not candidates:
        return None
    target = max(candidates, key=candidates.get)
    return _apply_attack(G, target, 'Targeted', t)

# ─────────────────────────────────────────────
# Attack Mode 3: Burst
# ─────────────────────────────────────────────

def attack_burst(G, t, n=5):
    """
    Simultaneously attacks n random non-compromised nodes in one time step.
    Simulates a botnet or coordinated DDoS-style attack.
    """
    candidates = [n for n in G.nodes() if G.nodes[n]['status'] != 'compromised']
    targets    = random.sample(candidates, min(n, len(candidates)))
    return [_apply_attack(G, target, 'Burst', t) for target in targets]

# ─────────────────────────────────────────────
# Save Logs to CSV
# ─────────────────────────────────────────────

def save_logs(all_logs, path='results/attack_logs.csv'):
    """
    Flattens all attack log entries (including Burst lists) and saves to CSV.
    """
    flat = []
    for entry in all_logs:
        if isinstance(entry, list):
            flat.extend([e for e in entry if e])
        elif entry:
            flat.append(entry)

    if not flat:
        print("No logs to save.")
        return flat

    with open(path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=flat[0].keys())
        writer.writeheader()
        writer.writerows(flat)

    print(f"Saved {len(flat)} attack log entries to {path}")
    return flat

# ─────────────────────────────────────────────
# Quick Test (run standalone)
# ─────────────────────────────────────────────

if __name__ == '__main__':
    import sys, os
    sys.path.insert(0, os.path.dirname(__file__))
    from iot_network import create_iot_network

    G = create_iot_network(50)
    logs = []

    print("Running 10 rounds of each attack mode...\n")

    for t in range(10):
        logs.append(attack_random(G, t))

    for t in range(10, 20):
        logs.append(attack_targeted(G, t))

    for t in range(20, 30):
        logs.append(attack_burst(G, t, n=5))

    flat = save_logs(logs)

    compromised = sum(1 for e in flat if e.get('compromised'))
    print(f"\nTotal attacks logged : {len(flat)}")
    print(f"Total compromised    : {compromised}")
    print(f"Compromise ratio     : {compromised/G.number_of_nodes()*100:.1f}%")
