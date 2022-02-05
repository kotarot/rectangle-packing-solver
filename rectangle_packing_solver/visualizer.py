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

from typing import Tuple

import matplotlib.patches as patches
from matplotlib import pylab as plt

from .solution import Solution


class Visualizer:
    """
    A floorplan visualizer.
    """

    def __init__(self) -> None:
        # Default font size is 12
        plt.rcParams["font.size"] = 14

    def visualize(self, solution: Solution, path: str = "floorplan.png", title: str = "Floorplan") -> None:
        if not isinstance(solution, Solution):
            raise TypeError("Invalid argument: 'solution' must be an instance of Solution.")

        positions = solution.floorplan.positions
        bounding_box = solution.floorplan.bounding_box

        # Figure settings
        bb_width = bounding_box[0]
        bb_height = bounding_box[1]
        fig = plt.figure(figsize=(10, 10 * bb_height / bb_width + 0.5))
        ax = plt.axes()
        ax.set_aspect("equal")
        plt.xlim([0, bb_width])
        plt.ylim([0, bb_height])
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.title(title)

        # Plot every rectangle
        for i, rectangle in enumerate(positions):
            color, fontcolor = self.get_color(i)
            r = patches.Rectangle(
                xy=(rectangle["x"], rectangle["y"]),
                width=rectangle["width"],
                height=rectangle["height"],
                edgecolor="#000000",
                facecolor=color,
                alpha=1.0,
                fill=True,
            )
            ax.add_patch(r)

            # Add text label
            centering_offset = 0.011
            center_x = rectangle["x"] + rectangle["width"] / 2 - bb_width * centering_offset
            center_y = rectangle["y"] + rectangle["height"] / 2 - bb_height * centering_offset
            ax.text(x=center_x, y=center_y, s=rectangle["id"], fontsize=18, color=fontcolor)

        # Output
        if path is None:
            plt.show()
        else:
            fig.savefig(path)

        plt.close()

    @classmethod
    def get_color(cls, i: int = 0) -> Tuple[str, str]:
        """
        Gets rectangle face color (and its font color) from matplotlib cmap.
        """
        cmap = plt.get_cmap("tab10")
        color = cmap(i % cmap.N)
        brightness = max(color[0], color[1], color[2])

        if 0.85 < brightness:
            fontcolor = "#000000"
        else:
            fontcolor = "#ffffff"

        return (color, fontcolor)
