# Copyright 2022 Kotaro Terada
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
import signal
import sys
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

        # If width/height limits are not given...
        if (width_limit is None) and (height_limit is None):
            return self._solve_with_constraints_strategy(
                problem, width_limit, height_limit, simanneal_minutes, simanneal_steps, constraints_strategy="soft"
            )

        # If width/height limits are given...
        if width_limit is None:
            width_limit = sys.float_info.max
        if height_limit is None:
            height_limit = sys.float_info.max
        max_width = max([min(r["width"], r["height"]) if r["rotatable"] else r["width"] for r in problem.rectangles])
        max_height = max([min(r["width"], r["height"]) if r["rotatable"] else r["height"] for r in problem.rectangles])
        if width_limit < max_width:
            raise ValueError(
                f"'width_limit' must be greater than or equal to {max_width} "
                + "(= the largest width of the given problem)."
            )
        if height_limit < max_height:
            raise ValueError(
                f"'height_limit' must be greater than or equal to {max_height} "
                + "(= the largest height of the given problem)."
            )

        # If constraints of width and/or hight are given,
        # we will use two kinds of annealer in a hybrid way.
        # - 1) Soft constraints strategy:
        #      Find a solution with smallest area as possible, the width/height limits may not be met.
        # - 2) Hard constraints strategy:
        #      Find a solution so that the width/height limits must be met. Sometimes no solutions will be found.
        solution_soft = self._solve_with_constraints_strategy(
            problem, width_limit, height_limit, simanneal_minutes, simanneal_steps, constraints_strategy="soft"
        )
        try:
            solution_hard = self._solve_with_constraints_strategy(
                problem, width_limit, height_limit, simanneal_minutes, simanneal_steps, constraints_strategy="hard"
            )
        except HardToFindSolutionException:
            return solution_soft

        is_constraints_met_soft = (solution_soft.floorplan.bounding_box[0] <= width_limit) and (
            solution_soft.floorplan.bounding_box[1] <= height_limit
        )
        is_constraints_met_hard = (solution_hard.floorplan.bounding_box[0] <= width_limit) and (
            solution_hard.floorplan.bounding_box[1] <= height_limit
        )
        if solution_soft.floorplan.area < solution_hard.floorplan.area:
            solution_smaller = solution_soft
        else:
            solution_smaller = solution_hard
        if is_constraints_met_soft and is_constraints_met_hard:
            return solution_smaller
        elif is_constraints_met_soft:
            return solution_soft
        elif is_constraints_met_hard:
            return solution_hard
        else:
            return solution_smaller

    def _solve_with_constraints_strategy(
        self,
        problem: Problem,
        width_limit: Optional[float] = None,
        height_limit: Optional[float] = None,
        simanneal_minutes: float = 0.1,
        simanneal_steps: int = 100,
        constraints_strategy: str = None,
    ) -> Solution:
        # Initial state (= G_{+} + G_{-} + rotations)
        init_gp = list(range(problem.n))
        if width_limit and (width_limit < sys.float_info.max):
            # Flat along with vertical line
            init_gn = list(reversed(list(range(problem.n))))
        else:
            # Flat along with horizontal line
            init_gn = list(range(problem.n))
        init_rot = [0 for _ in range(problem.n)]
        init_state = init_gp + init_gn + init_rot

        if constraints_strategy == "soft":
            rpp = RectanglePackingProblemAnnealerSoft(
                state=init_state, problem=problem, width_limit=width_limit, height_limit=height_limit
            )
        elif constraints_strategy == "hard":
            rpp = RectanglePackingProblemAnnealerHard(
                state=init_state, problem=problem, width_limit=width_limit, height_limit=height_limit
            )
        else:
            raise ValueError("'constraints_strategy' must be either of ['soft', 'hard'].")

        signal.signal(signal.SIGINT, exit_handler)
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
    The base class of the Annealer for the rectangle packing problem.
    """

    @classmethod
    def retrieve_pairs(cls, n: int, state: List[int]) -> Tuple[List[int], List[int], List[int]]:
        """
        Retrieve G_{+}, G_{-}, and rotations from a state.
        """
        gp = state[0:n]
        gn = state[n : 2 * n]
        rotations = state[2 * n : 3 * n]
        return (gp, gn, rotations)


class RectanglePackingProblemAnnealerSoft(RectanglePackingProblemAnnealer):
    """
    Annealer for the rectangle packing problem.
    This annealer is based on Soft constraints strategy. In other words, it can't be helped that it may find a
    solution violating constraints.
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

        self.width_limit: float = sys.float_info.max
        if width_limit:
            self.width_limit = width_limit
        self.height_limit: float = sys.float_info.max
        if height_limit:
            self.height_limit = height_limit
        self.state: List[int] = []
        self._step: int = 0
        super(RectanglePackingProblemAnnealerSoft, self).__init__(state)

    def update(self, step: int, T: int, E: float, acceptance: float, improvement: float) -> None:
        """
        Override the default_update method.
        Purpose: Introduce steps, and disable stderr output.
        """
        self._step = step

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
        # We would like to adopt a valid solution as the annealing steps proceeds.
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


