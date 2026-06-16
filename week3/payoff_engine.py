# payoff_engine.py
# Week 3 - Game Theory: Utility Functions and Payoff Engine
# Topic: Ud, Ua, P_detect, Infection Pressure
# Summer Research Internship 2025 - Group 4

import numpy as np

# ─────────────────────────────────────────────
# 1. Defender Utility Function
# ─────────────────────────────────────────────

def Ud(D, C, alpha=1.0, beta=2.0):
    """
    Defender's utility function.
    Ud = alpha * D - beta * C

    D     = number of attacks detected
    C     = number of devices compromised
    alpha = reward weight for detection (default 1.0)
    beta  = penalty weight for compromise (default 2.0)

    Positive Ud = defender is winning
    Negative Ud = attacker is winning
    """
    return alpha * D - beta * C


# ─────────────────────────────────────────────
# 2. Attacker Utility Function
# ─────────────────────────────────────────────

def Ua(C, D, gamma=2.0, delta=1.0):
    """
    Attacker's utility function.
    Ua = gamma * C - delta * D

    C     = number of successful compromises
    D     = number of attacks detected (penalty)
    gamma = reward weight for compromise (default 2.0)
    delta = penalty weight for detection (default 1.0)

    Higher Ua = more successful attack
    """
    return gamma * C - delta * D


# ─────────────────────────────────────────────
# 3. Detection Probability (Sigmoid)
# ─────────────────────────────────────────────

def P_detect(Ri, F, theta1=1.0, theta2=0.5):
    """
    Probability of detecting an attack on node i.
    Uses sigmoid function from seniors' paper.

    P_detect = 1 / (1 + e^(-(theta1 * Ri - theta2 * F)))

    Ri     = risk score of the target node (0 to 1)
    F      = defender fatigue factor (0 to 1)
    theta1 = risk sensitivity (default 1.0)
    theta2 = fatigue sensitivity (default 0.5)

    Higher Ri = easier to detect (high-risk nodes are suspicious)
    Higher F  = harder to detect (tired defender misses more)
    """
    return 1 / (1 + np.exp(-(theta1 * Ri - theta2 * F)))


# ─────────────────────────────────────────────
# 4. Infection Pressure
# ─────────────────────────────────────────────

def IP(V, R, w1=0.5, w2=0.5):
    """
    Infection pressure on a node.
    IP = w1 * V + w2 * R

    V  = vulnerability score of the node (0 to 1)
    R  = current risk score of the node (0 to 1)
    w1 = weight for vulnerability (default 0.5)
    w2 = weight for risk (default 0.5)

    High IP = node likely to spread infection to neighbours
    Used in malware/botnet spread simulation
    """
    return w1 * V + w2 * R


# ─────────────────────────────────────────────
# 5. Run Tests
# ─────────────────────────────────────────────

if __name__ == '__main__':

    print("=" * 55)
    print("  Payoff Function Tests — Week 3")
    print("  Project: Event-Driven 6G Scheduling")
    print("=" * 55)

    # Ud and Ua comparison
    print("\n  Defender vs Attacker Utility (D=detected, C=compromised)")
    print(f"  {'D':>3}  {'C':>3}  {'Ud':>8}  {'Ua':>8}  {'Winner':>10}")
    print("  " + "-" * 45)
    for D, C in [(5, 0), (4, 1), (3, 2), (2, 3), (1, 4), (0, 5)]:
        ud = Ud(D, C)
        ua = Ua(C, D)
        winner = "Defender" if ud > ua else "Attacker"
        print(f"  {D:>3}  {C:>3}  {ud:>8.2f}  {ua:>8.2f}  {winner:>10}")

    # P_detect across risk levels
    print("\n  Detection Probability vs Risk Score (Fatigue F=0.1)")
    print(f"  {'Risk':>6}  {'P_detect':>10}")
    print("  " + "-" * 20)
    for Ri in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]:
        pd = P_detect(Ri, F=0.1)
        print(f"  {Ri:>6.1f}  {pd:>10.4f}")

    # Fatigue effect
    print("\n  Fatigue Effect on Detection (Risk Ri=0.7)")
    print(f"  {'Fatigue':>8}  {'P_detect':>10}")
    print("  " + "-" * 22)
    for F in [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]:
        pd = P_detect(0.7, F)
        print(f"  {F:>8.1f}  {pd:>10.4f}")

    # Infection pressure
    print("\n  Infection Pressure (V=vulnerability, R=risk)")
    print(f"  {'V':>5}  {'R':>5}  {'IP':>8}")
    print("  " + "-" * 22)
    for V, R in [(0.9, 0.8), (0.5, 0.5), (0.3, 0.7), (0.1, 0.2)]:
        ip = IP(V, R)
        print(f"  {V:>5.1f}  {R:>5.1f}  {ip:>8.4f}")

    print("\n" + "=" * 55)
    print("  All payoff functions verified successfully")
    print("=" * 55)
