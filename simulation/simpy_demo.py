# simpy_demo.py
# Week 1 - SimPy: Event-Driven Attack Simulation
# Topic: Environment, Process, Timeout, Event Scheduling
# Summer Research Internship 2025 - Group 4

import simpy

# ─────────────────────────────────────────────
# Simulation Config
# ─────────────────────────────────────────────

SIM_DURATION    = 20   # total simulation time units
PACKET_INTERVAL = 2    # normal device sends every 2 time units
ATTACK_INTERVAL = 5    # attacker sends every 5 time units
DETECT_INTERVAL = 3    # defender checks every 3 time units

# Counters
stats = {"normal_packets": 0, "fake_packets": 0, "detected": 0, "missed": 0}

# ─────────────────────────────────────────────
# Process 1: Normal Device
# ─────────────────────────────────────────────

def normal_device(env):
    while True:
        stats["normal_packets"] += 1
        print(f"  [t={env.now:>4}]  Device    >> Sends NORMAL packet  (total: {stats['normal_packets']})")
        yield env.timeout(PACKET_INTERVAL)

# ─────────────────────────────────────────────
# Process 2: Attacker
# ─────────────────────────────────────────────

def attacker(env):
    yield env.timeout(0)   # attacker starts immediately
    while True:
        stats["fake_packets"] += 1
        print(f"  [t={env.now:>4}]  Attacker  >> Injects FAKE packet  (total: {stats['fake_packets']})")
        yield env.timeout(ATTACK_INTERVAL)

# ─────────────────────────────────────────────
# Process 3: Defender (basic detection logic)
# ─────────────────────────────────────────────

def defender(env):
    yield env.timeout(DETECT_INTERVAL)   # first check after delay
    while True:
        # Simple detection: catches attack if fake packet was sent in last window
        if stats["fake_packets"] > stats["detected"] + stats["missed"]:
            stats["detected"] += 1
            print(f"  [t={env.now:>4}]  Defender  >> ⚠ ATTACK DETECTED")
        else:
            stats["missed"] += 1
            print(f"  [t={env.now:>4}]  Defender  >> Network check OK")
        yield env.timeout(DETECT_INTERVAL)

# ─────────────────────────────────────────────
# Run Simulation
# ─────────────────────────────────────────────

print("=" * 55)
print("  SimPy Event-Driven Simulation - Week 1")
print("  Project: Event-Driven 6G Scheduling")
print("=" * 55)
print()

env = simpy.Environment()
env.process(normal_device(env))
env.process(attacker(env))
env.process(defender(env))
env.run(until=SIM_DURATION)

# ─────────────────────────────────────────────
# Summary
# ─────────────────────────────────────────────

print()
print("=" * 55)
print("  Simulation Summary (t=0 to t={})".format(SIM_DURATION))
print("=" * 55)
print(f"  Normal Packets Sent : {stats['normal_packets']}")
print(f"  Fake Packets Sent   : {stats['fake_packets']}")
print(f"  Attacks Detected    : {stats['detected']}")
print(f"  Attacks Missed      : {stats['missed']}")
if stats["fake_packets"] > 0:
    dr = stats["detected"] / stats["fake_packets"] * 100
    print(f"  Detection Rate      : {dr:.1f}%")
print("=" * 55)
