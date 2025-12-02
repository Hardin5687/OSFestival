# OSFestival 🎶

**OSFestival** is a Python multithreaded simulation of an outdoor music festival, modeling the complex, emergent behaviors of thousands of independent festival-goers, staff, and activities.  
Spectators interact, move, make decisions, and influence the environment, all while every significant event is logged to an SQLite database for further analysis.

---

## Table of Contents

- [Features](#features)
- [System Architecture](#system-architecture)
  - [Locations](#locations)
  - [Pathfinding](#pathfinding-search-bfs)
  - [Core Actors](#core-actors)
  - [Data Logging](#data-logging)
  - [Simulation Flow](#simulation-flow)
- [Data Flow Example](#data-flow-example)
- [Setup & Usage](#setup--usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **Multi-threaded environment:** Each spectator, security guard, and artist operates in its own Python thread for realism and concurrency.
- **Complex festival map:** Multiple interconnected locations using a manually constructed festival graph.
- **Probabilistic, personality-driven AI:** Spectators make decisions based on preferences, state, and relationships.
- **Full event audit:** All sales, security events, bathroom activity, drugs, and tickets logged to a central SQLite DB (thread-safe).
- **Security, nurse, and dealer logic:** Simulates drama and fun (fights, ejections, healing, drugs, etc.)
- **Artists dynamically update stages:** Music genres and quality ratings change throughout the simulation.
- **Configurable and extensible:** Easily adapt location types, spectator personalities, and event logging.

---

## System Architecture

### Locations

All festival areas inherit from a common `Location` base class, supporting movement and state-tracking of visitors.

#### Main Locations

- **Stages (Stage 1, 2, 3):**  
  - Host artists & music genres, support dancing behavior.  
- **Food Courts (A, B):**  
  - Sell food, water, alcohol. Log purchases to DB.
- **Bathrooms (A, B):**  
  - Model stall usage, waiting, and water consumption. Log all usage.
- **Nurse Tents (A, B):**  
  - Heal and reset spectators. Eject after repeat incidents.
- **Drug Dealers (3 total):**  
  - Fixed to a stage location. Log drug sales.
- **Exit Gate:**  
  - All festival departures flow through here.

See [Festival Graph](#festival-graph) below.

---

#### Festival Graph

**(Bidirectional links except where noted)**

```
(Stage1) <---> (Food Court A) <---> (Stage2) <---> (Food Court B) <---> (Stage3)
  |                           |                      |                          |
Bathroom A               Bathroom A             Bathroom B             Bathroom B
  |                         |                     |                      |
Nurse Tent A               |               Nurse Tent B                  |
  |_________________________|___________ ________________________________|
                |                                                    |
            (Exit Gate) <-------> [all three stages]
```

- **Spectator movement** is always resolved via breadth-first search (BFS), guaranteeing instant transit and no deadlocks or loops.

---

### Pathfinding (Search BFS)

Spectators request destination(s), triggering a correct BFS algorithm:

- Finds shortest path (if any) from current location to destination via neighbor connections
- Movement enacted via `Location.sendTo()` and `Location.receive()`
- No infinite loops; unmovable requests fail gracefully
- Ensures `spectator.location` always accurately reflects reality

---

### Core Actors

#### Spectators (`Spectator` thread)  
- **Attributes:**  
   - ID, personality, current location, inventory, preferences, relationships
   - Flags for fighting, being escorted, leaving, and activity status
- **Behaviors:**  
   - Dance, eat, drink, flirt, fight, take drugs, use bathroom, heal, exit
- **Decision process:**  
   - Preferences handled by a softmax model; some events override choice (e.g., fights)
   - Moves between locations using BFS

#### Security Guards (`SecurityGuard` thread)  
- **Monitors** locations for conflict
- **Intervenes**: Breaks up fights, escorts/kicks out spectators, logs actions

#### Artists (`Artist` thread)  
- **Perform** periodically, change music genre/quality on their stage

#### Drug Dealers  
- **Stationary** at assigned stage
- **Sell** drugs to interested spectators, log all sales

#### Clock (`Clock` thread)  
- Simulation time source, governs spectator spawning and events

---

### Data Logging

**All events are logged to SQLite** through a thread-safe event queue serviced by a dedicated writer thread.

- **Sales (`sales`)**
- **Drug Sales (`drug_sales`)**
- **Bathroom Usage (`bathroom_usage`)**
- **Security Events (`security_events`)**
- **Tickets (`tickets`)**

No database lock contention: writer thread is the only committer.

---

### Simulation Flow

1. **Initialize Locations & Graph:**  
   All locations are instantiated and connected per the festival graph (no auto-generation of neighbors).
2. **Create Actors:**  
   - Drug dealers, nurses, artists, security guard threads
3. **Start Clock**
4. **Spawn Spectators:**  
   - Each is a thread, spawned at valid `.receive()`-supporting locations (typically random stage)
5. **Run Simulation:**  
   - Each thread independently performs decisions/actions; data is logged to SQLite
6. **Exit:**  
   - Spectators eventually leave via the Exit Gate; simulation ends after all are gone

---

## Data Flow Example

1. **Spectator** at Stage 1 decides to get food (based on preferences/needs)
2. **Pathfinding**: BFS identifies route (Stage 1 → Food Court A)
3. **Purchase Event**: Buys food; metrics logged to SQLite (`metrics.log_sale`)
4. **Bathroom Need**: Decides to use facilities; path leads to Bathroom A
5. **Bathroom Usage**: Waits for stall; usage and wait time logged
6. **Drug Offer**: Interacts with local dealer, makes purchase; `metrics.log_drug_sale` tracks event
7. **Conflict**: Fight breaks out; security intervenes, event logged

All actions are concurrent, stochastic, and logged for external analysis.

---

## Setup & Usage

### Requirements

- Python 3.8+ (recommended 3.10+)
- [SQLite3](https://docs.python.org/3/library/sqlite3.html) (standard in Python)
- No external dependencies unless extended

### Installation

Clone the repository:

```bash
git clone https://github.com/Hardin5687/OSFestival.git
cd OSFestival
```

### Running the Simulation

```bash
python main.py
```
- The simulation will start, run until all spectators have exited, and output an SQLite database (`festival_metrics.db` by default) with all events.

### Configurations

- Initial parameters (spectator count, logging level, random seeds, etc.) can be set in `config.py` or `main.py` as provided.
- **Note**: Changing graph topology requires manual updating of neighbor lists for each `Location`.

---

## Project Structure

```
OSFestival/
├── locations/          # All Location subclasses
│   ├── stage.py
│   ├── foodcourt.py
│   ├── bathroom.py
│   ├── nursetent.py
│   └── exitgate.py
├── actors/             # Spectator, Security, Artist implementations
│   ├── spectator.py
│   ├── security.py
│   ├── artist.py
│   └── dealer.py
├── metrics.py          # SQLite database event queue + writer
├── clock.py            # Simulation time source
├── main.py             # Simulation entry point and setup
├── config.py           # Parameters and constants
└── README.md           # (You are here)
```

---

## Contributing

Pull requests, bug reports, and feature suggestions are welcome!  
Please open an issue or PR to discuss substantive changes or improvements.

---

## License

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.

---