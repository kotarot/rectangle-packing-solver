# rectangle-packing-solver

`rectangle-packing-solver` is a solver to find a solution for the 2D rectangle packing problem by simulated annealing (SA) optimization.
Sequence-pair [1] is used to represent a rectangle placement (floorplan).

## Features

- TBA

## Installation

```bash
pip install rectangle-packing-solver
```

## Example Usage

```python
import rectangle_packing_solver as rps

# Define a problem
problem = rps.Problem(rectangles=[
    [4, 6],  # Format: [width, height]
    {"width": 4, "height": 4},  # Or can be defined as dict. Default rotatable: False
    {"width": 2.1, "height": 3.2, "rotatable": False},
    {"width": 1, "height": 5, "rotatable": True},
])
print("problem:", problem)

# Get a solver
solver = rps.Solver()
print("solving...")

# Find a solution
solution = solver.solve(problem)
print("solution:", solution)
```

## References

[1] H. Murata, K. Fujiyoshi, S. Nakatake, and Y. Kajitani, "VLSI module placement based on rectangle-packing by the sequence-pair," *IEEE Trans. on Computer-Aided Design of Integrated Circuits and Systems*, vol. 15, no. 12, pp. 1518--1524, Dec 1996.
