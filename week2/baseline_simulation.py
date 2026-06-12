# baseline_simulation.py
# Week 2 - Full 100-Round Baseline Simulation
# Integrates: iot_network + attack_engine + defender_engine
# Summer Research Internship 2025 - Group 4

import sys
import os
import random
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(__file__))

from iot_network    import create_iot_network, analyse_network
from attack_engine  import attack_random, attack_targeted, attack_burst, save_logs
from defender_engine import get_monitored_nodes, monitor_node, network_stats

random.seed(42)
os.makedirs('results', exist_ok=True)

# ─────────────────────────────────────────────
# Simulation Config
# ─────────────────────────────────────────────

ROUNDS     = 100
BURST_SIZE = 5

# ─────────────────────────────────────────────
# Setup
# ─────────────────────────────────────────────

G          = create_iot_network(50)
monitored  = get_monitored_nodes(G, k=5)
prev_risks = {n: G.nodes[n]['risk_score'] for n in G.nodes()}

all_logs        = []
stats_over_time = []

print("=" * 55)
print("  Baseline Simulation — 100 Rounds")
print(f"  Nodes monitored: {monitored[:3]} ...")
print("=" * 55)
print()

# ─────────────────────────────────────────────
# Main Simulation Loop
# ─────────────────────────────────────────────

for t in range(ROUNDS):

    # Step 1: Attacker picks a random mode
    mode = random.choice(['random', 'targeted', 'burst'])

    if mode == 'random':
        log = attack_random(G, t)
    elif mode == 'targeted':
        log = attack_targeted(G, t)
    else:
        log = attack_burst(G, t, n=BURST_SIZE)

    # Step 2: Defender monitors and detects
    monitor_node(G, log, monitored, prev_risks)

    # Step 3: Update risk snapshot
    prev_risks = {n: G.nodes[n]['risk_score'] for n in G.nodes()}

    # Step 4: Log network state
    s = network_stats(G, t)
    stats_over_time.append(s)
    all_logs.append(log)

    # Print progress every 20 rounds
    if t % 20 == 0:
        print(f"  [t={t:>3}]  CR={s['compromised_ratio']:.3f}  "
              f"AvgRisk={s['avg_risk']:.3f}  Mode={mode}")

# ─────────────────────────────────────────────
# Save Attack Logs
# ─────────────────────────────────────────────

flat_logs = save_logs(all_logs)

# ─────────────────────────────────────────────
# Final Summary
# ─────────────────────────────────────────────

final          = stats_over_time[-1]
total_attacks  = len(flat_logs)
detected_count = sum(1 for e in flat_logs if e.get('detected'))
detection_rate = detected_count / total_attacks * 100 if total_attacks else 0

print()
print("=" * 55)
print("  SIMULATION RESULTS")
print("=" * 55)
print(f"  Total Rounds        : {ROUNDS}")
print(f"  Total Attacks       : {total_attacks}")
print(f"  Attacks Detected    : {detected_count}")
print(f"  Detection Rate      : {detection_rate:.1f}%")
print(f"  Final Compromised   : {final['compromised_ratio']*100:.1f}%")
print(f"  Final Avg Risk      : {final['avg_risk']:.4f}")
print("=" * 55)

# ─────────────────────────────────────────────
# Plots
# ─────────────────────────────────────────────

times = [s['time']              for s in stats_over_time]
crs   = [s['compromised_ratio'] for s in stats_over_time]
risks = [s['avg_risk']          for s in stats_over_time]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))

ax1.plot(times, crs, color='#E74C3C', linewidth=2)
ax1.fill_between(times, crs, alpha=0.15, color='#E74C3C')
ax1.set_title('Compromised Device Ratio over 100 Rounds', fontweight='bold', fontsize=12)
ax1.set_xlabel('Simulation Round')
ax1.set_ylabel('Compromised Ratio')
ax1.grid(True, alpha=0.3)
ax1.set_ylim(0, 1)

ax2.plot(times, risks, color='#2980B9', linewidth=2)
ax2.fill_between(times, risks, alpha=0.15, color='#2980B9')
ax2.set_title('Average Risk Score over 100 Rounds', fontweight='bold', fontsize=12)
ax2.set_xlabel('Simulation Round')
ax2.set_ylabel('Average Risk Score')
ax2.grid(True, alpha=0.3)
ax2.set_ylim(0, 1)

plt.suptitle('Baseline Simulation — Week 2 | Event-Driven 6G Scheduling',
             fontsize=11, y=1.02, fontweight='bold')
plt.tight_layout()
plt.savefig('results/compromised_over_time.png', dpi=150, bbox_inches='tight')
plt.close()
print("Plot saved: results/compromised_over_time.png")
