# Game Theory Review — Week 4
## Project: Event-Driven 6G Scheduling using SimPy + Sionna
**Group 4 | Week 4 | 21–27 June 2026**

---

## Stackelberg Game

- **Type:** Leader-Follower game
- **Structure:** Defender acts first (leader), Attacker responds optimally (follower)
- **Key Property:** Leader has first-mover advantage; can anticipate follower's best response
- **In Security:** Defender allocates resources assuming attacker will exploit weakest point
- **Payoff Logic:** Leader maximizes payoff knowing follower's reaction function

## Nash Equilibrium

- **Type:** Simultaneous-move game
- **Structure:** Both players choose strategies independently, no player benefits from unilateral deviation
- **Key Property:** Stable state — no incentive to change strategy given opponent's strategy
- **In Security:** Models scenarios where attacker and defender act without observing each other
- **Payoff Logic:** Equilibrium reached when both strategies are mutual best responses

## Key Differences

| Property | Stackelberg | Nash |
|---|---|---|
| Move Order | Sequential | Simultaneous |
| Information | Leader knows follower reacts optimally | Both act independently |
| Defender Role | Leader (proactive) | Equal player (reactive) |
| Performance (Week 4) | Detection Rate: 85%, CR: 0.17 | Detection Rate: 79%, CR: 0.23 |

## Payoff Function Design

- Payoff = f(detection_rate, resource_cost, attack_success)
- Small changes in payoff weights → significant strategy shifts
- Stackelberg defender optimizes over attacker's best-response curve
- Nash defender optimizes independently, leading to slightly suboptimal defense

## References
1. M. J. Osborne, *An Introduction to Game Theory*, Oxford University Press, 2004.
2. T. Başar and G. J. Olsder, *Dynamic Noncooperative Game Theory*, SIAM, 1999.
3. K. Hausken and J. M. Zhuang, *Game Theory and Cyber Security*, Springer, 2011.
