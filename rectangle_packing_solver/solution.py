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

from .sequence_pair import SequencePair


class Solution:
    """
    A class to represent a rectangle packing solution.
    """

    def __init__(self, sequence_pair, floorplan) -> None:
        self.sequence_pair = sequence_pair
        self.floorplan = floorplan


    def __repr__(self) -> str:
        s = "Solution({"
        s += "'sequence_pair': " + str(self.sequence_pair) + ", "
        s += "'floorplan': " + str(self.floorplan) + "})"

        return s
