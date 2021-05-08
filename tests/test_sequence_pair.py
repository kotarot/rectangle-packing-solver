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

import math

import pytest

import rectangle_packing_solver as rps
from example_data import example_problem, example_pair


def test_sequence_pair_init(example_pair):
    seqpair = rps.SequencePair(pair=example_pair)

    assert seqpair.pair == example_pair
    assert seqpair.gp == example_pair[0]
    assert seqpair.gn == example_pair[1]
    assert seqpair.n == 4

    assert seqpair.oblique_grid.grid == [[-1, -1, -1, 0], [-1, -1, 1, -1], [-1, 2, -1, -1], [3, -1, -1, -1]]
    assert seqpair.oblique_grid.coordinates == [{"x": 0, "y": 3}, {"x": 1, "y": 2}, {"x": 2, "y": 1}, {"x": 3, "y": 0}]


def test_sequence_pair_decode(example_problem, example_pair):
    problem = rps.Problem(rectangles=example_problem)
    seqpair = rps.SequencePair(pair=example_pair)

    floorplan = seqpair.decode(problem=problem)

    assert isinstance(floorplan, rps.Floorplan)
    assert isinstance(floorplan.positions, list)
    assert len(floorplan.positions) == 4
    assert isinstance(floorplan.boundary_box, tuple)
    assert len(floorplan.boundary_box) == 2
    assert isinstance(floorplan.area, float)

    # Positions
    assert floorplan.positions[0]["id"] == 0
    assert math.isclose(floorplan.positions[0]["x"], 0.0)
    assert math.isclose(floorplan.positions[0]["y"], 12.2)

    assert floorplan.positions[1]["id"] == 1
    assert math.isclose(floorplan.positions[1]["x"], 0.0)
    assert math.isclose(floorplan.positions[1]["y"], 8.2)

    assert floorplan.positions[2]["id"] == 2
    assert math.isclose(floorplan.positions[2]["x"], 0.0)
    assert math.isclose(floorplan.positions[2]["y"], 5.0)

    assert floorplan.positions[3]["id"] == 3
    assert math.isclose(floorplan.positions[3]["x"], 0.0)
    assert math.isclose(floorplan.positions[3]["y"], 0.0)

    # Boundary box
    assert floorplan.boundary_box == (4.0, 18.2)

    # Area
    assert floorplan.area == 72.8
