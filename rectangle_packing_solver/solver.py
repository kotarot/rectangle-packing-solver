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

import os
import random
import signal
import sys
from contextlib import redirect_stderr
from typing import List, Optional, Tuple

import simanneal

from .problem import Problem
from .sequence_pair import SequencePair
from .solution import Solution


def exit_handler(signum, frame) -> None:  # type: ignore
    """
    Since `simaaneal` traps SIGINT, we override it.
    """
    sys.exit(1)


class Solver:
    """
    A rectangle packing solver.
    """

    def __init__(self) -> None:
        pass

    def solve(
        self,
        problem: Problem,
        width_limit: Optional[float] = None,
        height_limit: Optional[float] = None,
        simanneal_minutes: float = 0.1,
        simanneal_steps: int = 100,
    ) -> Solution:
        if not isinstance(problem, Problem):
            raise TypeError("Invalid argument: 'problem' must be an instance of Problem.")

        # Initial state (= G_{+} + G_{-} + rotations)
        init_gp = list(range(problem.n))
        init_gn = list(range(problem.n))
        init_rot = [0 for _ in range(problem.n)]
        init_state = init_gp + init_gn + init_rot

        # Get rid of output (stderr) from simanneal in this "with" block
        rpp = RectanglePackingProblemAnnealer(
            state=init_state, problem=problem, width_limit=width_limit, height_limit=height_limit
        )
        signal.signal(signal.SIGINT, exit_handler)
        with redirect_stderr(open(os.devnull, "w")):
            rpp.copy_strategy = "slice"  # We use "slice" since the state is a list
            rpp.set_schedule(rpp.auto(minutes=simanneal_minutes, steps=simanneal_steps))
            final_state, _ = rpp.anneal()

        # Convert simanneal's final_state to a Solution object
        gp, gn, rotations = rpp.retrieve_pairs(n=problem.n, state=final_state)
        seqpair = SequencePair(pair=(gp, gn))
        floorplan = seqpair.decode(problem=problem, rotations=rotations)

        return Solution(sequence_pair=seqpair, floorplan=floorplan)


class RectanglePackingProblemAnnealer(simanneal.Annealer):
    """
    Annealer for the rectangle packing problem.
    """

    def __init__(
        self,
        state: List[int],
        problem: Problem,
        width_limit: Optional[float] = None,
        height_limit: Optional[float] = None,
    ) -> None:
        self.seqpair = SequencePair()
        self.problem = problem

        # The max possible width and height to deal with the size limit.
        self.max_possible_width = sum(
            [max(r["width"], r["height"]) if r["rotatable"] else r["width"] for r in problem.rectangles]
        )
        self.max_possible_height = sum(
            [max(r["width"], r["height"]) if r["rotatable"] else r["height"] for r in problem.rectangles]
        )

        self.width_limit = sys.float_info.max
        if width_limit:
            self.width_limit = width_limit
        self.height_limit = sys.float_info.max
        if height_limit:
            self.height_limit = height_limit
        self.state: List[int] = []
        super(RectanglePackingProblemAnnealer, self).__init__(state)

    def move(self) -> float:
        """
        Move state (sequence-pair) and return the energy diff.
        """

        initial_energy: float = self.energy()
        initial_state: List[int] = self.state[:]

        # Choose two indices and swap them
        i, j = random.sample(range(self.problem.n), k=2)  # The first and second index
        offset = random.randint(0, 1) * self.problem.n  # Choose G_{+} (=0) or G_{-} (=1)

        # Swap them (i != j always holds true)
        self.state[i + offset], self.state[j + offset] = initial_state[j + offset], initial_state[i + offset]

        # Random rotation
        if self.problem.rectangles[i]["rotatable"]:
            if random.randint(0, 1) == 1:
                self.state[i + 2 * self.problem.n] = initial_state[i + 2 * self.problem.n] + 1

        # A solution whose width/height limit is not satisfied has a larger energy.
        # We adopt a valid solution as the annealing steps proceeds.
        energy = self.energy()

        return energy - initial_energy

    def energy(self) -> float:
        """
        Calculates the area of bounding box.
        """

        # Pick up sequence-pair and rotations from state
        gp, gn, rotations = self.retrieve_pairs(n=self.problem.n, state=self.state)
        seqpair = SequencePair(pair=(gp, gn))
        floorplan = seqpair.decode(problem=self.problem, rotations=rotations)

        # Returns the max possible area, if width/height limit is not satisfied.
        # This solution could be chosen in the earlier steps of the annealing,
        # but would not be chosen in the later steps.
        if floorplan.bounding_box[0] > self.width_limit:
            return self.max_possible_width * self.max_possible_height
        if floorplan.bounding_box[1] > self.height_limit:
            return self.max_possible_width * self.max_possible_height

        return float(floorplan.area)

    @classmethod
    def retrieve_pairs(cls, n: int, state: List[int]) -> Tuple[List[int], List[int], List[int]]:
        """
        Retrieve G_{+}, G_{-}, and rotations from a state.
        """
        gp = state[0:n]
        gn = state[n : 2 * n]
        rotations = state[2 * n : 3 * n]
        return (gp, gn, rotations)
