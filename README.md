# Port Docking Optimization

Authors: Karol Tomczyk, Patryk Nogaś
Date: June 2026

## Project Overwiew

This project aims to find optimal docking of ships in a port with two docks, we use linear optimization techniques and we made some difficult to constrains -- large ships of length 3 or two medium sized ships can block the flow to inner port. The goal was to maximize the number of ships and value of docked ships.


## Approaches
We implemented two solutions to solve this combinatorial optimization problem:


### Linear Optimization using gurobi

Uses a matrix-based decision model.
- Objective: Maximize the sum of ship values docked.
- Constraints: Ensures no overlaps, blocks, or invalid placements.
- Pros: Guarantees optimal solutions.
- Cons: Resource-intensive and less scalable for large fleets. Must pay for pricey linear optimization solver.

### Genetic Algorithm
- Inspired by biological evolution (selection, crossover, mutation).
- Chromosome = Port layout, Gene = Ship position.
- Fitness function: Rewards valid dockings, penalizes blocks/collisions.
- Pros: Scalable, hardware-efficient, and adaptable.
- Cons: No guarantee of optimality (but often near-optimal).


## Results
- Gurobi: Optimal but slower for large inputs (e.g., 20 ships → 27 value).
- Genetic Algorithm: Fast convergence (e.g., 20 generations → 28 value).
- Comparison: Both methods yield similar results, but the genetic algorithm is more scalable.


# [READ WHOLE REPORT HERE](report.pdf)