class RectanglePackingProblemAnnealerHard(RectanglePackingProblemAnnealer):
    """
    Annealer for the rectangle packing problem.
    This annealer is based on Hard constraints strategy. In other words, it must find only a solution satisfying
    constraints. If it is hard to find a solution satisfying hard constraints, the annealer raises
    HardToFindSolutionException.
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

        self.width_limit: float = sys.float_info.max
        if width_limit:
            self.width_limit = width_limit
        self.height_limit: float = sys.float_info.max
        if height_limit:
            self.height_limit = height_limit
        self.state: List[int] = []
        self._step: int = 0
        super(RectanglePackingProblemAnnealerHard, self).__init__(state)

    def update(self, step: int, T: int, E: float, acceptance: float, improvement: float) -> None:
        """
        Override the default_update method.
        Purpose: Introduce steps, disable stderr output.
        """
        self._step = step

    def move(self) -> float:
        """
        Move state (sequence-pair) and return the energy diff.
        """
        initial_energy: float = self.energy()
        initial_state: List[int] = self.state[:]

        # Maximum the number of trial: 100
        for _ in range(100):
            # Choose two indices and swap them
            i, j = random.sample(range(self.problem.n), k=2)  # The first and second index
            offset = random.randint(0, 1) * self.problem.n  # Choose G_{+} (=0) or G_{-} (=1)

            # Swap them (i != j always holds true)
            self.state[i + offset], self.state[j + offset] = initial_state[j + offset], initial_state[i + offset]

            # Random rotation
            if self.problem.rectangles[i]["rotatable"]:
                if random.randint(0, 1) == 1:
                    self.state[i + 2 * self.problem.n] = initial_state[i + 2 * self.problem.n] + 1

            # We adopt solution if the solution width/height limit is satisfied
            energy = self.energy()
            if energy < sys.float_info.max:
                break

            # Restore the state
            self.state = initial_state[:]

        else:
            raise HardToFindSolutionException

        return energy - initial_energy

    def energy(self) -> float:
        """
        Calculates the area of bounding box.
        """

        # Pick up sequence-pair and rotations from state
        gp, gn, rotations = self.retrieve_pairs(n=self.problem.n, state=self.state)
        seqpair = SequencePair(pair=(gp, gn))
        floorplan = seqpair.decode(problem=self.problem, rotations=rotations)

        # Returns float max, if width/height limit is not satisfied
        if floorplan.bounding_box[0] > self.width_limit:
            return sys.float_info.max
        if floorplan.bounding_box[1] > self.height_limit:
            return sys.float_info.max

        return float(floorplan.area)


class HardToFindSolutionException(Exception):
    """
    When it is hard to find a solution, this exception is raised.
    """

    pass
