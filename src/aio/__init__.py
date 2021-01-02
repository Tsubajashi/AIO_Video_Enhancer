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
#   Purpose: Top level interface / package mostly for keeping stuff organized.
# Highly abstracted (sorta), distributes needed directories and whatnot.
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

from aio.common.wrappers.wrapper_ffmpeg import FFmpegWrapper
from aio.common.cmn_download import Download
from aio.common.cmn_utils import Utils
import subprocess
import tempfile
import logging
import struct
import shutil
import toml
import math
import sys
import os


class TopLevelInterface:

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

    # Return the subpackage "video_enhancer" interface class
    def get_video_enhancer_interface(self):
        debug_prefix = "[AIOPackageInterface.get_video_enhancer_interface]"

        logging.info(f"{debug_prefix} Return VEInterface")
        
        from aio.video_enhancer import AioVEInterface
        return AioVEInterface(top_level_interface = self)

    # Return one (usually required) setting up encoder
    def get_ffmpeg_wrapper(self):
        debug_prefix = "[AIOPackageInterface.get_ffmpeg_wrapper]"

        logging.info(f"{debug_prefix} Return FFmpegWrapper")
        
        return FFmpegWrapper(
            ffmpeg_binary = self.find_binary("ffmpeg"),
            ffprobe_binary = self.find_binary("ffprobe")
        )

    # Main interface class, mainly sets up root dirs, get config, distributes classes
    def __init__(self, **kwargs) -> None:
        debug_prefix = "[AIOPackageInterface.__init__]"

        # Versioning
        self.version = "0.0.1-GUI-BACKEND"

        # Greeter message :)
        self.greeter_message()

        # # Get this file's path

        sep = os.path.sep

        # Where this file is located, please refer using this on the whole package
        # Refer to it as self.aio_ve_main.top_level_interface.AIO_PACKAGE_ROOT at any depth in the code
        # This deals with the case we used pyinstaller and it'll get the executable path instead
        # Preferable use some directories we create here later one like externals_dir, data_dir
        if getattr(sys, 'frozen', True):    
            self.AIO_PACKAGE_ROOT = os.path.dirname(os.path.abspath(__file__))
            print(f"{debug_prefix} Running directly from source code")
            print(f"{debug_prefix} All in One Video Enhancer top level [aio] Python package [__init__.py] located at [{self.AIO_PACKAGE_ROOT}]")
        else:
            self.AIO_PACKAGE_ROOT = os.path.dirname(os.path.abspath(sys.executable))
            print(f"{debug_prefix} Running from release (sys.executable..?)")
            print(f"{debug_prefix} All in One Video Enhancer executable located at [{self.AIO_PACKAGE_ROOT}]")

        # # Load prelude configuration

        print(f"{debug_prefix} Loading prelude configuration file")
        
        # Build the path the prelude file should be located at
        prelude_file = f"{self.AIO_PACKAGE_ROOT}{sep}prelude.toml"

        print(f"{debug_prefix} Attempting to load prelude file located at [{prelude_file}], we cannot continue if this is wrong..")

        # Load the prelude file
        with open(prelude_file, "r") as f:
            self.prelude = toml.loads(f.read())
        
        print(f"{debug_prefix} Loaded prelude configuration file, data: [{self.prelude}]")

        # # # Logging 

        # # We can now set up logging as we have where this file is located at

        # # Reset current handlers if any
        
        print(f"{debug_prefix} Resetting Python's logging logger handlers to empty list")

        # Get logger and empty the list
        logger = logging.getLogger()
        logger.handlers = []

        # Handlers on logging to file and shell output, the first one if the user says to
        handlers = [logging.StreamHandler(sys.stdout)]

        # Loglevel is defined in the prelude.toml configuration
        LOG_LEVEL = {
            "critical": logging.CRITICAL,
            "debug": logging.DEBUG,
            "error": logging.ERROR,
            "info": logging.INFO,
            "warn": logging.WARN,
            "notset": logging.NOTSET,
        }.get(self.prelude["logging"]["log_level"])

        # If user chose to log to a file, add its handler..
        if self.prelude["logging"]["log_to_file"]:

            # Hard coded where the log file will be located
            # this is only valid for the last time we run this software
            self.LOG_FILE = f"{self.AIO_PACKAGE_ROOT}{sep}last_log.log"

            # Reset the log file
            with open(self.LOG_FILE, "w") as f:
                print(f"{debug_prefix} Reset log file located at [{self.LOG_FILE}]")
                f.write("")

            # Verbose and append the file handler
            print(f"{debug_prefix} Reset log file located at [{self.LOG_FILE}]")
            handlers.append(logging.FileHandler(filename = self.LOG_FILE, encoding = 'utf-8'))

        # .. otherwise just keep the StreamHandler to stdout

        log_format = {
            "informational": "[%(levelname)-8s] [%(filename)-32s:%(lineno)-3d] (%(relativeCreated)-6d) %(message)s",
            "pretty": "[%(levelname)-8s] (%(relativeCreated)-5d)ms %(message)s",
            "economic": "[%(levelname)s::%(filename)s::%(lineno)d] %(message)s",
            "onlymessage": "%(message)s"
        }.get(self.prelude["logging"]["log_format"])

        # Start the logging global class, output to file and stdout
        logging.basicConfig(
            level = LOG_LEVEL,
            format = log_format,
            handlers = handlers,
        )

        # Start logging message
        bias = " " * ((self.terminal_width//2) - 13);
        print("\n" + "-" * self.terminal_width + "\n")
        print(f"{bias[:-1]}# # [ Start Logging ] # #\n")
        print("-" * self.terminal_width + "\n")

        # Log what we'll do next
        logging.info(f"{debug_prefix} We're done with the pre configuration of Python's behavior and loading prelude.toml configuration file")

        # Log prelude configuration
        logging.info(f"{debug_prefix} Prelude configuration is {self.prelude}")

        # Log precise Python version
        sysversion = sys.version.replace("\n", " ").replace("  ", " ")
        logging.info(f"{debug_prefix} Running on Python: [{sysversion}]")

        # # The operating system we're on, one of "linux", "windows", "macos"

        # Get the desired name from a dict matching against os.name
        self.os = {
            "posix": "linux",
            "nt": "windows",
            "darwin": "macos"
        }.get(os.name)

        # Log which OS we're running
        logging.info(f"{debug_prefix} Running on Operating System: [{self.os}]")
        logging.info(f"{debug_prefix} (os.path.sep) is [{sep}]")

        # # Create interface's classes

        logging.info(f"{debug_prefix} Creating Utils() class")
        self.utils = Utils()

        logging.info(f"{debug_prefix} Creating Download() class")
        self.download = Download()

        # # Common directories between packages

        # Externals dir
        self.externals_dir = f"{self.AIO_PACKAGE_ROOT}{sep}externals"
        logging.info(f"{debug_prefix} Externals directory is [{self.externals_dir}]")
        self.utils.mkdir_dne(path = self.externals_dir)

        # Downloads (inside externals)
        self.downloads_dir = f"{self.AIO_PACKAGE_ROOT}{sep}externals{sep}downloads"
        logging.info(f"{debug_prefix} Downloads dir is [{self.downloads_dir}]")
        self.utils.mkdir_dne(path = self.downloads_dir)

        # Runtime dir
        self.runtime_dir = f"{self.AIO_PACKAGE_ROOT}{sep}runtime"
        logging.info(f"{debug_prefix} Runtime directory is [{self.runtime_dir}]")
        self.utils.mkdir_dne(path = self.runtime_dir)

        # Data dir
        self.data_dir = f"{self.AIO_PACKAGE_ROOT}{sep}data"
        logging.info(f"{debug_prefix} Data dir is [{self.data_dir}]")

        # Configuration dir
        self.config_dir = f"{self.AIO_PACKAGE_ROOT}{sep}config"
        logging.info(f"{debug_prefix} Config dir is [{self.config_dir}]")

        # Sessions dir
        self.sessions_dir = f"{self.AIO_PACKAGE_ROOT}{sep}sessions"
        logging.info(f"{debug_prefix} Sessions directory is [{self.sessions_dir}]")
        self.utils.mkdir_dne(path = self.sessions_dir)

        # Windoe juuuust in case
        if self.os == "windows":
            logging.info(f"{debug_prefix} Appending the Externals directory to system path juuuust in case...")
            sys.path.append(self.externals_dir)

        # # External dependencies where to append for PATH

        # When using some function like Utils.get_executable_with_name, it have an argument
        # called extra_paths, add this for searching for the full externals directory.
        # Preferably use this interface methods like find_binary instead
        self.EXTERNALS_SEARCH_PATH = [
            self.externals_dir
        ]

        # Code flow management
        if self.prelude["flow"]["stop_at_initialization"]:
            logging.critical(f"{debug_prefix} Exiting as stop_at_initialization key on prelude.toml is True")
            sys.exit(0)
        
    # Search for something in system's PATH, also searches for the externals folder
    # Don't append the extra .exe because Linux, macOS doesn't have these
    def find_binary(self, binary):
        debug_prefix = "[AIOPackageInterface.find_binary]"

        # Log action
        logging.info(f"{debug_prefix} Finding binary in PATH and EXTERNALS directories: [{binary}]")

        found = self.utils.get_executable_with_name(binary, extra_paths = self.EXTERNALS_SEARCH_PATH)
        logging.info(f"{debug_prefix} Got: [{found}]")

        return found

    # Make sure we have FFmpeg. Linux people please install from your distro's package manager
    # For forcing to download the Windows binaries for a release, please send making_release=True
    def download_check_ffmpeg(self, making_release = False):
        debug_prefix = "[AIOPackageInterface.download_check_ffmpeg]"

        # Log action
        logging.info(f"{debug_prefix} Checking for FFmpeg on Linux or downloading for Windows / if (making release: [{making_release}]")

        if getattr(sys, 'frozen', False):
            logging.info(f"{debug_prefix} Not checking ffmpeg.exe because is executable build.. (should have ffmpeg.exe bundled?)")
            return

        sep = os.path.sep

        # If the code is being run on a Windows OS
        if (self.os == "windows") or (making_release):

            if making_release:
                logging.info(f"{debug_prefix} Getting FFmpeg for Windows regardless the OS because making_release=True")

            # Where we should find the ffmpeg binary
            FINAL_FFMPEG_FINAL_BINARY = self.externals_dir + f"{sep}ffmpeg.exe"
            FINAL_FFPROBE_FINAL_BINARY = self.externals_dir + f"{sep}ffprobe.exe"

            # If we don't have FFmpeg binary on externals dir
            if not os.path.isfile(FINAL_FFMPEG_FINAL_BINARY):

                # Get the latest release number of ffmpeg
                ffmpeg_release = self.download.get_html_content("https://www.gyan.dev/ffmpeg/builds/release-version")
                logging.info(f"{debug_prefix} FFmpeg release number is [{ffmpeg_release}]")

                # Where we'll save the compressed zip of FFmpeg
                ffmpeg_7z = self.downloads_dir + f"{sep}ffmpeg-{ffmpeg_release}-essentials_build.7z"

                # Download FFmpeg build
                self.download.wget(
                    "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.7z",
                    ffmpeg_7z, f"FFmpeg v={ffmpeg_release}"
                )

                # Extract the files
                self.download.extract_file(ffmpeg_7z, self.downloads_dir)

                # Where the FFmpeg binary is located and move it
                ffmpeg_bin = ffmpeg_7z.replace(".7z", "") + f"{sep}bin{sep}ffmpeg.exe"
                self.utils.move(ffmpeg_bin, FINAL_FFMPEG_FINAL_BINARY)

                # Where the FFprobe binary is located and move it
                ffprobe_bin = ffmpeg_7z.replace(".7z", "") + f"{sep}bin{sep}ffprobe.exe"
                self.utils.move(ffprobe_bin, FINAL_FFPROBE_FINAL_BINARY)

            else:
                logging.info(f"{debug_prefix} Already have [ffmpeg.exe] downloaded and extracted at [{FINAL_FFMPEG_FINAL_BINARY}]")
        else:
            # We're on Linux so checking ffmpeg external dependency
            logging.info(f"{debug_prefix} You are using Linux, please make sure you have FFmpeg package installed on your distro, we'll just check for it now..")
            
            # Can't continue
            if not self.utils.has_executable_with_name("ffmpeg"):
                logging.error(f"{debug_prefix} Couldn't find lowercase ffmpeg binary on PATH, install from your Linux distro package manager / macOS homebrew")


