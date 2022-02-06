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
from typing import Any, List, Optional, Tuple

import simanneal
from tqdm.auto import tqdm

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
        show_progress: bool = False,
        seed: Optional[int] = None,
    ) -> Solution:
        if seed:
            random.seed(seed)

        if not isinstance(problem, Problem):
            raise TypeError("Invalid argument: 'problem' must be an instance of Problem.")

        # If width/height limits are not given...
        if (width_limit is None) and (height_limit is None):
            return self._solve_with_strategy(
                problem, width_limit, height_limit, None, simanneal_minutes, simanneal_steps, show_progress, strategy="hard"
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
        # we can use two kinds of annealer in a hybrid way.
        # - 1) Hard constraints strategy:
        #      Find a solution so that the width/height limits must be met. Sometimes no solutions will be found.
        # - 2) Soft constraints strategy:
        #      Find a solution with smallest area as possible, the width/height limits may not be met.
        if (width_limit < sys.float_info.max) and (height_limit < sys.float_info.max):
            return self._solve_with_strategy(
                problem, width_limit, height_limit, None, simanneal_minutes, simanneal_steps, show_progress, strategy="soft"
            )
        else:
            return self._solve_with_strategy(
                problem, width_limit, height_limit, None, simanneal_minutes, simanneal_steps, show_progress, strategy="hard"
            )

    def _solve_with_strategy(
        self,
        problem: Problem,
        width_limit: Optional[float] = None,
        height_limit: Optional[float] = None,
        initial_state: Optional[List[int]] = None,
        simanneal_minutes: float = 0.1,
        simanneal_steps: int = 100,
        show_progress: bool = False,
        strategy: str = None,
    ) -> Solution:
        if not initial_state:
            # Initial state (= G_{+} + G_{-} + rotations)
            if width_limit and (width_limit < sys.float_info.max):
                # As flat as possible along with vertical line
                init_gp = list(range(problem.n))
                init_gn = list(reversed(list(range(problem.n))))
                init_rot = [1 if r["rotatable"] and r["width"] > r["height"] else 0 for r in problem.rectangles]
            elif height_limit and (height_limit < sys.float_info.max):
                # As flat as possible along with horizontal line
                init_gp = list(range(problem.n))
                init_gn = list(range(problem.n))
                init_rot = [1 if r["rotatable"] and r["width"] < r["height"] else 0 for r in problem.rectangles]
            else:
                # Random sequence pair (shuffle)
                init_gp = random.sample(list(range(problem.n)), k=problem.n)
                init_gn = random.sample(list(range(problem.n)), k=problem.n)
                init_rot = [0 for _ in range(problem.n)]
            init_state = init_gp + init_gn + init_rot
        else:
            init_state = initial_state

        if strategy == "hard":
            rpp = RectanglePackingProblemAnnealerHard(
                state=init_state, problem=problem, width_limit=width_limit, height_limit=height_limit, show_progress=show_progress
            )
        elif strategy == "soft":
            rpp = RectanglePackingProblemAnnealerSoft(
                state=init_state, problem=problem, width_limit=width_limit, height_limit=height_limit, show_progress=show_progress
            )
        else:
            raise ValueError("'strategy' must be either of ['hard', 'soft'].")

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

    def __init__(
        self,
        state: List[int],
        problem: Problem,
        width_limit: Optional[float] = None,
        height_limit: Optional[float] = None,
        show_progress: bool = False,
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
        self._step: int = 0  # Current annealing step
        self._prev_step: int = 0  # Previous step in the update method
        self._annealing_phase: bool = False  # Annealing phase: True / Auto phase: False
        self._progress: Any = None  # tqdm progress bar
        self._show_progress: bool = show_progress
        super(RectanglePackingProblemAnnealer, self).__init__(state)

    def update(self, step: int, T: int, E: float, acceptance: float, improvement: float) -> None:
        """
        Override the default_update method.
        Purpose: Introduce steps, disable stderr output, and progress visualization.
        """
        self._step = step
        if self._annealing_phase and self._show_progress:
            self._progress.update(step - self._prev_step)
            self._prev_step = step

    def anneal(self) -> Tuple[Any]:
        """
        Override the anneal method for progress visualization.
        """
        self._annealing_phase = True
        if self._show_progress:
            self._progress = tqdm(total=self.steps, desc="Progress")
        return super().anneal()

    @classmethod
    def retrieve_pairs(cls, n: int, state: List[int]) -> Tuple[List[int], List[int], List[int]]:
        """
        Retrieve G_{+}, G_{-}, and rotations from a state.
        """
        gp = state[0:n]
        gn = state[n : 2 * n]
        rotations = state[2 * n : 3 * n]
        return (gp, gn, rotations)


class RectanglePackingProblemAnnealerHard(RectanglePackingProblemAnnealer):
    """
    Annealer for the rectangle packing problem.
    This annealer is based on Hard constraints strategy. In other words, it must find only a solution satisfying
    constraints. If it is hard to find a solution satisfying hard constraints, the annealer raises
    HardToFindSolutionException.
    """

    def move(self) -> float:
        """
        Move state (sequence-pair) and return the energy diff.
        """
        initial_energy: float = self.energy()
        initial_state: List[int] = self.state[:]

        # Maximum the number of trial: 10000
        for _ in range(10000):
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


class RectanglePackingProblemAnnealerSoft(RectanglePackingProblemAnnealer):
    """
    Annealer for the rectangle packing problem.
    This annealer is based on Soft constraints strategy. In other words, it can't be helped that it may find a
    solution violating constraints.
    """

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
            return self.max_possible_width * self.max_possible_height + floorplan.area
        if floorplan.bounding_box[1] > self.height_limit:
            return self.max_possible_width * self.max_possible_height + floorplan.area

        return float(floorplan.area)


class HardToFindSolutionException(Exception):
    """
    When it is hard to find a solution, this exception is raised.
    """

    pass
