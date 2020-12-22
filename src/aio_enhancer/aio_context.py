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
import shelve
import yaml
import sys
import os


# Manage and store where directories should be
class AIOPaths:
    def __init__(self, aio_main, depth):
        debug_prefix = "[AIOPaths.__init__]"
        self.aio_main = aio_main
    
        # Path separator, / on unix and \\ on Windows
        sep = os.path.sep
        logging.debug(f"{depth}{debug_prefix} OS path separador is [{sep}]")

        # # # Directories

        # Where we store data such as configs, gui, profiles
        self.data_dir = f"{self.aio_main.DIR}{sep}data"
        logging.info(f"{depth}{debug_prefix} (expect) Data directory is [{self.data_dir}]")

        # External stuff like ffmpeg, ffprobe
        self.externals_dir = f"{self.aio_main.DIR}{sep}externals"
        logging.info(f"{depth}{debug_prefix} (expect) Externals directory is [{self.externals_dir}]")

        # # Static // expected paths on the data directory

        self.profiles_dir = f"{self.data_dir}{sep}profiles"
        logging.info(f"{depth}{debug_prefix} (expect) Profiles directory is [{self.profiles_dir}]")
        
        self.config_dir = f"{self.data_dir}{sep}config"
        logging.info(f"{depth}{debug_prefix} (expect) Config directory is [{self.config_dir}]")

        self.defaults_dir = f"{self.data_dir}{sep}defaults"
        logging.info(f"{depth}{debug_prefix} (expect) Defaults directory is [{self.defaults_dir}]")

        # # # Files

        # # Static // expected file paths

        self.runtime_file = f"{self.data_dir}{sep}runtime.yaml"

        # # User configured directories
        
        # Load directories.yaml
        self.data_directories = self.aio_main.utils.load_yaml(f"{self.data_dir}{sep}config{sep}directories.yaml", depth + "| ")

        # Sessions directory set by the user
        self.sessions_dir = self.expand_dir(self.data_directories["global"]["sessions_folder"], depth + "| ")
        logging.info(f"{depth}{debug_prefix} Sessions directory is [{self.sessions_dir}]")


    # On the directories.yaml we refer to the directory of the __init__.py with ~~
    # and replace / with the according os.path.sep
    def expand_dir(self, dir_string, depth):
        debug_prefix = "[AIOPaths.expand_dir]"

        logging.debug(f"{depth}{debug_prefix} Expanding path [{dir_string}]")

        # The stuff we'll replace
        replaces =  {
            "~~": self.aio_main.DIR,
            "/": os.path.sep,
        }

        # Replace every key on that replaces dict on the string
        for key, value in replaces.items():
            dir_string = dir_string.replace(key, value)
            logging.debug(f"{depth}{debug_prefix} | Replaced [{key} -> {value}]: Dir is [{dir_string}]")

        return self.aio_main.utils.get_realpath_absolute(dir_string, depth + "| ")

# Free real state for changing, modifying runtime dependent vars
# Not really any specification here
class AIORuntime:
    def __init__(self, aio_main):
        debug_prefix = "[AIORuntime.__init__]"
        self.aio_main = aio_main

    # # Runtime

    # Load the runtime file (saves last profile, last input / output video configured)
    # Returns False if no file existed before, True if it existed
    def load_runtime(self, depth):
        debug_prefix = "[AIORuntime.load_runtime]"

        # Did the runtime.yaml file exist? if not create the default and needed values
        existed = os.path.exists(self.aio_main.context.paths.runtime_file)
        
        if not existed:
            logging.info(f"{depth}{debug_prefix} Runtime file didn't exist (first time running program?), dumping default configs")

            self.runtime_dict = {
                "last_profile": "anime",
                "input_video": "",
                "output_video": "",
            }

            self.save_current_runtime(depth + "| ")
        else:
            self.runtime_dict = self.aio_main.utils.load_yaml(self.aio_main.context.paths.runtime_file, depth + "| ")

        logging.info(f"{depth}{debug_prefix} Loaded runtime.yaml, here's the values we got:")

        for key, value in self.runtime_dict.items():
            logging.info(f"{depth}{debug_prefix} [{key}]: [{value}]")

        return existed

    # Dump current runtime_dict into the runtime.yaml
    def save_current_runtime(self, depth):
        debug_prefix = "[AIORuntime.save_runtime]"
        # logging.debug(f"{depth}{debug_prefix} Dumping current runtime_dict to runtime.yaml")
        self.aio_main.utils.dump_yaml(self.runtime_dict, self.aio_main.context.paths.runtime_file, depth + "| ", silent = True)

    # Wrapper for loading the profiled marked on the runtime.yaml config
    def load_profile_on_runtime_dict(self, depth):
        self.load_profile(self.runtime_dict["last_profile"] + ".yaml", depth + "| ")

    # # Profile

    # Persistent database file across runs with GUI default configs, settings
    def load_profile(self, name, depth):
        debug_prefix = "[AIORuntime.load_database]"

        logging.debug(f"{depth}{debug_prefix} Attempting to load profile with name [{name}]")
        self.current_profile = name

        self.profile_yaml_path = f"{self.aio_main.context.paths.profiles_dir}{os.path.sep}{name}"
        logging.debug(f"{depth}{debug_prefix} Profile YAML should be located at: [{self.profile_yaml_path}]")

        self.profile = self.aio_main.utils.load_yaml(self.profile_yaml_path, depth + "| ")

# Context vars (configured stuff)
class AIOContext:
    def __init__(self, aio_main, depth):
        debug_prefix = "[AIOContext.__init__]"
        self.aio_main = aio_main
        
        logging.info(f"{depth}{debug_prefix} Creating AIOPaths")
        self.paths = AIOPaths(self.aio_main, depth + "| ")

        logging.info(f"{depth}{debug_prefix} Creating AIORuntime")
        self.runtime = AIORuntime(self.aio_main)
