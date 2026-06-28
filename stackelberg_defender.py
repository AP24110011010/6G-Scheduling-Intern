"""
stackelberg_defender.py
Week 4 — Stackelberg Defender Model (Refined)
Group 4 | Event-Driven 6G Scheduling using SimPy + Sionna
"""

import simpy
import random
import csv
import os

random.seed(42)

# --- Payoff Parameters ---
DEFENDER_DETECTION_REWARD = 10.0
DEFENDER_MISS_PENALTY = -5.0
RESOURCE_COST = 2.0
ATTACKER_SUCCESS_REWARD = 8.0
ATTACKER_FAIL_PENALTY = -3.0

NUM_NODES = 10
SIM_RUNS = 20


def attacker_best_response(defender_coverage: float) -> float:
    """Attacker picks attack probability inversely proportional to defender coverage."""
    return max(0.1, 1.0 - defender_coverage)


def stackelberg_defender_strategy(num_nodes: int) -> float:
    """
    Stackelberg leader: choose coverage anticipating attacker's best response.
    Maximizes defender payoff over attacker's reaction function.
    """
    best_coverage = 0.0
    best_payoff = float('-inf')

    for coverage_pct in [i / 10 for i in range(1, 11)]:
        attack_prob = attacker_best_response(coverage_pct)
        detection_rate = coverage_pct * 0.9
        payoff = (
            detection_rate * DEFENDER_DETECTION_REWARD
            - (1 - detection_rate) * attack_prob * abs(DEFENDER_MISS_PENALTY)
            - coverage_pct * RESOURCE_COST
        )
        if payoff > best_payoff:
            best_payoff = payoff
            best_coverage = coverage_pct

    return best_coverage


def node_process(env, node_id, coverage, results):
    """SimPy process: each node faces an attack event."""
    yield env.timeout(random.uniform(1, 5))

    attack_prob = attacker_best_response(coverage)
    attacked = random.random() < attack_prob

    if attacked:
        detected = random.random() < (coverage * 0.9)
        compromised = not detected
    else:
        detected = False
        compromised = False

    risk_score = 0.0 if not attacked else (0.1 if detected else 0.8)

    results.append({
        'node_id': node_id,
        'attacked': int(attacked),
        'detected': int(detected),
        'compromised': int(compromised),
        'risk_score': round(risk_score, 2),
        'strategy': 'Stackelberg'
    })


def run_simulation(run_id: int):
    env = simpy.Environment()
    results = []
    coverage = stackelberg_defender_strategy(NUM_NODES)

    for i in range(NUM_NODES):
        env.process(node_process(env, i, coverage, results))

    env.run(until=20)
    return results


def main():
    all_results = []

    for run in range(SIM_RUNS):
        run_results = run_simulation(run)
        all_results.extend(run_results)

    total = len(all_results)
    attacked = sum(r['attacked'] for r in all_results)
    detected = sum(r['detected'] for r in all_results)
    compromised = sum(r['compromised'] for r in all_results)
    avg_risk = sum(r['risk_score'] for r in all_results) / total

    detection_rate = (detected / attacked * 100) if attacked > 0 else 0
    compromised_ratio = compromised / total if total > 0 else 0

    print("=== Stackelberg Defender Results ===")
    print(f"Total Nodes Simulated : {total}")
    print(f"Nodes Attacked        : {attacked}")
    print(f"Detection Rate        : {detection_rate:.1f}%")
    print(f"Compromised Ratio     : {compromised_ratio:.2f}")
    print(f"Average Risk Score    : {avg_risk:.2f}")

    os.makedirs('results', exist_ok=True)
    with open('results/stackelberg_results.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=all_results[0].keys())
        writer.writeheader()
        writer.writerows(all_results)

    print("Results saved to results/stackelberg_results.csv")
    return detection_rate, compromised_ratio, avg_risk


if __name__ == '__main__':
    main()
