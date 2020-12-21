# ==============================================================================
#
# MIT License
#
# Copyright (c) 2020,
#  - Tremeschin < https://tremeschin.gitlab.io > 
#  - Tsubajashi < https://github.com/Tsubajashi >
#
# ==============================================================================
#
#   Purpose: Deal with "contextual" variables (settings) like video width,
# height, frames per second or runtime dependent vars, pre configured paths
# for storing databases, configuration scripts, etc.
#
# ==============================================================================
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# ==============================================================================
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# ==============================================================================
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# ==============================================================================

import logging
import os


# Manage and store where directories should be
class AIOPaths:
    def __init__(self, aio_main):
        debug_prefix = "[AIOPaths.__init__]"
        self.aio_main = aio_main
    
        # Path separator, / on unix and \\ on Windows
        sep = os.path.sep

        # # Paths

        # Where we store data such as configs, gui, profiles
        self.data_path = f"{self.aio_main.DIR}{sep}data"
        logging.info(f"{debug_prefix} Data path is [{self.data_path}]")

        # # Files

        # Where we store persistent profile information
        self.database_file = f"{self.data_path}{sep}database.shelf"
        logging.info(f"{debug_prefix} Database file is [{self.database_file}]")

        # # Create / check stuff

        logging.info(f"{debug_prefix} Creating data path if it doesn't exist (it should?)")
        self.aio_main.utils.mkdir_dne(self.data_path)


# Free real state for changing, modifying runtime dependent vars
# Not really any specification here
class AIORuntime:
    def __init__(self, aio_main):
        debug_prefix = "[AIORuntime.__init__]"
        self.aio_main = aio_main


# Context vars (configured stuff)
class AIOContext:
    def __init__(self, aio_main):
        debug_prefix = "[AIOContext.__init__]"
        self.aio_main = aio_main
        
        logging.info(f"{debug_prefix} Creating AIOPaths")
        self.paths = AIOPaths(self.aio_main)

        logging.info(f"{debug_prefix} Creating AIORuntime")
        self.runtime = AIORuntime(self.aio_main)
