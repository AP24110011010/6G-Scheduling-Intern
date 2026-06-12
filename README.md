# Event-Driven 6G Scheduling using SimPy + Sionna

**Project Goal**

To develop and study an event-driven scheduling framework for future 6G networks using discrete-event simulation (SimPy), graph-based network modeling (NetworkX), and physical-layer channel simulation (Sionna), with intelligent resource management techniques based on Game Theory and Machine Learning.

---

## Team Members

| Name | Roll Number |
|---|---|
| Snehitha | AP24110011008 |
| Shahistha Anjum | AP24110010993 |
| Shanmukh | AP24110011010 |
| Sandeep | AP24110010992 |

**Mentor:** Dr. Ch Anil Carie
**Institution:** SRM University AP, Amaravati
**Programme:** Summer Research Internship 2025 (8 Weeks)

---

## Repository Structure

```
6G-Scheduling-Intern/
│
├── week1/
│   └── network_topology.py         # 5-node NetworkX graph (Week 1)
│
├── week2/
│   ├── iot_network.py              # 50-node Barabasi-Albert IoT network
│   ├── attack_engine.py            # Random, Targeted, Burst attack modes
│   ├── defender_engine.py          # Betweenness-guided monitoring engine
│   └── baseline_simulation.py      # Full 100-round baseline simulation
│
├── simulation/
│   └── simpy_demo.py               # Week 1 SimPy event simulation
│
├── notebooks/
│   └── python_basics.py            # Python fundamentals practice
│
├── notes/
│   ├── important_notes.md          # Nash + Stackelberg + Modbus (Week 1)
│   ├── graph_theory_notes.md       # Centrality metrics + BA model (Week 2)
│   └── iot_security_notes.md       # DoS, DDoS, Recon, Malware, Botnets (Week 2)
│
├── results/
│   ├── network_topology.png        # 5-node graph (Week 1)
│   ├── network_visualization.png   # 50-node risk heatmap (Week 2)
│   ├── attack_logs.csv             # Attack event log (Week 2)
│   └── compromised_over_time.png   # 100-round simulation plots (Week 2)
│
├── requirements.txt
└── README.md
```

---

## Week 1 Tasks Completed

* Installed Python, VS Code, Git, and required libraries
* Built 5-node IoT network topology using NetworkX
* Implemented event-driven simulation with SimPy (normal device + attacker)
* Studied Nash Equilibrium and Stackelberg Game Theory
* Analyzed CIC Modbus 2023 dataset structure and attack types

## Week 2 Tasks Completed

* Studied Graph Theory — Degree, Betweenness, Closeness Centrality, Network Density
* Studied IoT Security attack types — DoS, DDoS, Reconnaissance, Malware, Botnets
* Built 50-node scale-free IoT network using Barabasi-Albert model
* Implemented three attack modes: Random, Targeted, Burst with CSV logging
* Built betweenness-guided defender engine with detection and partial recovery
* Ran full 100-round baseline simulation with network statistics over time

---

## How to Run

```bash
# Install dependencies
pip install -r requirements.txt

# Week 2 — Run 50-node network
python week2/iot_network.py

# Week 2 — Run attack engine test
python week2/attack_engine.py

# Week 2 — Run full 100-round simulation
python week2/baseline_simulation.py

# Week 1 — Run 5-node network
python week1/network_topology.py

# Week 1 — Run SimPy demo
python simulation/simpy_demo.py
```

---

## Dataset Reference

**CIC Modbus 2023 Dataset**
Source: [https://www.unb.ca/cic/datasets/modbus-2023.html](https://www.unb.ca/cic/datasets/modbus-2023.html)

---

## Week 3 Plan

- Implement Stackelberg game-theoretic defender strategy
- Implement Nash baseline defender for comparison
- Run Stackelberg vs Nash 100-round comparison
- Generate comparison plots for paper
