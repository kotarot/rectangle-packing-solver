#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2022 Kotaro Terada
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import rectangle_packing_solver as rps


def main():
    # Define a problem
    problem = rps.Problem(
        rectangles=[
            [4, 6],  # Format: [width, height] as list. Default rotatable: False
            (4, 4),  # Format: (width, height) as tuple. Default rotatable: False
            {"width": 2.1, "height": 3.2, "rotatable": False},  # Or can be defined as dict.
            {"width": 1, "height": 5, "rotatable": True},
        ]
    )
    print("problem:", problem)

    # Find a solution
    print("\n=== Solving without width/height constraints ===")
    solution = rps.Solver().solve(problem=problem)
    print("solution:", solution)

    # Visualization (to floorplan.png)
    rps.Visualizer().visualize(solution=solution, path="./figs/floorplan_example.png")

    # [Other Usages]
    # We can also give a solution width (and/or height) limit
    print("\n=== Solving with width/height constraints ===")
    solution = rps.Solver().solve(problem=problem, height_limit=6.5, show_progress=True, seed=1111)
    print("solution:", solution)
    rps.Visualizer().visualize(solution=solution, path="./figs/floorplan_example_limit.png")


if __name__ == "__main__":
    main()
