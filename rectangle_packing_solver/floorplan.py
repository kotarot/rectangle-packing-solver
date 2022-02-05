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

from typing import Dict, List, Tuple, Union


class Floorplan:
    """
    A class to represent a rectangle packing floorplan.
    """

    def __init__(self, positions: List[Dict], bounding_box: Tuple, area: Union[int, float] = -1.0) -> None:
        self.positions = positions
        self.bounding_box = bounding_box
        if 0 < area:
            self.area = area
        else:
            self.area = bounding_box[0] * bounding_box[1]

    def __repr__(self) -> str:
        s = "Floorplan({"
        s += "'positions': " + str(self.positions) + ", "
        s += "'bounding_box': " + str(self.bounding_box) + ", "
        s += "'area': " + str(self.area) + "})"

        return s
