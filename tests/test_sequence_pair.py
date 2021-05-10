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

from example_data import example_pair_horizontally, example_pair_vertically, example_problem  # noqa: F401

import rectangle_packing_solver as rps


def test_sequence_pair_init_horizontally(example_pair_horizontally):  # noqa: F811
    seqpair = rps.SequencePair(pair=example_pair_horizontally)

    assert seqpair.pair == example_pair_horizontally
    assert seqpair.gp == example_pair_horizontally[0]
    assert seqpair.gn == example_pair_horizontally[1]
    assert seqpair.n == 4

    assert seqpair.oblique_grid.grid == [[0, -1, -1, -1], [-1, 1, -1, -1], [-1, -1, 2, -1], [-1, -1, -1, 3]]
    assert seqpair.oblique_grid.coordinates == [{"a": 0, "b": 0}, {"a": 1, "b": 1}, {"a": 2, "b": 2}, {"a": 3, "b": 3}]


def test_sequence_pair_init_vertically(example_pair_vertically):  # noqa: F811
    seqpair = rps.SequencePair(pair=example_pair_vertically)

    assert seqpair.pair == example_pair_vertically
    assert seqpair.gp == example_pair_vertically[0]
    assert seqpair.gn == example_pair_vertically[1]
    assert seqpair.n == 4

    assert seqpair.oblique_grid.grid == [[-1, -1, -1, 0], [-1, -1, 1, -1], [-1, 2, -1, -1], [3, -1, -1, -1]]
    assert seqpair.oblique_grid.coordinates == [{"a": 0, "b": 3}, {"a": 1, "b": 2}, {"a": 2, "b": 1}, {"a": 3, "b": 0}]


def test_sequence_pair_decode_horizontally(example_problem, example_pair_horizontally):  # noqa: F811
    seqpair = rps.SequencePair(pair=example_pair_horizontally)
    floorplan = seqpair.decode(problem=rps.Problem(rectangles=example_problem))

    assert isinstance(floorplan, rps.Floorplan)
    assert isinstance(floorplan.positions, list)
    assert len(floorplan.positions) == 4
    assert isinstance(floorplan.bounding_box, tuple)
    assert len(floorplan.bounding_box) == 2
    assert isinstance(floorplan.area, float)

    # Positions
    assert floorplan.positions[0]["id"] == 0
    assert math.isclose(floorplan.positions[0]["x"], 0.0)
    assert math.isclose(floorplan.positions[0]["y"], 0.0)

    assert floorplan.positions[1]["id"] == 1
    assert math.isclose(floorplan.positions[1]["x"], 4.0)
    assert math.isclose(floorplan.positions[1]["y"], 0.0)

    assert floorplan.positions[2]["id"] == 2
    assert math.isclose(floorplan.positions[2]["x"], 8.0)
    assert math.isclose(floorplan.positions[2]["y"], 0.0)

    assert floorplan.positions[3]["id"] == 3
    assert math.isclose(floorplan.positions[3]["x"], 10.1)
    assert math.isclose(floorplan.positions[3]["y"], 0.0)

    # Bounding box
    assert floorplan.bounding_box == (11.1, 6.0)

    # Area
    assert floorplan.area == 66.6


def test_sequence_pair_decode_vertically(example_problem, example_pair_vertically):  # noqa: F811
    seqpair = rps.SequencePair(pair=example_pair_vertically)
    floorplan = seqpair.decode(problem=rps.Problem(rectangles=example_problem))

    assert isinstance(floorplan, rps.Floorplan)
    assert isinstance(floorplan.positions, list)
    assert len(floorplan.positions) == 4
    assert isinstance(floorplan.bounding_box, tuple)
    assert len(floorplan.bounding_box) == 2
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

    # Bounding box
    assert floorplan.bounding_box == (4.0, 18.2)

    # Area
    assert floorplan.area == 72.8
