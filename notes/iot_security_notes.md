# Week 2 Notes — IoT Security Attack Types
**Summer Research Internship 2025 | Group 4**
**Project: Event-Driven 6G Scheduling using SimPy + Sionna**

---

## 1. DoS (Denial of Service)

### What It Is
A single attacker floods a target device with requests or packets, exhausting its processing capacity so it cannot serve legitimate traffic.

### How We Simulate It
In our `attack_random()` function, the attacker sends a high-volume packet burst to one selected node, increasing its risk score by 0.2–0.4 per round. If risk reaches 0.85, the device is marked as compromised (unavailable).

### Effect on Network
One node becomes unavailable. Connected devices lose their direct link to it. If the targeted node has high betweenness centrality, the impact on overall routing is severe.

---

## 2. DDoS (Distributed Denial of Service)

### What It Is
Multiple compromised devices (botnet nodes) simultaneously flood a single target. Traffic comes from many sources, making detection harder than a single-source DoS.

### How We Simulate It
Our `attack_burst()` function models this — 5 nodes are attacked simultaneously in one time step, simulating a distributed coordinated attack. The defender's check window is more likely to be triggered by simultaneous events.

### Effect on Network
Higher total damage per round than single DoS. Multiple devices degrade simultaneously, accelerating overall compromised ratio growth.

---

## 3. Reconnaissance

### What It Is
The attacker scans the network to map its topology, discover device IP addresses, open ports, and identify the most vulnerable nodes — before launching a destructive attack.

### How We Simulate It
In `attack_targeted()`, the attacker reads all node `risk_score` attributes before selecting the highest-risk target. This models an attacker who has completed reconnaissance and knows which device to strike.

### Effect on Network
No immediate damage — but enables the next attack to be maximally effective. The Targeted attack mode assumes reconnaissance is already complete.

---

## 4. Malware / Infection Spread

### What It Is
Malicious code that compromises one device and can spread autonomously to connected devices through the network.

### How We Simulate It
When a node's status becomes `'compromised'`, it has a 30% chance per round to increase the risk score of each of its neighbours by 0.1. This models the infection spread model from the seniors' paper: `IP = w1*V + w2*R`.

### Effect on Network
Exponential growth in compromised nodes if not contained. Defender must detect and recover nodes quickly to break the spread chain.

---

## 5. Botnets

### What It Is
A network of already-compromised devices remotely controlled by an attacker to launch coordinated attacks (DDoS, spam, data exfiltration) against external or internal targets.

### How We Simulate It
Once 3 or more nodes are compromised, they collectively act as a botnet in the Burst attack mode — each contributing to the simultaneous multi-node attack. The attacker's effective attack power grows as the botnet grows.

### Effect on Network
Positive feedback loop: more compromised nodes → more effective Burst attacks → more compromised nodes. This is why early detection is critical.

---

## Attack Type Comparison

| Attack Type | Nodes Hit/Round | Knowledge Required | Detection Difficulty |
|---|---|---|---|
| DoS (Random) | 1 | None | Low |
| Targeted | 1 | High (needs risk map) | Medium |
| Burst (DDoS) | 5 | Low | High |
| Malware Spread | 1–N (spreading) | None | Medium |
| Botnet | 5+ (growing) | Medium | High |

---

## Key Insight

> Reconnaissance is not an attack in itself but it enables Targeted attacks to be far more effective than Random attacks. In our simulation, the 20% difference in compromise rate between Random and Targeted modes directly quantifies the value of reconnaissance — a finding worth highlighting in the paper's Discussion section.
