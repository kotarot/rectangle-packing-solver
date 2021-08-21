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

import pytest


@pytest.fixture
def example_problem():
    rectangles = [
        [4, 6],
        (4, 4),
        {"width": 2.1, "height": 3.2, "rotatable": False},
        {"width": 1, "height": 5, "rotatable": True},
    ]
    return rectangles


@pytest.fixture
def example_pair_horizontally():
    # By this pair of sequences, all of the four rectangles are aligned in a strait line horizontally.
    gp = [0, 1, 2, 3]
    gn = [0, 1, 2, 3]
    pair = (gp, gn)
    return pair


@pytest.fixture
def example_pair_vertically():
    # By this pair of sequences, all of the four rectangles are aligned in a strait line vertically.
    gp = [0, 1, 2, 3]
    gn = [3, 2, 1, 0]
    pair = (gp, gn)
    return pair


@pytest.fixture
def example_pair():
    gp = [0, 1, 3, 2]
    gn = [3, 0, 2, 1]
    pair = (gp, gn)
    return pair


@pytest.fixture
def example_floorplan():
    return {
        "positions": [{"id": 0, "x": 0, "y": 1}, {"id": 1, "x": 4, "y": 3.2}, {"id": 2, "x": 5.0, "y": 0.0}, {"id": 3, "x": 0, "y": 0}],
        "bounding_box": (8, 7.2),
        "area": 57.6,
    }
