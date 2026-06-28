# Performance Report — Week 4
## Game-Theoretic Defender Strategy Comparison
**Group 4 | Event-Driven 6G Scheduling using SimPy + Sionna**
**Period: 21–27 June 2026**

---

## Summary

This report presents the preliminary performance evaluation of the Stackelberg Defender and Nash Defender models implemented during Week 4. Both strategies were tested over 20 simulation runs with 10 IoT nodes each.

---

## Metrics Used

| Metric | Definition |
|---|---|
| Detection Rate | % of attacks successfully detected by the defender |
| Compromised Ratio | Fraction of total nodes that were compromised |
| Average Risk Score | Mean risk score across all nodes (0 = safe, 1 = fully compromised) |

---

## Results Table

| Strategy | Detection Rate | Compromised Ratio | Avg Risk Score | Simulation Runs |
|---|---|---|---|---|
| Stackelberg Defender | **85%** | **0.17** | **0.34** | 20 |
| Nash Defender | 79% | 0.23 | 0.41 | 20 |

---

## Key Observations

1. **Stackelberg outperforms Nash** across all three metrics in preliminary evaluation.
2. **Detection Rate gap:** Stackelberg achieves 6 percentage points higher detection rate.
3. **Compromised Ratio:** Stackelberg reduces compromised ratio by ~26% compared to Nash.
4. **Risk Score:** Stackelberg average risk score is 17% lower than Nash.
5. **Payoff sensitivity:** Small modifications to payoff weights (±1.0) caused ~3–5% shifts in detection rate, confirming high sensitivity of strategy selection to payoff function design.

---

## Why Stackelberg Performs Better

The Stackelberg defender acts as the **leader** in a sequential game — it selects coverage by anticipating the attacker's optimal response. This proactive allocation concentrates defenses where attacks are most likely, reducing successful intrusions.

The Nash defender operates under **simultaneous-move** assumptions, treating the attacker's strategy as fixed. This leads to a mixed-strategy equilibrium that is stable but not optimal against a rational attacker.

---

## Limitations

- Evaluation limited to **small-scale simulations** (10 nodes, 20 runs).
- Attack scenarios used fixed probability distributions; real IoT attacks show dynamic patterns.
- Visualization of comparison plots partially completed (see `results/strategy_comparison.png`).
- Large-scale network topology testing deferred to Week 5.

---

## Next Steps (Week 5)

- Scale simulations to 50–100 nodes.
- Test under multiple attack scenario types (DDoS, replay, eavesdropping).
- Complete `strategy_comparison.png` visualization.
- Refine payoff engine based on sensitivity findings.

---

*Figure reference: results/strategy_comparison.png — Bar chart comparing Detection Rate and Compromised Ratio for Stackelberg vs Nash Defender across 20 simulation runs.*
