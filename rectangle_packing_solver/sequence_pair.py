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

import graphlib
from typing import Any, Dict, List, Optional, Tuple

from .floorplan import Floorplan
from .problem import Problem


class ObliqueGrid:
    def __init__(self, grid: List[List[int]], coordinates: List[Dict]) -> None:
        self.grid = grid
        self.coordinates = coordinates


class SequencePair:
    """
    A class of Sequence-Pair.
    """

    def __init__(self, pair: Tuple[List, List] = ([], [])) -> None:
        if not isinstance(pair, tuple):
            raise TypeError("Invalid argument: 'pair' must be a tuple.")
        if len(pair) != 2:
            raise ValueError("Invalid argument: Length of 'pair' must be two.")

        self.pair = pair
        self.gp = pair[0]  # G_{+}
        self.gn = pair[1]  # G_{-}

        if len(self.gp) != len(self.gn):
            raise ValueError("Lists in the pair must be the same length.")
        self.n = len(self.gp)

        self.oblique_grid = self.pair_to_obliquegrid(pair=self.pair)

    def decode(self, problem: Problem, rotations: Optional[List] = None) -> Floorplan:
        """
        Decode:
            Based on the sequence pair and the problem with rotations information, calculate a floorplan
            (bounding box, area, and rectangle positions).
        """

        if not isinstance(problem, Problem):
            raise TypeError("Invalid argument: 'problem' must be an instance of Problem.")

        if problem.n != self.n:
            raise ValueError("'problem.n' must be the same as the sequence-pair length.")

        if rotations is not None:
            if len(rotations) != self.n:
                raise ValueError("'rotations' length must be the same as the sequence-pair length.")

        coords = self.oblique_grid.coordinates

        # Width and height dealing with rotations
        width_wrot = []
        height_wrot = []
        for i in range(self.n):
            if (rotations is None) or (rotations[i] % 2 == 0):
                # no rotation
                width_wrot.append(problem.rectangles[i]["width"])
                height_wrot.append(problem.rectangles[i]["height"])
            else:
                # with rotation
                assert problem.rectangles[i]["rotatable"]
                width_wrot.append(problem.rectangles[i]["height"])
                height_wrot.append(problem.rectangles[i]["width"])

        # Calculate the longest path in the "Horizontal Constraint Graph" (G_h)
        # This time complexity is O(n^2), may be optimized...
        graph_h: Dict[int, List] = {i: [] for i in range(self.n)}
        for i in range(self.n):
            for j in range(self.n):
                # When j is right of i, set an edge from j to i
                if (coords[i]["a"] < coords[j]["a"]) and (coords[i]["b"] < coords[j]["b"]):
                    graph_h[j].append(i)

        # Topological order of DAG (G_h)
        topo_h = graphlib.TopologicalSorter(graph_h)
        torder_h = list(topo_h.static_order())

        # Calculate W (bounding box width) from G_h
        dist_h = [width_wrot[i] for i in range(self.n)]
        for i in torder_h:
            dist_h[i] += max([dist_h[e] for e in graph_h[i]], default=0)
        bb_width = max(dist_h)

        # Calculate the longest path in the "Vertical Constraint Graph" (G_v)
        # This time complexity is O(n^2), may be optimized...
        graph_v: Dict[int, List] = {i: [] for i in range(self.n)}
        for i in range(self.n):
            for j in range(self.n):
                # When j is above i, set an edge from j to i
                if (coords[i]["a"] > coords[j]["a"]) and (coords[i]["b"] < coords[j]["b"]):
                    graph_v[j].append(i)

        # Topological order of DAG (G_v)
        topo_v = graphlib.TopologicalSorter(graph_v)
        torder_v = list(topo_v.static_order())

        # Calculate H (bounding box height) from G_v
        dist_v = [height_wrot[i] for i in range(self.n)]
        for i in torder_v:
            dist_v[i] += max([dist_v[e] for e in graph_v[i]], default=0)
        bb_height = max(dist_v)

        # Calculate bottom-left positions
        positions = []
        for i in range(self.n):
            positions.append(
                {
                    "id": i,
                    "x": dist_h[i] - width_wrot[i],  # distance from left edge
                    "y": dist_v[i] - height_wrot[i],  # distande from bottom edge
                    "width": width_wrot[i],
                    "height": height_wrot[i],
                }
            )

        return Floorplan(bounding_box=(bb_width, bb_height), positions=positions)

    def encode(self) -> None:
        """
        Encode:
            TODO
        """
        raise NotImplementedError()

    def __repr__(self) -> str:
        return "SequencePair(" + str(self.pair) + ")"

    @classmethod
    def pair_to_obliquegrid(cls, pair: Tuple[List, List]) -> ObliqueGrid:
        """
        Convert a Sequence-pair (a tuple of G_{+} and G_{-}) to Oblique-grid.
        """

        n = len(pair[0])
        gp = pair[0]
        gn = pair[1]

        # Oblique grid is basically an n x n 2d array
        grid = [[-1 for _ in range(n)] for _ in range(n)]
        coordinates = [{"a": -1, "b": -1} for _ in range(n)]

        # This time complexity is O(n^2), may be optimized...
        for i in range(n):
            index_p = gp.index(i)
            index_n = gn.index(i)
            grid[index_p][index_n] = i
            coordinates[i] = {"a": index_p, "b": index_n}

        return ObliqueGrid(grid=grid, coordinates=coordinates)

    @classmethod
    def obliquegrid_to_pair(cls, oblique_grid: ObliqueGrid) -> Tuple[List, List]:
        """
        Convert an Oblique-grid to Sequence-pair (a tuple of G_{+} and G_{-}).
        """

        n = len(oblique_grid.grid)
        gp = [-1 for _ in range(n)]  # G_{+}
        gn = [-1 for _ in range(n)]  # G_{-}

        # This time complexity is O(n^2), may be optimized...
        for x in range(n):
            for y in range(n):
                rectangle_id = oblique_grid.grid[x][y]
                if rectangle_id != -1:
                    gp[x] = rectangle_id
                    gn[y] = rectangle_id

        return (gp, gn)

    ################################################################
    # Operators
    ################################################################

    def __eq__(self, other: Any) -> Any:
        return self.pair == other.pair

    def __ne__(self, other: Any) -> Any:
        return not self.__eq__(other)
