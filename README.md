# rectangle-packing-solver

A solver to find a solution of the 2D rectangle packing problem by simulated annealing (SA) optimization.
Sequence-pair [1] is used to represent a rectangle placement (floorplan).

## Features

- Solution quality and execution time are tunable, since the solver is SA-based.
- Not only integers but also real numbers can be set as a rectangle width and height.
- A rectangle can rotate while optimizing.
- The built-in visualizer visualizes a floorplan solution.

## Installation

```bash
pip install rectangle-packing-solver
```

## Example Usage

### Sample code:

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

# Find a solution
solution = rpm.Solver().solve(problem=problem)
print("solution:", solution)

# Visualization (to floorplan.png)
rps.Visualizer().visualize(solution=solution, path="./floorplan.png")
```

### Output:

```plaintext
problem: Problem({'n': 4, 'rectangles': [{'id': 0, 'width': 4, 'height': 6, 'rotatable': False}, {'id': 1, 'width': 4, 'height': 4, 'rotatable': False}, {'id': 2, 'width': 2.1, 'height': 3.2, 'rotatable': False}, {'id': 3, 'width': 1, 'height': 5, 'rotatable': True}]})
solution: Solution({'sequence_pair': SequencePair(([0, 1, 3, 2], [3, 0, 2, 1])), 'floorplan': Floorplan({'positions': [{'id': 0, 'x': 0, 'y': 1}, {'id': 1, 'x': 4, 'y': 3.2}, {'id': 2, 'x': 5.0, 'y': 0.0}, {'id': 3, 'x': 0, 'y': 0}], 'bounding_box': (8, 7.2), 'area': 57.6})})
```

### Floorplan (example):

![floorplan_example](./figs/floorplan_example.png)

### Floorplan (larger example):

![floorplan_large](./figs/floorplan_large.png)

## References

[1] H. Murata, K. Fujiyoshi, S. Nakatake, and Y. Kajitani, "VLSI module placement based on rectangle-packing by the sequence-pair," *IEEE Trans. on Computer-Aided Design of Integrated Circuits and Systems*, vol. 15, no. 12, pp. 1518--1524, Dec 1996.
