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
    def mkdir_dne(self, path):
        debug_prefix = "  [Utils.mkdir_dne]"

        print(debug_prefix, f"Make directory if it doesn't exist [{path}]")
        
        # Always get the absolute path 
        path = self.get_realpath_absolute(path)

        # Create the directories
        print(debug_prefix, f"Create required directories")
        os.makedirs(path, exist_ok=True)

    # If a file is a symlink return where it points to
    # Not intended for usage outside this class, see get_realpath_absolute function for that
    def _get_realpath(self, path):
        realpath = os.path.realpath(path)

        # If it changed, warn it was a symlink
        if not realpath == path:
            print(f"  [Utils._get_realpath] Realpath of [{path}] is [{realpath}")
            
        return realpath

    # Return an absolute path always, substitutes symlinks and so
    # Preferred functions when dealing with those.
    def get_realpath_absolute(self, path):
        debug_prefix = "  [Utils.get_abspath]"

        # Expand user "~" -> /home/$USER
        if (self.os == "linux") and ("~" in path):
            print(debug_prefix, "[Linux] Expanding path with user home folder ~ to /home/$USER if any")
            path = os.path.expanduser(path)
       
        # Get the absolute path to a file, that is, if we're on /home/user/
        # we can type ./binary to execute a binary located at /home/user/binary
        # this is the absolute path, remember this can be a symlink still!!
        abspath = os.path.abspath(path)

        print(debug_prefix, f"Absolute path of [{path}] is [{abspath}]")

        return self._get_realpath(abspath)
    
