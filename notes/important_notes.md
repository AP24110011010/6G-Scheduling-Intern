# Week 1 Notes — Game Theory & Modbus Dataset
**Summer Research Internship 2025 | Group 4**
**Project: Event-Driven 6G Scheduling using SimPy + Sionna**

---

## 1. Nash Equilibrium

### Definition
A Nash Equilibrium is a stable state in a game where no player can improve their outcome by changing only their own strategy, assuming all other players keep their strategies unchanged.

### Simple Example — Attacker vs Defender

|  | **Defender: Monitor** | **Defender: Don't Monitor** |
|---|---|---|
| **Attacker: Attack** | Attacker loses, Defender wins | Attacker wins, Defender loses |
| **Attacker: Don't Attack** | Both stable | Both stable |

When both players choose the strategy that is their best response to the other's choice, the system reaches **Nash Equilibrium** — neither wants to change.

### Why It Matters in Cybersecurity
- Helps predict how an attacker will behave given the defender's current monitoring level
- Allows defenders to set monitoring intensity so attacks are not profitable
- Used in network resource allocation and intrusion detection strategy design

### Limitation
- Both players decide **simultaneously** — unrealistic in practice
- Defenders usually deploy systems *before* attackers act
- This is why **Stackelberg Game** is more applicable to real security scenarios

---

## 2. Stackelberg Game

### Definition
A sequential, leader-follower game where one player (the Leader) commits to a strategy first, and the other player (the Follower) observes and responds.

### Structure in Our Project

| Role | Player | Action |
|---|---|---|
| **Leader** | Defender (Base Station) | Sets monitoring level / allocates resources first |
| **Follower** | Attacker / User | Observes the leader's move and responds accordingly |

### How It Works — Step by Step
1. Defender (Leader) chooses and commits to a monitoring strategy
2. Attacker (Follower) observes the defender's strategy
3. Attacker responds with the best attack given what they observed
4. Defender, knowing the attacker will respond this way, chose the strategy that minimises damage

### Payoff Functions (from seniors' paper)
```
Ud = α·D − β·C    (Defender payoff: gain per detection, lose per compromise)
Ua = γ·C − δ·D    (Attacker payoff: gain per compromise, lose per detection)
```

### Advantages Over Nash
- More **realistic** — defenders build systems before attackers act
- Defender can be **proactive** rather than reactive
- Proven results: Stackelberg attack success rate = **0.021** vs Nash = **0.034** (38% fewer successful attacks)

### Connection to 6G Scheduling
In our 6G project, the **base station acts as leader** — it allocates radio resource blocks first. Users (followers) then transmit based on what's assigned. This is the same leader-follower structure as Stackelberg.

---

## 3. Modbus Dataset Summary

### Dataset
**CIC Modbus 2023 Dataset**
Source: [https://www.unb.ca/cic/datasets/modbus-2023.html](https://www.unb.ca/cic/datasets/modbus-2023.html)
Provided by: Canadian Institute for Cybersecurity, University of New Brunswick

### What is Modbus?
Modbus is a communication protocol used in **industrial control systems (ICS)** and **IoT** environments — power grids, water treatment plants, factories. It sends sensor readings and commands between devices over TCP/IP. It has **no built-in authentication**, making it a common attack target.

### Why It Is Used in IoT Security Research
- Widely deployed in real industrial environments
- Simple structure makes it easy to inject fake commands
- Attack patterns are well-documented and realistic

### Key Features / Columns

| Feature | Description |
|---|---|
| Source IP | IP address of the sender |
| Destination IP | IP address of the receiver |
| Source Port | Port used by sender |
| Destination Port | Port used by receiver |
| Packet Length | Size of the network packet in bytes |
| Protocol | Communication protocol used |
| Timestamp | Time when the packet was captured |
| Label | Normal / DoS / Scanning / Injection |

### Attack Types

| Attack | Description |
|---|---|
| **DoS** | Denial of Service — floods the network with packets to make it unavailable |
| **Scanning** | Probes devices to find open ports and vulnerabilities |
| **Injection** | Sends fake Modbus commands to actuators, causing incorrect actions |

### Relevance to Our Project
The Modbus dataset provides real-world attack and normal traffic data. In future weeks, we will train a **Random Forest ML classifier** on this dataset to generate device risk scores dynamically — replacing the randomly generated risk values used in prior work.

---

## Key Insight This Week

> The Stackelberg game gives the defender a strategic advantage over Nash equilibrium because the defender commits first and can anticipate the attacker's response. This is exactly how a 6G base station should operate — allocating resources intelligently before users respond, rather than reacting after.
