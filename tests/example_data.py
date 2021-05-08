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
        {"width": 4, "height": 4},
        {"width": 2.1, "height": 3.2, "rotatable": False},
        {"width": 1, "height": 5, "rotatable": True},
    ]
    return rectangles


@pytest.fixture
def example_pair():
    gp = [0, 1, 2, 3]
    gn = [3, 2, 1, 0]
    pair = (gp, gn)
    return pair
