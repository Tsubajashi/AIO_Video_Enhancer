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


# Context vars (configured stuff)
class AioVEnhancerContext:
    def __init__(self, aio_ve_main):
        debug_prefix = "[AioVEnhancerContext.__init__]"
        self.aio_ve_main = aio_ve_main

        # Runtime configuration (input video, output, last profile)
        self.runtime_file = f"{self.aio_ve_main.top_level_interface.runtime_dir}{os.path.sep}runtime.yaml"
        self.load_runtime()
        
    # On the directories.yaml we refer to the directory of the __init__.py with ~~
    # and replace / with the according os.path.sep
    def expand_dir(self, dir_string):
        debug_prefix = "[AioVEnhancerContext.expand_dir]"

        logging.debug(f"{debug_prefix} Expanding path [{dir_string}]")

        # The stuff we'll replace
        replaces =  {
            "~~": self.aio_ve_main.DIR,
            "/": os.path.sep,
        }

        # Replace every key on that replaces dict on the string
        for key, value in replaces.items():
            dir_string = dir_string.replace(key, value)
            logging.debug(f"{debug_prefix} | Replaced [{key} -> {value}]: Dir is [{dir_string}]")

        return self.aio_ve_main.utils.get_realpath_absolute(dir_string)

    # Load the runtime file (saves last profile, last input / output video configured)
    # Returns False if no file existed before, True if it existed
    def load_runtime(self):
        debug_prefix = "[AioVEnhancerContext.load_runtime]"

        # Did the runtime.yaml file exist? if not create the default and needed values
        existed = os.path.exists(self.runtime_file)
        
        if not existed:
            logging.info(f"{debug_prefix} Runtime file didn't exist (first time running program?), dumping default configs")

            self.runtime_dict = {
                "last_profile": "anime",
                "input_video": "",
                "output_video": "",
                "theme": "Dark",
            }

            self.save_current_runtime()
        else:
            self.runtime_dict = self.aio_ve_main.utils.load_yaml(self.runtime_file)

        logging.info(f"{debug_prefix} Loaded runtime.yaml, here's the values we got:")

        for key, value in self.runtime_dict.items():
            logging.info(f"{debug_prefix} [{key}]: [{value}]")

        return existed

    # Dump current runtime_dict into the runtime.yaml
    def save_current_runtime(self):
        debug_prefix = "[AioVEnhancerContext.save_runtime]"
        # logging.debug(f"{debug_prefix} Dumping current runtime_dict to runtime.yaml")
        self.aio_ve_main.utils.dump_yaml(self.runtime_dict, self.runtime_file, silent = True)

    # Wrapper for loading the profiled marked on the runtime.yaml config
    def load_profile_on_runtime_dict(self):
        self.load_profile(self.runtime_dict["last_profile"] + ".yaml")

    # # Profile

    # Persistent database file across runs with GUI default configs, settings
    def load_profile(self, name):
        debug_prefix = "[AioVEnhancerContext.load_database]"

        logging.debug(f"{debug_prefix} Attempting to load profile with name [{name}]")
        self.current_profile = name

        self.profile_yaml_path = f"{self.aio_ve_main.top_level_interface.profiles_dir}{os.path.sep}{name}"
        logging.debug(f"{debug_prefix} Profile YAML should be located at: [{self.profile_yaml_path}]")

        self.profile = self.aio_ve_main.utils.load_yaml(self.profile_yaml_path)

        logging.debug(f"{debug_prefix} AioVEnhancerContext.profiles is {self.profile}")
