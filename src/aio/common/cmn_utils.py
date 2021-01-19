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

import subprocess
import logging
import shutil
import yaml
import sys
import os


class Utils:
    def __init__(self):
        # The operating system we're on, one of "linux", "windows", "macos"
        self.os = {
            "posix":  "linux",
            "nt":     "windows",
            "darwin": "macos"
        }.get(os.name)

    # Make directory if it does not exist, alias for
    # $ mkdir -p dst
    def mkdir_dne(self, path, silent = False):
        debug_prefix = "[Utils.mkdir_dne]"

        if not silent:
            logging.info(f"{debug_prefix} Make directory if it doesn't exist [{path}]")
        
        # Always get the absolute path 
        path = self.get_realpath_absolute(path = path, silent = True)

        # Create the directories
        os.makedirs(path, exist_ok = True)
    
    # Deletes an directory, fail safe? Quits if we can't delete it..
    def rmdir(self, path, silent = False) -> None:
        debug_prefix = "[Utils.rmdir]"

        # If the asked directory is even a path
        if os.path.isdir(path):

            # Log action
            if not silent:
                logging.info(f"{debug_prefix} Removing dir: [{path}]")

            # Try removing with ignoring errors first..?
            shutil.rmtree(path, ignore_errors = True)

            # Not deleted? 
            if os.path.isdir(path):

                # Ok. We can't be silent here we're about to error out probably
                logging.warn(f"{debug_prefix} Error removing directory with ignore_errors=True, trying again.. will quit if we can't")

                # Remove without ignoring errors?
                shutil.rmtree(path, ignore_errors = False)

                # Still exists? oops, better quit
                if os.path.isdir(path):
                    logging.error(f"{debug_prefix} COULD NOT REMOVE DIRECTORY: [{path}]")
                    sys.exit(-1)

            # Warn we're done
            if not silent:
                logging.debug(f"{debug_prefix} Removed directory successfully")
        else:
            # Directory didn't exist at first, nothing to do here
            if not silent:
                logging.debug(f"{debug_prefix} Directory doesn't exists, nothing to do here... [{path}]")

    # $ mv A B
    def move(self, src, dst, silent = False) -> None:
        debug_prefix = "[Utils.move]"

        # Make sure we have the absolute and real path of the targets
        src = self.get_realpath_absolute(src, silent = True)
        dst = self.get_realpath_absolute(dst, silent = True)
        
        # Log action
        if not silent:
            logging.info(f"{debug_prefix} Moving path [{src}] -> [{dst}]")

        # Only move if the target directory doesn't exist
        if not os.path.exists(dst):
            shutil.move(src, dst)
        else:
            err = f"{debug_prefix} Target path already exist"
            logging.error(err)
            raise RuntimeError(err)
        
    # $ cp A B
    def copy(self, src, dst, silent = False) -> None:
        debug_prefix = "[Utils.copy]"

        # Make sure we have the absolute and real path of the targets
        src = self.get_realpath_absolute(src, silent = True)
        dst = self.get_realpath_absolute(dst, silent = True)

        # Log action
        if not silent:
            logging.info(f"{debug_prefix} Copying path [{src}] -> [{dst}]")

        # Copy the directories
        # Only move if the target directory doesn't exist
        if not os.path.exists(dst):
            shutil.copy(src, dst)
        else:
            err = f"{debug_prefix} Target path already exist"
            logging.error(err)
            raise RuntimeError(err)

    # If name is an file on PATH marked as executable returns True
    def has_executable_with_name(self, binary, silent = False) -> None:
        debug_prefix = "[Utils.has_executable_with_name]"

        # Log action
        if not silent:
            logging.info(f"{debug_prefix} Checking we can find the executable [{binary}] in PATH")

        # Tell if we can find the binary
        exists = shutil.which(binary) is not None

        # If it doesn't exist show warning, no need to quit
        if not silent:
            msg = f"{debug_prefix} Executable exists: [{exists}]"

            # Info if exists else warn
            if exists:
                logging.info(msg)
            else:
                logging.warn(msg)

        return exists
    
    # Get a executable from path, returns False if it doesn't exist
    def get_executable_with_name(self, binary, extra_paths = [], silent = False):
        debug_prefix = "[Utils.get_executable_with_name]"

        # Log action
        if not silent:
            logging.info(f"{debug_prefix} Get executable with name [{binary}]")

        # Force list variable
        extra_paths = self.force_list(extra_paths)
        search_path = os.environ["PATH"] + os.pathsep + os.pathsep.join(extra_paths)

        # Log search paths
        if not silent:
            logging.warn(f"{debug_prefix} Extra paths to search: [{extra_paths}]")
            logging.warn(f"{debug_prefix} Full search path: [{search_path}]")

        # Locate it
        locate = shutil.which(binary, path = search_path)

        # If it's not found then return False
        if locate is None:
            if not silent:
                logging.warn(f"{debug_prefix} Couldn't find binary, returning False..")
            return False
            
        # Else return its path
        if not silent:
            logging.info(f"{debug_prefix} Binary found and located at [{locate}]")

        return locate

    # If a file is a symlink return where it points to
    # Not intended for usage outside this class, see get_realpath_absolute function for that
    def _get_realpath(self, path, silent = False):
        debug_prefix = "[Utils._get_realpath]"

        realpath = os.path.realpath(path)

        # If it changed, warn it was a symlink
        if (not realpath == path) and (not silent):
            logging.info(f"{debug_prefix} Realpath of [{path}] is [{realpath}")
            
        return realpath

    # Return an absolute path always, substitutes symlinks and so
    # Preferred functions when dealing with those. This function is kinda overkill
    # but it is kinda very safe, at least verbose enough to catch where stuff is wrong
    def get_realpath_absolute(self, path, silent = False):
        debug_prefix = "[Utils.get_realpath_absolute]"

        # Expand user "~" -> /home/$USER
        if (self.os == "linux") and ("~" in path):
            if not silent:
                logging.info(f"{debug_prefix} [Linux] Expanding path with user home folder ~ to /home/$USER if any")
            path = os.path.expanduser(path)
       
        # Get the absolute path to a file, that is, if we're on /home/user/
        # we can type ./binary to execute a binary located at /home/user/binary
        # this is the absolute path, remember this can be a symlink still!!
        abspath = os.path.abspath(path)

        # Warn the absolute path we got
        if (not abspath == path) and (not silent):
            logging.info(f"{debug_prefix} Absolute path of [{path}] is [{abspath}]")

        got = self._get_realpath(path = abspath, silent = True)

        if not silent:
            logging.info(f"{debug_prefix} Returning absolute and real path [{got}]")

        # Get the realpath (if it's a symlink get where it points to)
        return got

    # Load a yaml and return its content
    def load_yaml(self, path, silent = False):
        debug_prefix = "[Utils.load_yaml]"
        
        # Info
        if not silent:
            logging.info(f"{debug_prefix} Loading data from yaml [{path}]")
        
        # Get absolute and real path always
        path = self.get_realpath_absolute(path, silent = True)
        
        # Open the file in read mode and get the data dictionary
        with open(path, "r") as f:
            data = yaml.load(f, Loader = yaml.FullLoader)
        
        # Debug and return the data
        if not silent:
            logging.debug(f"{debug_prefix} Loaded data is {data}")

        return data

    # Save a dictionary to a YAML file
    def dump_yaml(self, data, path, silent = False):
        debug_prefix = "[Utils.dump_yaml]"
        
        # Debug / info
        if not silent:
            logging.info(f"{debug_prefix} Saving data to yaml file [{path}]")
            logging.debug(f"{debug_prefix} Saving data to yaml file [{path}], data: {data}")

        # Get absolute and real path always
        path = self.get_realpath_absolute(path = path, silent = silent)
        
        # Open the file in write mode and overwrite with data dictionary
        with open(path, "w") as f:
            yaml.dump(data, f, allow_unicode = True, default_flow_style = False)

    # Remove a suffix from a string
    def removesuffix(self, string, suffix, silent = False):
        debug_prefix = "  [Utils.removesuffix]"
        
        if not silent:
            logging.debug(f"{debug_prefix} Remove suffix [{suffix}] from string [{string}]")

        # Python 3.9 have a neat removesuffix method that should be more stable, but for
        # compatibility reasons we'll use the manual one
        # if sys.version_info >= (3, 9):
        #     done = string.removesuffix(suffix)

        # Manual way of doing it
        if string.endswith(suffix):
            done =  string[:-len(suffix)]

        # Debug and return
        if not silent:
            logging.debug(f"{debug_prefix} String without that suffix is [{done}]")

        return done
    
    # If data is string, "abc" -> ["abc"], if data is list, return data
    def force_list(self, data):
        if not isinstance(data, list):
            data = [data]
        return data
    
    # Tries opening an URL for the user, platform independent
    def open_url(self, url):
        debug_prefix = "[Utils.open_url]"

        logging.debug(f"{debug_prefix} Try opening url [{url}] on this platform's browser")

        try:
            if self.os == "windows":
                os.startfile(url)  # NT only?
            elif self.os == "macos":
                subprocess.Popen(['open', url])  # Searched looks like this is the way?
            elif self.os == "linux":
                subprocess.Popen(['xdg-open', url])  # I know this works

        except Exception:
            raise RuntimeError(f"Somehow couldn't open the url [{url}] for your platform. Please open it on your browser manually instead")