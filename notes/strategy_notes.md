# Week 3 Notes — Stackelberg vs Nash Strategy Selection
**Summer Research Internship 2025 | Group 4**
**Project: Event-Driven 6G Scheduling using SimPy + Sionna**

---

## 1. Nash Equilibrium

### Definition
A stable state in a game where no player can improve their outcome by changing their own strategy, assuming all other players keep their strategies unchanged.

**Condition:** `Ui(s*i, s*j) ≥ Ui(si, s*j)` for both players

### How It Works in Our Simulation
Both defender and attacker decide their strategies **simultaneously** — neither knows what the other will do before committing.

**Iterative Best Response (how we compute Nash):**
1. Defender starts by monitoring top-5 highest-risk nodes
2. Attacker best response: picks highest-risk **unmonitored** node
3. Defender best response: shifts monitoring to include attacker's likely target
4. Repeat until neither player wants to change — **equilibrium reached**

### Limitation
Both players respond to the **current** state, not the anticipated future state. Defender cannot predict where the attacker will strike next. This is why Nash is **reactive**.

---

## 2. Stackelberg Game

### Definition
A sequential, leader-follower game where the **Leader** (Defender) commits to a strategy first, and the **Follower** (Attacker) observes and responds optimally.

### How It Works in Our Simulation
1. **Defender (Leader):** Enumerates possible monitoring sets from top-12 high-risk nodes
2. For each monitoring set: simulates what the attacker would do (best response)
3. Computes estimated Ud for that outcome
4. Commits to the monitoring set with the **highest Ud** — knowing the attacker is rational

### Why Stackelberg Is Better for Security
| | Nash | Stackelberg |
|---|---|---|
| Decision timing | Simultaneous | Defender moves first |
| Attacker knowledge | Neither knows the other's move | Attacker knows defender's allocation |
| Defender advantage | None | Anticipates attacker's best response |
| Result | Reactive defence | Proactive defence |

**From seniors' paper:** Stackelberg attack success rate = **0.021** vs Nash = **0.034** — 38% fewer successful attacks.

---

## 3. Key Equations

| Function | Formula | What It Measures |
|---|---|---|
| Defender Utility | `Ud = α·D − β·C` | Defender gain (α=1.0, β=2.0) |
| Attacker Utility | `Ua = γ·C − δ·D` | Attacker gain (γ=2.0, δ=1.0) |
| Detection Prob | `P = 1/(1+e^(-(θ₁Ri−θ₂F)))` | Sigmoid based on risk + fatigue |
| Infection Pressure | `IP = w₁V + w₂R` | Spread risk to neighbours |

---

## 4. Defender Resource Allocation

The defender has a **fixed budget** of 5 monitored nodes out of 50. This models real-world constraints — a network operator cannot monitor every device with equal intensity. Both strategies must decide which 5 nodes get monitoring resources each round.

- **Stackelberg:** allocates based on anticipated attacker response — proactive
- **Nash:** allocates based on current risk scores converged through iteration — reactive

---

## 5. Attack Prediction

Stackelberg's core advantage is **attack prediction** — by simulating the attacker's best response to every candidate monitoring set, the defender effectively "plays out" the attacker's move before committing. This is computationally more expensive (evaluates combinations) but produces a measurably better outcome.

---

## 6. Connection to 6G Scheduling

In our 6G scheduling context, the base station (defender/leader) allocates radio resource blocks first. Users (followers) transmit based on what's assigned. This is the same Stackelberg structure — the base station can anticipate which users will request the most bandwidth and pre-allocate accordingly, rather than reacting to requests after they arrive.

---

## Week 3 Key Insight

> The first-mover advantage in Stackelberg is not about being faster — it is about being smarter. By committing to a strategy that accounts for the rational attacker's response, the defender turns the attacker's own rationality against them. The attacker's best move under the Stackelberg monitoring set is always less damaging than the attacker's best move under Nash.
