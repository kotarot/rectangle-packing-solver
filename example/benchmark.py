#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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

import random
import time

import rectangle_packing_solver as rps


def generate_rectangles(n=10, range_width=(1, 100), range_height=(1, 100)):
    rectangles = []
    for i in range(n):
        rectangles.append((
            random.randint(range_width[0], range_width[1]),
            random.randint(range_height[0], range_height[1])
        ))
    return rectangles


def main():
    random.seed(12345)

    n_rectangles = list(range(4, 10)) + list(range(10, 50, 10))
    for n in n_rectangles:
        print("\n================")
        print("N =", n)

        rectangles = generate_rectangles(n=n)
        problem = rps.Problem(rectangles=rectangles)
        print("problem:", problem)

        solver = rps.Solver()

        start = time.time()
        solution = solver.solve(problem, simanneal_minutes=0.1, simanneal_steps=100)
        elapsed_time = time.time() - start
        print("solution:", solution)
        print(solution.floorplan.bounding_box, solution.floorplan.area)
        print("elapsed_time:", elapsed_time)


if __name__ == "__main__":
    main()
