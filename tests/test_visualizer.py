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

import mimetypes

import rectangle_packing_solver as rps
from tests.example_data import example_problem  # noqa: F401


def test_visualizer(example_problem):  # noqa: F811
    problem = rps.Problem(rectangles=example_problem)
    solver = rps.Solver()
    solution = solver.solve(problem=problem, simanneal_minutes=0.01, simanneal_steps=10)

    rps.Visualizer().visualize(solution=solution, path="./floorplan.png")

    mimetype = mimetypes.guess_type("./floorplan.png")[0]
    assert mimetype == "image/png"
