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

class Problem:
    """
    A class to represent a rectangle packing problem.
    """

    def __init__(self, rectangles) -> None:
        self.rectangles = []
        self.n = 0

        if not isinstance(rectangles, list):
            raise TypeError("Invalid argument: 'rectangles' must be a list.")

        for r in rectangles:
            if isinstance(r, list):
                self.rectangles.append({
                    "id": self.n,
                    "width": r[0],
                    "height": r[1],
                    "rotatable": r[2] if len(r) >= 3 else False,
                })
            elif isinstance(r, dict):
                self.rectangles.append({
                    "id": self.n,
                    "width": r["width"],
                    "height": r["height"],
                    "rotatable": r["rotatable"] if "rotatable" in r else False,
                })
            else:
                raise TypeError("A rectangle must be a list or a dict.")

            self.n += 1


    def __repr__(self) -> str:
        s = "Problem({"
        s += "'n': " + str(self.n) + ", "
        s += "'rectangles': " + str(self.rectangles) + "})"

        return s
