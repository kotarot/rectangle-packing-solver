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
from contextlib import redirect_stderr

import simanneal

from .problem import Problem
from .solution import Solution
from .sequence_pair import SequencePair


class Solver:
    """
    A rectangle packing solver.
    """

    def __init__(self) -> None:
        pass

    def solve(self, problem, simanneal_minutes=0.1, simanneal_steps=100):
        if not isinstance(problem, Problem):
            raise TypeError("Invalid argument: 'problem' must be an instance of Problem.")

        # Initial state (= G_{+} + G_{-} + rotations)
        init_gp = list(range(problem.n))
        init_gn = list(range(problem.n))
        init_rot = [0 for _ in range(problem.n)]
        init_state = init_gp + init_gn + init_rot

        # Get rid of output (stderr) from simanneal in this "with" block
        rpp = RectanglePackingProblemAnnealer(state=init_state, problem=problem)
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

    def __init__(self, state, problem) -> None:
        self.seqpair = SequencePair()
        self.problem = problem
        super(RectanglePackingProblemAnnealer, self).__init__(state)

    def move(self):
        """
        Move state (sequence-pair) and return the energy diff.
        """

        initial_energy = self.energy()

        # Choose two indices and swap them
        i = random.randint(0, self.problem.n - 1)  # The first index
        j = random.randint(0, self.problem.n - 1)  # The second index
        offset = random.randint(0, 1) * self.problem.n  # Choose G_{+} (=0) or G_{-} (=1)

        # Swap
        if i != j:
            self.state[i + offset], self.state[j + offset] = self.state[j + offset], self.state[i + offset]

        # Random rotation
        if self.problem.rectangles[i]["rotatable"]:
            if random.randint(0, 1) == 1:
                self.state[i + 2 * self.problem.n] += 1

        return self.energy() - initial_energy

    def energy(self):
        """
        Calculates the area of boundary box.
        """

        # Pick up sequence-pair and rotations from state
        gp, gn, rotations = self.retrieve_pairs(n=self.problem.n, state=self.state)
        seqpair = SequencePair(pair=(gp, gn))
        floorplan = seqpair.decode(problem=self.problem, rotations=rotations)

        return floorplan.area

    @classmethod
    def retrieve_pairs(cls, n, state):
        """
        Retrieve G_{+}, G_{-}, and rotations from a state.
        """
        gp = state[0:n]
        gn = state[n : 2 * n]  # noqa: E203
        rotations = state[2 * n : 3 * n]  # noqa: E203
        return (gp, gn, rotations)
