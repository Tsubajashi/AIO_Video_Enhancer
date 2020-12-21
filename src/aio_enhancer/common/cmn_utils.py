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
#   Purpose: Utilities functions for easier life, managing paths, fail safety.
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
import shutil
import yaml
import sys
import os


class Utils:
    def __init__(self):
        # The operating system we're on, one of "linux", "windows", "macos"
        self.os = {
            "posix": "linux",
            "nt": "windows",
            "darwin": "macos"
        }.get(os.name)

    # Make directory if it does not exist
    def mkdir_dne(self, path, depth):
        debug_prefix = "[Utils.mkdir_dne]"

        logging.info(f"{depth}{debug_prefix} Make directory if it doesn't exist [{path}]")
        
        # Always get the absolute path 
        path = self.get_realpath_absolute(path, depth + "| ")

        # Create the directories
        logging.info(f"{depth}{debug_prefix} Create required directories")
        os.makedirs(path, exist_ok=True)

    # If a file is a symlink return where it points to
    # Not intended for usage outside this class, see get_realpath_absolute function for that
    def _get_realpath(self, path):
        realpath = os.path.realpath(path)

        # If it changed, warn it was a symlink
        if not realpath == path:
            print(f"[Utils._get_realpath] Realpath of [{path}] is [{realpath}")
            
        return realpath

    # Return an absolute path always, substitutes symlinks and so
    # Preferred functions when dealing with those. This function is kinda overkill
    # but it is kinda very safe, at least verbose enough to catch where stuff is wrong
    def get_realpath_absolute(self, path, depth):
        debug_prefix = "[Utils.get_realpath_absolute]"

        # Expand user "~" -> /home/$USER
        if (self.os == "linux") and ("~" in path):
            logging.info(f"{depth}{debug_prefix} [Linux] Expanding path with user home folder ~ to /home/$USER if any")
            path = os.path.expanduser(path)
       
        # Get the absolute path to a file, that is, if we're on /home/user/
        # we can type ./binary to execute a binary located at /home/user/binary
        # this is the absolute path, remember this can be a symlink still!!
        abspath = os.path.abspath(path)

        # Warn the absolute path we got
        logging.info(f"{depth}{debug_prefix} Absolute path of [{path}] is [{abspath}]")

        # Get the realpath (if it's a symlink get where it points to)
        return self._get_realpath(abspath)

    # Load a yaml and return its content
    def load_yaml(self, path, depth):
        debug_prefix = "[Utils.load_yaml]"
        
        # Info
        logging.info(f"{depth}{debug_prefix} Loading data from yaml [{path}]")
        
        # Get absolute and real path always
        path = self.get_realpath_absolute(path, depth + "| ")
        
        # Open the file in read mode and get the data dictionary
        with open(path, "r") as f:
            data = yaml.load(f, Loader = yaml.FullLoader)
        
        # Debug and return the data
        logging.debug(f"{depth}{debug_prefix} Loaded data is {data}")
        return data

    # Save a dictionary to a YAML file
    def dump_yaml(self, data, path, depth):
        debug_prefix = "[Utils.dump_yaml]"
        
        # Debug / info
        logging.info(f"{depth}{debug_prefix} Saving data to yaml file [{path}]")
        logging.debug(f"{depth}{debug_prefix} Saving data to yaml file [{path}], data: {data}")

        # Get absolute and real path always
        path = self.get_realpath_absolute(path, depth + "| ")
        
        # Open the file in write mode and overwrite with data dictionary
        with open(path, "w") as f:
            yaml.dump(data, f, allow_unicode = True, default_flow_style = False)

    # Remove a suffix from a string
    def removesuffix(self, string, suffix, depth):
        debug_prefix = "  [Utils.removesuffix]"
        logging.debug(f"{depth}{debug_prefix} Remove suffix [{suffix}] from string [{string}]")

        # Python 3.9 have a neat removesuffix method that should be more stable
        if sys.version_info >= (3, 9):
            done = string.removesuffix(suffix)
        else:
            # Manual way of doing it
            if string.endswith(suffix):
                done =  string[:-len(suffix)]

        # Debug and return
        logging.debug(f"{depth}{debug_prefix} String without that suffix is [{done}]")
        return done

    # Get a executable from path, returns None if it doesn't exist
    # Don't append the .exe for Windows, there is fail safe mechanism
    def get_executable_with_name(self, binary, depth, extra_paths = []):
        debug_prefix = "[Utils.get_executable_with_name]"

        # Force list and joing with this OS's pathsep "operator"
        extra_paths = self.force_list(extra_paths)
        extra_paths = os.pathsep.join(extra_paths)

        logging.debug(f"{depth}{debug_prefix} Getting executable with name [{binary}], also searching extra paths: [{extra_paths}]")
        assert (not binary.endswith(".exe")), "Don't append .exe when searching for binaries, this function already does that!"

        # Force list variable
        search_path = os.environ["PATH"] + os.pathsep + extra_paths

        # Locate it
        locate = shutil.which(binary, path = search_path)

        # If it's not found then return None
        if locate is None:
            return None
            
        # Else return its path
        return locate
    
    # If data is string, "abc" -> ["abc"], if data is list, return data
    def force_list(self, data):
        if not isinstance(data, list):
            data = [data]
        return data