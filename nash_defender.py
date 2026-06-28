"""
nash_defender.py
Week 4 — Nash Defender Model (Refined)
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


def nash_equilibrium_strategy() -> tuple:
    """
    Nash Equilibrium: Both players choose mixed strategies simultaneously.
    Defender coverage and attack probability satisfy mutual best-response.
    Returns (defender_coverage, attack_probability).
    """
    # Mixed strategy Nash: solve p* and q* analytically
    # Defender indifferent: q*(DR - RC) = (1-q*)*(MP + RC) => solve for q*
    # Attacker indifferent: p*(ASR) = (1-p*)*(AFP) => solve for p*
    q_star = (abs(DEFENDER_MISS_PENALTY) + RESOURCE_COST) / (
        DEFENDER_DETECTION_REWARD + abs(DEFENDER_MISS_PENALTY)
    )
    p_star = abs(ATTACKER_FAIL_PENALTY) / (
        ATTACKER_SUCCESS_REWARD + abs(ATTACKER_FAIL_PENALTY)
    )
    return round(min(q_star, 1.0), 3), round(min(p_star, 1.0), 3)


def node_process(env, node_id, coverage, attack_prob, results):
    """SimPy process: each node operates under Nash equilibrium strategies."""
    yield env.timeout(random.uniform(1, 5))

    attacked = random.random() < attack_prob

    if attacked:
        detected = random.random() < (coverage * 0.85)
        compromised = not detected
    else:
        detected = False
        compromised = False

    risk_score = 0.0 if not attacked else (0.15 if detected else 0.85)

    results.append({
        'node_id': node_id,
        'attacked': int(attacked),
        'detected': int(detected),
        'compromised': int(compromised),
        'risk_score': round(risk_score, 2),
        'strategy': 'Nash'
    })


def run_simulation(run_id: int):
    env = simpy.Environment()
    results = []
    coverage, attack_prob = nash_equilibrium_strategy()

    for i in range(NUM_NODES):
        env.process(node_process(env, i, coverage, attack_prob, results))

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

    print("=== Nash Defender Results ===")
    print(f"Total Nodes Simulated : {total}")
    print(f"Nodes Attacked        : {attacked}")
    print(f"Detection Rate        : {detection_rate:.1f}%")
    print(f"Compromised Ratio     : {compromised_ratio:.2f}")
    print(f"Average Risk Score    : {avg_risk:.2f}")

    os.makedirs('results', exist_ok=True)
    with open('results/nash_results.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=all_results[0].keys())
        writer.writeheader()
        writer.writerows(all_results)

    print("Results saved to results/nash_results.csv")
    return detection_rate, compromised_ratio, avg_risk


if __name__ == '__main__':
    main()
