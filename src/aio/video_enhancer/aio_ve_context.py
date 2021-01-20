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

    # # Profile

    # Persistent database file across runs with GUI default configs, settings
    def load_profile(self, name):
        debug_prefix = "[AioVEnhancerContext.load_profile]"

        logging.debug(f"{debug_prefix} Attempting to load profile with name [{name}]")
        self.current_profile = name

        self.profile_yaml_path = f"{self.aio_ve_main.top_level_interface.profiles_dir}{os.path.sep}{name}"
        logging.debug(f"{debug_prefix} Profile YAML should be located at: [{self.profile_yaml_path}]")

        self.profile = self.aio_ve_main.utils.load_yaml(self.profile_yaml_path)

        logging.debug(f"{debug_prefix} AioVEnhancerContext.profiles is {self.profile}")

    # Create directories for a session and assigns to this Context's variables
    def setup_session(self, session_name):
        debug_prefix = "[AioVEnhancerContext.setup_session]"

        # Assign some shortcuts
        sessions_dir = self.aio_ve_main.aio_package_interface.sessions_dir
        self.session_name = session_name

        # Assign the directories
        self.session_dir =                        f"{sessions_dir}{os.path.sep}{self.session_name}"
        self.session_input_original_frames =      f"{self.session_dir}{os.path.sep}in_original_frames"
        self.session_output_upscaled_frames =     f"{self.session_dir}{os.path.sep}out_upscaled_frames"
        self.session_output_interpolated_frames = f"{self.session_dir}{os.path.sep}out_interpolated_frames"

        # Remove the session dir if it existed before
        self.aio_ve_main.utils.rmdir(self.session_dir)

        # Pretty print and make the directories
        for (key, value) in {
            "Session directory": self.session_dir,
            "Session's input original frames": self.session_input_original_frames,
            "Session's output upscaled frames": self.session_output_upscaled_frames,
            "Session's output interpolated frames": self.session_output_interpolated_frames,
        }.items():
            logging.info(f"{debug_prefix} {value} is [{key}]")
            self.aio_ve_main.utils.mkdir_dne(value)
