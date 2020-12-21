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
import logging
import shelve
import shutil
import math
import yaml
import sys
import os


class AIOEnhancerMain:
    def __init__(self):
        debug_prefix = "[AIOEnhancerMain.__init__]"
        self.version = "0.0.1-GUI-BACKEND"

        # Greeter message and version telling
        self.greeter_message()

        print(debug_prefix, "Hello World!! Need to find the directory we're at and reset the log file before actually logging")

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
        
        # Hard coded where the log file will be located
        # this is only valid for the last time we run this software
        self.LOG_FILE = f"{self.DIR}{os.path.sep}log.log"

        # Reset the log file
        with open(self.LOG_FILE, "w") as f:
            print(f"{debug_prefix} Reset log file located at [{self.LOG_FILE}]")
            f.write("")

        # # We can now set up logging as we have where this file is located at

        # Handlers on logging to file and shell output
        log_to_file_handler = logging.FileHandler(filename = self.LOG_FILE)
        log_to_stdout_handler = logging.StreamHandler(sys.stdout)

        # Start the logging global class
        logging.basicConfig(
            encoding = 'utf-8',
            level = logging.DEBUG,
            format = "[%(levelname)-7s] [%(filename)-15s:%(lineno)-3d] %(message)s",
            handlers = [log_to_file_handler, log_to_stdout_handler],
        )

        print("\n # # [ Start Logging ] # #\n")

        # Log the version we're running
        logging.warn(f"{debug_prefix} All in One Video Enhancer version [{self.version}]")

        # Log where this source file / executable is
        logging.debug(f"{debug_prefix} AIOVE located at: [{self.DIR}], [getattr(sys, 'frozen', True) = {getattr(sys, 'frozen', True)}]")

        # # The operating system we're on, one of "linux", "windows", "macos"

        # Get the desired name from a dict matching against os.name
        self.os = {
            "posix": "linux",
            "nt": "windows",
            "darwin": "macos"
        }.get(os.name)

        # Log which OS we're runnig
        logging.info(f"{debug_prefix} Running All in Onne Video Enhancer on OS: [{self.os}]")

        # # Create classes

        logging.info(f"{debug_prefix} Creating Utils")
        self.utils = Utils()

        logging.info(f"{debug_prefix} Creating AIOContext")
        self.context = AIOContext(self)

        logging.info(f"{debug_prefix} Creating AIOCore")
        self.core = AIOCore(self)

        # Open database across runs, shelve acts like a dictionary as a file
        # it can even save entire objects, in face, any object that python can 
        # pickle and unpickle. If it doesn't exist that means we create a new
        # one with some default configuration
        os.remove(self.context.paths.database_file) # FIXME: HARD DEBUG
        existed = os.path.exists(self.context.paths.database_file)
        self.database = shelve.open(self.context.paths.database_file, "c")  # Open in change mode

        # Is this first time running AIO?
        logging.info(f"{debug_prefix} Database file existed: [{existed}]")

        # Database file didn't exist, add default configuration
        if not existed:
            logging.warn(f"{debug_prefix} Adding default configuration to database file")
            
            # Default configuration for AIOVE
            default_config = {
                "something": 3,
                "other": 5,
                "list": {
                    "subdir": "that/path",
                    "asjkd": "those/files",
                }
            }

            # Assign every default config key to the shelf database
            for key, value in default_config.items():
                self.database[key] = value

        # Hard debug, create a dictionary of the database file and dump to yaml
        debug_data = yaml.dump(
            {k: v for k, v in self.database.items()},
            allow_unicode = True,
            default_flow_style = False
        ).split("\n")  # Split into a list of lines so we can visualize better the debug info
        
        logging.debug(f"{debug_prefix} [SHELVE] Contents of database file:")

        # Log every line of the database if it's not empty (we should have a trailing char here ie. ignore it)
        for line in debug_data:
            if not line == "": logging.debug(f"{debug_prefix} [SHELVE] | {line}")

    # Execute AIO main routine
    def run(self):
        logging.info(f"[AIOEnhancerMain.run] Executing AIOCore.run()")
        self.core.run()


    # # QOL / greeter / thanks messages


    def greeter_message(self):

        self.terminal_width = shutil.get_terminal_size()[0]

        bias = " "*(math.floor(self.terminal_width/2) - 36)
        version_text = f"Version {self.version}"

        if self.terminal_width >= 73:
            message = \
f"""{"-"*self.terminal_width}
{bias}     _     ___  ___    _____         _                                    
{bias}    / \\   |_ _|/ _ \\  | ____| _ __  | |__    __ _  _ __    ___  ___  _ __ 
{bias}   / _ \\   | || | | | |  _|  | '_ \\ | '_ \\  / _` || '_ \\  / __|/ _ \\| '__|
{bias}  / ___ \\  | || |_| | | |___ | | | || | | || (_| || | | || (__|  __/| |   
{bias} /_/   \\_\\|___|\\___/  |_____||_| |_||_| |_| \\__,_||_| |_| \\___|\\___||_|
{bias}
{bias}                       All in One Video Enhancer                      
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

        self.terminal_width = shutil.get_terminal_size()[0]

        bias = " "*(math.floor(self.terminal_width/2) - 45)

        if self.terminal_width >= 90:
            message = \
f"""\n{"-"*self.terminal_width}\n
{bias}[+-------------------------------------------------------------------------------------+]
{bias} |                                                                                     |
{bias} |           :: Thanks for using the All in One Video Enhancer Project!! ::            |
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
  # # [ Thanks for using the All in One Video Enhancer Project!!! ] # #

 Here's a few official links for AIO Enhancer:
  - GitHub Repository: https://github.com/Tsubajashi/AIO_Video_Enhancer
\n{"-"*self.terminal_width}
"""
        print(message)
