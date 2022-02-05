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

import re

import rectangle_packing_solver as rps


def test_version_format():
    assert re.match(r"^\d+.\d+.\d+(.(dev|a|b|rc)\d+)?$", rps.__version__)


def test_version_info_format():
    ver_info = rps.__version_info__
    assert len(ver_info) in (3, 4)

    assert isinstance(ver_info[0], int)
    assert isinstance(ver_info[1], int)
    assert isinstance(ver_info[2], int)
    if len(ver_info) == 4:
        assert isinstance(ver_info[3], str)
