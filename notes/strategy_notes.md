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

### Strategy Selection (Nash)
```python
strategy_select_nash(G, budget=5, max_iter=10)
```
Converges in ~5–7 iterations typically. Returns the stable monitoring set where neither player benefits from changing.

### Limitation
Both players respond to the **current** state, not the anticipated future state. Defender cannot predict where the attacker will strike next. This is why Nash is **reactive**.

---

## 2. Stackelberg Game

### Definition
A sequential, leader-follower game where the **Leader** (Defender) commits to a strategy first, and the **Follower** (Attacker) observes and responds optimally.

### How It Works in Our Simulation
1. **Defender (Leader):** Enumerates all possible monitoring sets of size 5
2. For each monitoring set: simulates what the attacker would do (best response)
3. Computes estimated Ud for that outcome
4. Commits to the monitoring set with the **highest Ud** — knowing the attacker is rational

### Strategy Selection (Stackelberg)
```python
strategy_select_stackelberg(G, budget=5)
```
Evaluates combinations of top-12 high-risk nodes (fast approximation). Returns the optimal monitoring set under rational attacker assumption.

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

## 4. Strategy Differences in Practice

### Test on 10-node network (seed=42):
- **Stackelberg** selected nodes with **balanced risk + centrality** — spread monitoring to cover attacker's anticipated move
- **Nash** selected the **highest raw risk nodes** — no anticipation, just current state

### Key Insight
Stackelberg monitoring set is different from Nash because it solves:

> "If I monitor these nodes, the rational attacker moves to that node. So I should include that node in my monitoring set, which pushes the attacker elsewhere. I should pick the set that makes every possible attack as detectable as possible."

Nash simply answers: **"What is the best response to the attacker's current behaviour?"**

---

## 5. Connection to 6G Scheduling

In our 6G scheduling context, the base station (defender/leader) allocates radio resource blocks first. Users (followers) transmit based on what's assigned. This is the same Stackelberg structure — the base station can anticipate which users will request the most bandwidth and pre-allocate accordingly, rather than reacting to requests after they arrive.

---

## Week 3 Key Insight

> The first-mover advantage in Stackelberg is not about being faster — it is about being smarter. By committing to a strategy that accounts for the rational attacker's response, the defender turns the attacker's own rationality against them. The attacker's best move under the Stackelberg monitoring set is always less damaging than the attacker's best move under Nash.
