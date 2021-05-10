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

Sample code:
```python
import rectangle_packing_solver as rps

# Define a problem
problem = rps.Problem(rectangles=[
    [4, 6],  # Format: [width, height] as list. Default rotatable: False
    (4, 4),  # Format: (width, height) as tuple. Default rotatable: False
    {"width": 2.1, "height": 3.2, "rotatable": False},  # Or can be defined as dict.
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

Output:
```plaintext
problem: Problem({'n': 4, 'rectangles': [{'id': 0, 'width': 4, 'height': 6, 'rotatable': False}, {'id': 1, 'width': 4, 'height': 4, 'rotatable': False}, {'id': 2, 'width': 2.1, 'height': 3.2, 'rotatable': False}, {'id': 3, 'width': 1, 'height': 5, 'rotatable': True}]})
solving...
solution: Solution({'sequence_pair': SequencePair(([0, 1, 3, 2], [3, 0, 2, 1])), 'floorplan': Floorplan({'positions': [{'id': 0, 'x': 0, 'y': 1}, {'id': 1, 'x': 4, 'y': 3.2}, {'id': 2, 'x': 5.0, 'y': 0.0}, {'id': 3, 'x': 0, 'y': 0}], 'boundary_box': (8, 7.2), 'area': 57.6})})
```

## References

[1] H. Murata, K. Fujiyoshi, S. Nakatake, and Y. Kajitani, "VLSI module placement based on rectangle-packing by the sequence-pair," *IEEE Trans. on Computer-Aided Design of Integrated Circuits and Systems*, vol. 15, no. 12, pp. 1518--1524, Dec 1996.
