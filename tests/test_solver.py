# Copyright 2021 Kotaro Terada
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
from tests.example_data import example_problem  # noqa: F401


def test_solver(example_problem):  # noqa: F811
    problem = rps.Problem(rectangles=example_problem)
    solver = rps.Solver()
    solution = solver.solve(problem=problem)

    assert isinstance(solution, rps.Solution)
    assert isinstance(solution.sequence_pair, rps.SequencePair)
    assert isinstance(solution.floorplan, rps.Floorplan)

    # The optimal solution is any of ([0, 1, 3, 2], [3, 0, 2, 1]), ([1, 2, 0, 3], [2, 3, 1, 0]), ([2, 3, 1, 0], [1, 2, 0, 3]), or ([3, 0, 2, 1], [0, 1, 3, 2])
    optimal_0 = solution.sequence_pair.pair == ([0, 1, 3, 2], [3, 0, 2, 1]) and solution.floorplan.bounding_box == (8, 7.2)
    optimal_1 = solution.sequence_pair.pair == ([1, 2, 0, 3], [2, 3, 1, 0]) and solution.floorplan.bounding_box == (8, 7.2)
    optimal_2 = solution.sequence_pair.pair == ([2, 3, 1, 0], [1, 2, 0, 3]) and solution.floorplan.bounding_box == (8, 7.2)
    optimal_3 = solution.sequence_pair.pair == ([3, 0, 2, 1], [0, 1, 3, 2]) and solution.floorplan.bounding_box == (8, 7.2)
    assert optimal_0 or optimal_1 or optimal_2 or optimal_3

    assert solution.floorplan.area == 57.6
    assert solution.floorplan.bounding_box[0] * solution.floorplan.bounding_box[1] == solution.floorplan.area


def test_solver_with_width_limit(example_problem):  # noqa: F811
    problem = rps.Problem(rectangles=example_problem)
    solver = rps.Solver()
    solution = solver.solve(problem=problem, width_limit=6.5)
    assert solution.floorplan.bounding_box[0] <= 6.5


def test_solver_with_height_limit(example_problem):  # noqa: F811
    problem = rps.Problem(rectangles=example_problem)
    solver = rps.Solver()
    solution = solver.solve(problem=problem, height_limit=6.5)
    assert solution.floorplan.bounding_box[1] <= 6.5
