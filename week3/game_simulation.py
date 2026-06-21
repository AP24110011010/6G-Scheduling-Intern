# game_simulation.py
# Week 3 - Full 100-Round Stackelberg vs Nash Comparison
# Integrates: iot_network + stackelberg_defender + nash_defender
# Summer Research Internship 2025 - Group 4

import sys
import os
import copy
import csv
import random

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(__file__))

from iot_network          import create_iot_network
from stackelberg_defender import stackelberg_step
from nash_defender        import nash_step

random.seed(1)
os.makedirs('results', exist_ok=True)

ROUNDS = 100

# ─────────────────────────────────────────────
# Setup — Identical starting networks for fair comparison
# ─────────────────────────────────────────────

G_base  = create_iot_network(50, seed=1)
G_stack = copy.deepcopy(G_base)
G_nash  = copy.deepcopy(G_base)

logs_s, logs_n = [], []
prev_s = {n: G_stack.nodes[n]['risk_score'] for n in G_stack.nodes()}
prev_n = {n: G_nash.nodes[n]['risk_score']  for n in G_nash.nodes()}

print("=" * 55)
print("  Game Simulation — Stackelberg vs Nash — 100 Rounds")
print("=" * 55)

# ─────────────────────────────────────────────
# Main Loop — Run both strategies on identical networks
# ─────────────────────────────────────────────

for t in range(ROUNDS):
    ls = stackelberg_step(G_stack, t, prev_s)
    ln = nash_step(G_nash, t, prev_n)

    logs_s.append(ls)
    logs_n.append(ln)

    prev_s = {n: G_stack.nodes[n]['risk_score'] for n in G_stack.nodes()}
    prev_n = {n: G_nash.nodes[n]['risk_score']  for n in G_nash.nodes()}

    if t % 20 == 0:
        print(f"  [t={t:>3}] Stack CR={ls['compromised_ratio']:.3f} "
              f"AR={ls['avg_risk']:.3f} | "
              f"Nash CR={ln['compromised_ratio']:.3f} "
              f"AR={ln['avg_risk']:.3f}")

# ─────────────────────────────────────────────
# Save Combined CSV
# ─────────────────────────────────────────────

all_logs = logs_s + logs_n
keys = all_logs[0].keys()
with open('results/comparison_results.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=keys)
    writer.writeheader()
    writer.writerows(all_logs)
print("\nSaved: results/comparison_results.csv")

# ─────────────────────────────────────────────
# Final Metrics
# ─────────────────────────────────────────────

s_dr  = sum(1 for l in logs_s if l['detected']) / ROUNDS * 100
n_dr  = sum(1 for l in logs_n if l['detected']) / ROUNDS * 100
s_cr  = logs_s[-1]['compromised_ratio'] * 100
n_cr  = logs_n[-1]['compromised_ratio'] * 100
s_ar  = logs_s[-1]['avg_risk']
n_ar  = logs_n[-1]['avg_risk']
s_nsr = (1 - logs_s[-1]['compromised_ratio']) * 100
n_nsr = (1 - logs_n[-1]['compromised_ratio']) * 100

print("\n" + "=" * 55)
print("  FINAL RESULTS")
print("=" * 55)
print(f"  Detection Rate  : Stackelberg={s_dr:.1f}%   Nash={n_dr:.1f}%")
print(f"  Compromised     : Stackelberg={s_cr:.1f}%   Nash={n_cr:.1f}%")
print(f"  Avg Risk        : Stackelberg={s_ar:.4f}   Nash={n_ar:.4f}")
print(f"  Survival Rate   : Stackelberg={s_nsr:.1f}%   Nash={n_nsr:.1f}%")
print("=" * 55)

# ─────────────────────────────────────────────
# Plot 1: Final Metrics Comparison Bar Chart
# ─────────────────────────────────────────────

fig, ax = plt.subplots(figsize=(10, 5))
metrics = ['Detection Rate', 'Compromised Ratio', 'Avg Risk (x100)', 'Survival Rate']
s_vals  = [s_dr, s_cr, s_ar * 100, s_nsr]
n_vals  = [n_dr, n_cr, n_ar * 100, n_nsr]
x = range(len(metrics))
width = 0.35

ax.bar([i - width/2 for i in x], s_vals, width, label='Stackelberg', color='#2980B9', alpha=0.85)
ax.bar([i + width/2 for i in x], n_vals, width, label='Nash', color='#E74C3C', alpha=0.85)
ax.set_xticks(list(x))
ax.set_xticklabels(metrics, fontsize=9)
ax.set_ylabel('Value (%)')
ax.set_title('Stackelberg vs Nash — Final Metrics Comparison (100 Rounds)',
             fontweight='bold', fontsize=12)
ax.legend()
ax.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig('results/stackelberg_vs_nash.png', dpi=150, bbox_inches='tight')
plt.close()
print("Saved: results/stackelberg_vs_nash.png")

# ─────────────────────────────────────────────
# Plot 2: Compromised Ratio + Risk over Time
# ─────────────────────────────────────────────

times = [l['time'] for l in logs_s]

fig, axes = plt.subplots(1, 2, figsize=(13, 5))

axes[0].plot(times, [l['compromised_ratio'] for l in logs_s],
             color='#2980B9', linewidth=2, label='Stackelberg')
axes[0].plot(times, [l['compromised_ratio'] for l in logs_n],
             color='#E74C3C', linewidth=2, linestyle='--', label='Nash')
axes[0].set_title('Compromised Ratio over 100 Rounds', fontweight='bold')
axes[0].set_xlabel('Simulation Round')
axes[0].set_ylabel('Compromised Ratio')
axes[0].legend()
axes[0].grid(True, alpha=0.3)
axes[0].set_ylim(0, 1)

axes[1].plot(times, [l['avg_risk'] for l in logs_s],
             color='#2980B9', linewidth=2, label='Stackelberg')
axes[1].plot(times, [l['avg_risk'] for l in logs_n],
             color='#E74C3C', linewidth=2, linestyle='--', label='Nash')
axes[1].set_title('Average Risk Score over 100 Rounds', fontweight='bold')
axes[1].set_xlabel('Simulation Round')
axes[1].set_ylabel('Average Risk Score')
axes[1].legend()
axes[1].grid(True, alpha=0.3)
axes[1].set_ylim(0, 1)

plt.suptitle('Stackelberg vs Nash — Week 3 Results', fontsize=11,
             fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('results/risk_over_time.png', dpi=150, bbox_inches='tight')
plt.close()
print("Saved: results/risk_over_time.png")
print("\nSimulation complete.")
