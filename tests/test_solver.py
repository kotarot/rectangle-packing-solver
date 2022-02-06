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

import itertools

import pytest

import rectangle_packing_solver as rps
from tests.example_data import example_large_problem, example_problem  # noqa: F401

################################################################
# Example
################################################################


def test_solver_example_problem(example_problem):  # noqa: F811
    problem = rps.Problem(rectangles=example_problem)
    solver = rps.Solver()
    solution = solver.solve(problem=problem)

    assert isinstance(solution, rps.Solution)
    assert isinstance(solution.sequence_pair, rps.SequencePair)
    assert isinstance(solution.floorplan, rps.Floorplan)

    # The optimal solution is any of
    #   ([0, 1, 3, 2], [3, 0, 2, 1]),
    #   ([1, 2, 0, 3], [2, 3, 1, 0]),
    #   ([2, 3, 1, 0], [1, 2, 0, 3]), or
    #   ([3, 0, 2, 1], [0, 1, 3, 2])
    optimal_0 = solution.sequence_pair.pair == ([0, 1, 3, 2], [3, 0, 2, 1])
    optimal_1 = solution.sequence_pair.pair == ([1, 2, 0, 3], [2, 3, 1, 0])
    optimal_2 = solution.sequence_pair.pair == ([2, 3, 1, 0], [1, 2, 0, 3])
    optimal_3 = solution.sequence_pair.pair == ([3, 0, 2, 1], [0, 1, 3, 2])
    assert optimal_0 or optimal_1 or optimal_2 or optimal_3
    assert solution.floorplan.bounding_box == (8, 7.2)

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


################################################################
# Large example
################################################################


def test_solver_example_large_problem(example_large_problem):  # noqa: F811
    problem = rps.Problem(rectangles=example_large_problem)
    solver = rps.Solver()
    solution = solver.solve(problem=problem, simanneal_minutes=1.0, simanneal_steps=500)

    assert isinstance(solution, rps.Solution)
    assert isinstance(solution.sequence_pair, rps.SequencePair)
    assert isinstance(solution.floorplan, rps.Floorplan)

    assert solution.floorplan.area < 6000


def test_solver_example_large_problem_with_width(example_large_problem):  # noqa: F811
    problem = rps.Problem(rectangles=example_large_problem)
    solver = rps.Solver()
    solution = solver.solve(problem=problem, simanneal_minutes=1.0, simanneal_steps=500, width_limit=50.0)
    assert solution.floorplan.bounding_box[0] <= 50.0


def test_solver_example_large_problem_with_height(example_large_problem):  # noqa: F811
    problem = rps.Problem(rectangles=example_large_problem)
    solver = rps.Solver()
    solution = solver.solve(problem=problem, simanneal_minutes=1.0, simanneal_steps=500, height_limit=50.0)
    assert solution.floorplan.bounding_box[1] <= 50.0


################################################################
# Invalid width/height
################################################################


def test_solver_with_invalid_width_limit(example_problem):  # noqa: F811
    problem = rps.Problem(rectangles=example_problem)
    solver = rps.Solver()
    with pytest.raises(ValueError) as e:
        solver.solve(problem=problem, width_limit=3)
    assert "'width_limit' must be greater than or equal to 4" in str(e.value)


def test_solver_with_invalid_height_limit(example_problem):  # noqa: F811
    problem = rps.Problem(rectangles=example_problem)
    solver = rps.Solver()
    with pytest.raises(ValueError) as e:
        solver.solve(problem=problem, height_limit=5.5)
    assert "'height_limit' must be greater than or equal to 6" in str(e.value)


################################################################
# Tight problem
################################################################


def test_solver_with_tight_limits():
    # Note: See PR #23 for details.
    problem = rps.Problem(
        rectangles=[
            {"width": 5, "height": 7, "rotatable": True},
            {"width": 5, "height": 7, "rotatable": True},
            {"width": 5, "height": 7, "rotatable": True},
            {"width": 5, "height": 7, "rotatable": True},
            {"width": 5, "height": 7, "rotatable": True},
        ]
    )
    for width_limit, height_limit in itertools.product([19, 17, 15], [17, 15, 13]):
        solution = rps.Solver().solve(problem=problem, width_limit=width_limit, height_limit=height_limit)
        assert solution.floorplan.bounding_box[0] <= width_limit
        assert solution.floorplan.bounding_box[1] <= height_limit


################################################################
# Random seed
################################################################


def test_solver_random_seed(example_problem):  # noqa: F811
    problem = rps.Problem(rectangles=example_problem)
    solver = rps.Solver()
    solution_1 = solver.solve(problem=problem, seed=1111)

    solution_2 = solver.solve(problem=problem, seed=1111)
    assert solution_1.sequence_pair == solution_2.sequence_pair

    solution_3 = solver.solve(problem=problem, seed=3333)
    assert solution_1.sequence_pair != solution_3.sequence_pair
