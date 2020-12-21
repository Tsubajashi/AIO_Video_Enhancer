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
#   Purpose: Main file for interfacing with other scripts of the AIO Enhancer
# project.
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

from aio_enhancer.common.cmn_utils import Utils
from aio_enhancer.aio_context import AIOContext
from aio_enhancer.aio_core import AIOCore
import shelve
import shutil
import math
import sys
import os


class AIOEnhancerMain:
    def __init__(self):
        debug_prefix = "[AIO_EnhancerMain.__init__]"
        print(debug_prefix, "Hello World!!")

        # Greeter message and version telling
        self.misc = Miscellaneous()
        self.misc.greeter_message()

        # Where this file is located, please refer using this on the whole package
        # Refer to it as self.aio_main.DIR at any depth in the code
        # This deals with the case we used pyinstaller and it'll get the executable path
        if getattr(sys, 'frozen', True):    
            self.DIR = os.path.dirname(os.path.abspath(__file__))
            print(debug_prefix, "Running directly from source code")
            print(debug_prefix, f"AIO Enhancer Python package aio_enhancer [__init__.py] located at [{self.DIR}]")
        else:
            self.DIR = os.path.dirname(os.path.abspath(sys.executable))
            print(debug_prefix, "Running from release (sys.executable..?)")
            print(debug_prefix, f"AIO Enhancer executable located at [{self.DIR}]")

        # The operating system we're on, one of "linux", "windows", "macos"
        self.os = {
            "posix": "linux",
            "nt": "windows",
            "darwin": "macos"
        }.get(os.name)

        # # Create classes

        print(debug_prefix, "Creating Utils")
        self.utils = Utils()

        print(debug_prefix, "Creating AIOContext")
        self.context = AIOContext(self)

        print(debug_prefix, "Creating AIOCore")
        self.core = AIOCore(self)

        # Open database across runs, shelve acts like a dictionary as a file
        # it can even save entire objects, in face, any object that python can 
        # pickle and unpickle.
        self.database = shelve.open(self.context.paths.database_file)

    # Execute AIO main routine
    def run(self):
        self.core.run()


class Miscellaneous:
    def __init__(self) -> None:
        self.version = "0.0.1-GUI-BACKEND"

    def greeter_message(self) -> None:

        self.terminal_width = shutil.get_terminal_size()[0]

        bias = " "*(math.floor(self.terminal_width/2) - 36)
        version_text = f"Version {self.version}"

        if self.terminal_width >= 73:
            message = \
f"""{"-"*self.terminal_width}
{bias}     _     ___  ___    _____         _                                    
{bias}    / \   |_ _|/ _ \  | ____| _ __  | |__    __ _  _ __    ___  ___  _ __ 
{bias}   / _ \   | || | | | |  _|  | '_ \ | '_ \  / _` || '_ \  / __|/ _ \| '__|
{bias}  / ___ \  | || |_| | | |___ | | | || | | || (_| || | | || (__|  __/| |   
{bias} /_/   \_\|___|\___/  |_____||_| |_||_| |_| \__,_||_| |_| \___|\___||_|
{bias}
{bias}                         All in One Enhancer                      
{bias}{(73 - len(version_text))*" "}{version_text}
{"-"*self.terminal_width}
"""
        else:
            # The terminal screen is shorter for the fancy text at the top
            bias = " "*(math.floor(self.terminal_width/2) - 13 - math.floor(len(version_text)/2))
            message = \
f"""
{"-"*self.terminal_width}
{bias} [ All in One Enhancer | {version_text} ]
{"-"*self.terminal_width}
"""
        print(message)



    # Print a thanks messages with a few links
    def thanks_message(self):

        bias = " "*(math.floor(self.terminal_width/2) - 45)

        if self.terminal_width >= 90:
            message = \
f"""{"-"*self.terminal_width}\n
{bias}[+-------------------------------------------------------------------------------------+]
{bias} |                                                                                     |
{bias} |           ::    Thanks for using the All in One Enhancer Project!!    ::            |
{bias} |           ==============================================================            |
{bias} |                                                                                     |
{bias} | Here's a few official links for AIO Enhancer:                                       |
{bias} |                                                                                     |
{bias} |    - GitHub Repository:       [ https://github.com/Tsubajashi/AIO_Video_Enhancer ]  |
{bias} |                                                                                     |
{bias}[+-------------------------------------------------------------------------------------+]
\n{"-"*self.terminal_width}
"""
        else:
            message = \
f"""{"-"*self.terminal_width}\n
  # # [ Thanks for using the All in One Enhancer Project!! ] # #

 Here's a few official links for AIO Enhancer:
  - GitHub Repository: https://github.com/Tsubajashi/AIO_Video_Enhancer
\n{"-"*self.terminal_width}
"""
        print(message)
