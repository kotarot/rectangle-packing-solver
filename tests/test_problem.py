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

import rectangle_packing_solver as rps
from example_data import example_problem  # noqa: F401


def test_problem_init(example_problem):  # noqa: F811
    problem = rps.Problem(rectangles=example_problem)

    assert problem.n == 4
    assert len(problem.rectangles) == 4

    # Rectangle id 0
    assert problem.rectangles[0]["id"] == 0
    assert problem.rectangles[0]["width"] == 4
    assert problem.rectangles[0]["height"] == 6
    assert not problem.rectangles[0]["rotatable"]

    # Rectangle id 1
    assert problem.rectangles[1]["id"] == 1
    assert problem.rectangles[1]["width"] == 4
    assert problem.rectangles[1]["height"] == 4
    assert not problem.rectangles[1]["rotatable"]

    # Rectangle id 2
    assert problem.rectangles[2]["id"] == 2
    assert problem.rectangles[2]["width"] == 2.1
    assert problem.rectangles[2]["height"] == 3.2
    assert not problem.rectangles[2]["rotatable"]

    # Rectangle id 3
    assert problem.rectangles[3]["id"] == 3
    assert problem.rectangles[3]["width"] == 1
    assert problem.rectangles[3]["height"] == 5
    assert problem.rectangles[3]["rotatable"]


def test_problem_type_error():
    with pytest.raises(TypeError):
        rps.Problem(rectangles="invalid type")

    with pytest.raises(TypeError):
        rps.Problem(rectangles=["invalid type"])
