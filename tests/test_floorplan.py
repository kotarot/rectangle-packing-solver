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

from tests.example_data import example_floorplan  # noqa: F401

import rectangle_packing_solver as rps


def test_floorplan_init_with_area(example_floorplan):  # noqa: F811
    floorplan = rps.Floorplan(
        positions=example_floorplan["positions"],
        bounding_box=example_floorplan["bounding_box"],
        area=example_floorplan["area"],
    )

    assert floorplan.positions == example_floorplan["positions"]
    assert floorplan.bounding_box == example_floorplan["bounding_box"]
    assert floorplan.area == example_floorplan["area"]


def test_floorplan_init_without_area(example_floorplan):  # noqa: F811
    floorplan = rps.Floorplan(
        positions=example_floorplan["positions"],
        bounding_box=example_floorplan["bounding_box"],
    )

    assert floorplan.positions == example_floorplan["positions"]
    assert floorplan.bounding_box == example_floorplan["bounding_box"]
    assert floorplan.area == example_floorplan["area"]


def test_floorplan_str(example_floorplan):  # noqa: F811
    floorplan = rps.Floorplan(
        positions=example_floorplan["positions"],
        bounding_box=example_floorplan["bounding_box"],
    )

    assert isinstance(floorplan.__str__(), str)
    assert "Floorplan({'positions': [{'id': 0, 'x': 0, 'y': 1}, {'id': 1, 'x': 4, 'y': 3.2}, {'id': 2, 'x': 5.0, 'y': 0.0}, {'id': 3, 'x': 0, 'y': 0}], 'bounding_box': (8, 7.2), 'area': 57.6})" in floorplan.__str__()
