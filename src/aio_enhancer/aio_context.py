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
import sys
import os


# Manage and store where directories should be
class AIOPaths:
    def __init__(self, aio_main):
        debug_prefix = "[AIOPaths.__init__]"
        self.aio_main = aio_main
    
        # Path separator, / on unix and \\ on Windows
        sep = os.path.sep
        logging.debug(f"{debug_prefix} OS path separador is [{sep}]")

        # # # Paths


        # # Hard coded // expected

        # Config directory
        
        # Where we store data such as configs, gui, profiles
        self.config_dir = f"{self.aio_main.DIR}{sep}config"
        logging.info(f"{debug_prefix} [EXPECTED] Config directory is [{self.config_dir}]")

        # Error assertion, config dir should exist
        logging.info(f"{debug_prefix} Checking existing config directory (it should?)")
        if not os.path.exists(self.config_dir):
            logging.error(f"{debug_prefix} Config directory [{self.config_dir}] doesn't exists.."); sys.exit(-1)

        # Where we store persistent profile information across runs
        self.database_file = f"{self.config_dir}{sep}database.shelf"
        logging.info(f"{debug_prefix} Database file is [{self.database_file}]")


        # # User configured paths

        # Load directories.yaml
        self.config_directories = self.aio_main.utils.load_yaml(f"{self.config_dir}{sep}directories.yaml")

        # # Sessions
        # Where we store sessions, extract videos and so
        self.sessions_dir = self.expand_dir(self.config_directories["global"]["sessions_folder"])
        logging.info(f"{debug_prefix} Sessions directory is [{self.sessions_dir}]")


    # On the directories.yaml we refer to the directory of the __init__.py with ~~
    # and replace / with the according os.path.sep
    def expand_dir(self, string):
        replaces =  {
            "~~": self.aio_main.DIR,
            "/": os.path.sep,
        }

        # Replace every key on that replaces dict on the string
        for key, value in replaces.items():
            string = string.replace(key, value)

        return string

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
