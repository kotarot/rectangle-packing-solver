#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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

import re
from codecs import open
from os import path

import setuptools

package_name = "rectangle-packing-solver"
package_path = package_name.replace("-", "_")

root_dir = path.abspath(path.dirname(__file__))

with open(path.join(root_dir, package_path, "__version__.py"), encoding="utf8") as f:
    version = re.search(r"__version__\s*=\s*[\'\"](.+?)[\'\"]", f.read()).group(1)

with open(path.join(root_dir, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name=package_name,
    packages=setuptools.find_packages(),
    version=version,
    license="Apache 2.0",
    install_requires=[
        "simanneal>=0.5.0,<1.0.0",
        "graphlib-backport>=1.0.3,<2.0.0",  # TODO: Drop this when we drop 3.8 support
    ],
    extras_require={
        "dev": [
            # For test
            "pytest>=6.2.4,<7.0.0",
            # For lint
            "black>=21.5b0,<22.0",
            "flake8>=3.9.1,<4.0.0",
            "isort>=5.8.0,<6.0.0",
            "mypy>=0.812,<1.0",
        ],
    },
    author="Kotaro Terada",
    author_email="kotarot@apache.org",
    url="https://github.com/kotarot/rectangle-packing-solver",
    description="A solver to find a solution for the 2D rectangle packing problem by simulated annealing (SA) optimization.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="python rectangle-packing placement optimization simulated-annealing",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.9",
    ],
)
