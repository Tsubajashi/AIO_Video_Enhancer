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
from aio.common.wrappers.wrapper_rife import RifeWrapper
from aio.video_enhancer import AioVEInterface
from aio.common.cmn_download import Download
from aio.common.cmn_utils import Utils
import subprocess
import tempfile
import logging
import struct
import shutil
import json
import toml
import math
import sys
import os


class AIOPackageInterface:

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
        return AioVEInterface(aio_package_interface = self)

    # Return one (usually required) setting up encoder
    def get_ffmpeg_wrapper(self):
        debug_prefix = "[AIOPackageInterface.get_ffmpeg_wrapper]"
        logging.info(f"{debug_prefix} Return FFmpegWrapper")
        return FFmpegWrapper(
            ffmpeg_binary = self.find_binary("ffmpeg"),
            ffprobe_binary = self.find_binary("ffprobe")
        )
    
    # Return one (usually required) setting up encoder
    def get_rife_wrapper(self):
        debug_prefix = "[AIOPackageInterface.get_rife_wrapper]"
        logging.info(f"{debug_prefix} Return RifeWrapper")
        return RifeWrapper(
            rife_binary = self.find_binary("rife-ncnn-vulkan"),
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

        # Externals directory
        self.externals_dir = f"{self.AIO_PACKAGE_ROOT}{sep}externals"
        logging.info(f"{debug_prefix} Externals directory is [{self.externals_dir}]")
        self.utils.mkdir_dne(path = self.externals_dir, silent = True)

        # Downloads (inside externals)
        self.downloads_dir = f"{self.AIO_PACKAGE_ROOT}{sep}externals{sep}downloads"
        logging.info(f"{debug_prefix} Downloads dir is [{self.downloads_dir}]")
        self.utils.mkdir_dne(path = self.downloads_dir, silent = True)

        # Runtime directory
        self.runtime_dir = f"{self.AIO_PACKAGE_ROOT}{sep}runtime"
        logging.info(f"{debug_prefix} Runtime directory is [{self.runtime_dir}]")
        self.utils.mkdir_dne(path = self.runtime_dir, silent = True)

        # Data directory
        self.data_dir = f"{self.AIO_PACKAGE_ROOT}{sep}data"
        logging.info(f"{debug_prefix} Data dir is [{self.data_dir}]")

        # Profiles directory
        self.profiles_dir = f"{self.data_dir}{sep}profiles"
        logging.info(f"{debug_prefix} Profiles dir is [{self.profiles_dir}]")
        self.utils.mkdir_dne(path = self.profiles_dir, silent = True)

        # Sessions directory
        self.sessions_dir = f"{self.AIO_PACKAGE_ROOT}{sep}sessions"
        logging.info(f"{debug_prefix} Sessions directory is [{self.sessions_dir}]")
        self.utils.mkdir_dne(path = self.sessions_dir, silent = True)

        # Windoe juuuust in case
        if self.os == "windows":
            logging.info(f"{debug_prefix} Appending the Externals directory to system path juuuust in case...")
            sys.path.append(self.externals_dir)

        # # External dependencies where to append for PATH

        # Externals directory for Linux
        self.externals_dir_linux = f"{self.AIO_PACKAGE_ROOT}{sep}externals{sep}linux"
        logging.info(f"{debug_prefix} Externals directory for Linux OS is [{self.externals_dir_linux}]")
        self.utils.mkdir_dne(path = self.externals_dir_linux, silent = True)

        # Externals directory for Windows
        self.externals_dir_windows = f"{self.AIO_PACKAGE_ROOT}{sep}externals{sep}windows"
        logging.info(f"{debug_prefix} Externals directory for Windows OS is [{self.externals_dir_windows}]")
        self.utils.mkdir_dne(path = self.externals_dir_windows, silent = True)

        # Externals directory for macOS
        self.externals_dir_macos = f"{self.AIO_PACKAGE_ROOT}{sep}externals{sep}macos"
        logging.info(f"{debug_prefix} Externals directory for Darwin OS (macOS) is [{self.externals_dir_macos}]")
        self.utils.mkdir_dne(path = self.externals_dir_macos, silent = True)

        self.__update_externals_search_path()

        # Code flow management
        if self.prelude["flow"]["stop_at_initialization"]:
            logging.critical(f"{debug_prefix} Exiting as stop_at_initialization key on prelude.toml is True")
            sys.exit(0)
    
    # Internally update the search path for finding externals
    def __update_externals_search_path(self):
        debug_prefix = "[AIOPackageInterface.__update_externals_search_path]"

        # # This native platform externals dir
        self.externals_dir_this_platform = self.__get_platform_external_dir(self.os)
        logging.info(f"{debug_prefix} This platform externals directory is: [{self.externals_dir_this_platform}]")
        
        # Get a list of recursive directories
        recursive_directories = []
        for path in os.listdir(self.externals_dir_this_platform):
            recursive_directories.append(f"{self.externals_dir_this_platform}{os.path.sep}{path}")

        # When using some function like Utils.get_executable_with_name, it have an argument
        # called extra_paths, add this for searching for the full externals directory.
        # Preferably use this interface methods like find_binary instead
        self.EXTERNALS_SEARCH_PATH = [
            self.externals_dir,
            self.externals_dir_this_platform,
        ] + recursive_directories

    # Get the target externals dir for this platform
    def __get_platform_external_dir(self, platform):
        debug_prefix = "[AIOPackageInterface.__get_platform_external_dir]"

        # # This platform externals dir
        externals_dir = {
            "linux": self.externals_dir_linux,
            "windows": self.externals_dir_windows,
            "macos": self.externals_dir_macos,
        }.get(platform)

        # log action
        logging.info(f"{debug_prefix} Return external dir for platform [{platform}] -> [{externals_dir}]")

        return externals_dir

    # Search for something in system's PATH, also searches for the externals folder
    # Don't append the extra .exe because Linux, macOS doesn't have these
    def find_binary(self, binary):
        debug_prefix = "[AIOPackageInterface.find_binary]"

        # Log action
        logging.info(f"{debug_prefix} Finding binary in PATH and EXTERNALS directories: [{binary}]")

        found = self.utils.get_executable_with_name(binary, extra_paths = self.EXTERNALS_SEARCH_PATH)
        logging.info(f"{debug_prefix} Got: [{found}]")

        return found

    # If we have a previous version of this external extracted, ask to delete the old one
    def verify_external_already_present(self, external_name, zipped_download, target_externals_dir):
        debug_prefix = "[AIOPackageInterface.verify_external_already_present]"

        # If user chose not to delete old versions
        if self.prelude["externals"]["dont_verify_delete_old_versions"]:
            logging.warn(f"{debug_prefix} Not verifying and deleting old versions of externals because configuration on [prelude.toml]")
            return

        # The extracted folder inside the zip
        # FIXME: will error if the extracted folder has different name
        extracted_external_folder_name = zipped_download.replace(".zip", "")

        logging.info(f"{debug_prefix} Checking if no other version of External [{external_name}] is already extracted on [{target_externals_dir}]")

        # Which externals are currently present (extracted)
        extracted_externals = os.listdir(target_externals_dir)

        # Iterate on the extracted externals
        for external_folder in extracted_externals:

            # If the external substring is present on the directories on the target platform dir
            # if "ffmpeg" in "ffmpeg-n4.3.1-29-g89daac5fe2-win64-gpl-4.3" -> True
            if external_name in external_folder:

                # If this last version zip file is not a folder that have the external name
                # for example, we have ffmpeg-2 and ffmpeg-3, the latest version is the -3
                # when we iter through the directory we might find the two ["ffmpeg-2", "ffmpeg-3"]
                # so we want to delte the one that contains "ffmpeg" and isn't "ffmpeg-3" (latest v.)
                if extracted_external_folder_name != external_folder:

                    # The full path of the old extracted external to delete
                    full_path = f"{target_externals_dir}{os.path.sep}{external_folder}"

                    logging.info(f"{debug_prefix} External [{external_folder}] is older version and extracted on Externals dir")
                    logging.info(f"{debug_prefix} Asking user to delete path: [{full_path}]")
                    
                    # Ask the user to enter y or n for deleting or not the 
                    while True:
                        # Don't confirm with the user to delete old directories of externals
                        if self.prelude["externals"]["dont_confirm_before_deleting_old_version"]:
                            uinput = "y"
                        else:
                            uinput = input(f"\nA new version of the external [{external_name}] was downloaded and extracted, delete the old one at [{full_path}] ? New one is [{extracted_external_folder_name}] (y/n): ")
                            uinput = uinput.lower()

                        if uinput == "y":
                            self.utils.rmdir(path = full_path)
                            break
                        elif uinput == "n":
                            break
                        else:
                            print("\n Entered answer isn't (y/n) [\"y\" or \"n\"]")
                 
    # Make sure we have some target Externals, downloads latest release for them.
    # For forcing to download the Windows binaries for a release, send os="windows" for overwriting
    # otherwise it'll be set to this class's os.
    #
    # For FFmpeg: Linux and macOS people please install from your distro's package manager.
    # Waifu2x ncnn vulkan and Rife ncnn vulkan we get from the latest release so no need to worry.
    #
    # Possible values for target are: ["ffmpeg", "rife-ncnn-vulkan", "waifu2x-ncnn-vulkan"]
    #
    def check_download_externals(self, target_externals = [], platform = None):
        debug_prefix = "[AIOPackageInterface.check_download_externals]"

        # Overwrite os if user set to a specific one
        if platform is None:
            platform = self.os
        else:
            # Error assertion, only allow linux, macos or windows target os
            valid = ["linux", "macos", "windows"]
            if not platform in valid:
                err = f"Target os [{platform}] not valid: should be one of {valid}"
                logging.error(f"{debug_prefix} {err}")
                raise RuntimeError(err)

        # Force the externals argument to be a list
        target_externals = self.utils.force_list(target_externals)

        # Log action
        logging.info(f"{debug_prefix} Checking externals {target_externals} for os = [{platform}]")

        # We're frozen (running from release..)
        if getattr(sys, 'frozen', False):
            logging.info(f"{debug_prefix} Not checking for externals because is executable build.. (should have them bundled?)")
            return

        # Short hand
        sep = os.path.sep
        
        # The target externals dir for this platform, it must be windows if we're here..
        target_externals_dir = self.__get_platform_external_dir(platform)

        # For each target external
        for external in target_externals:
            debug_prefix = "[AIOPackageInterface.check_download_externals]"
            logging.info(f"{debug_prefix} Checking / downloading external: [{external}] for platform [{platform}]")
            
            # # FFmpeg / FFprobe

            if external == "ffmpeg":
                debug_prefix = f"[AIOPackageInterface.check_download_externals({external})]"

                # We're on Linux / macOS so checking ffmpeg external dependency on system's path
                if platform in ["linux", "macos"]:
                    logging.info(f"{debug_prefix} You are using Linux, please make sure you have FFmpeg package installed on your distro, we'll just check for it now..")
                    
                    # Can't continue
                    if not self.utils.has_executable_with_name("ffmpeg"):
                        logging.error(f"{debug_prefix} Couldn't find lowercase ffmpeg binary on PATH, install from your Linux distro package manager / macOS homebrew")
                        sys.exit(-1)
                    continue
    
                # Get the latest release number of ffmpeg
                repo = "https://api.github.com/repos/BtbN/FFmpeg-Builds/releases/latest"
                logging.info(f"{debug_prefix} Getting latest release info on repository: [{repo}]")
                ffmpeg_release = json.loads(self.download.get_html_content(repo))

                # The assets (downloadable stuff)
                assets = ffmpeg_release["assets"]

                logging.info(f"{debug_prefix} Available assets to download (checking for non shared, gpl, non vulkan release):")

                # Parsing the version we target and want
                for item in assets:

                    # The name of the 
                    name = item["name"]
                    logging.info(f"{debug_prefix} - [{name}]")

                    # Expected stuff
                    is_lgpl = "lgpl" in name
                    is_shared = "shared" in name
                    have_vulkan = "vulkan" in name
                    from_master = "N" in name

                    # Log what we expect
                    logging.info(f"{debug_prefix} - :: Is LGPL:                   [{is_lgpl:<1}] (expect: 0)")
                    logging.info(f"{debug_prefix} - :: Is Shared:                 [{is_shared:<1}] (expect: 0)")
                    logging.info(f"{debug_prefix} - :: Have Vulkan:               [{have_vulkan:<1}] (expect: 0)")
                    logging.info(f"{debug_prefix} - :: Master branch (N in name): [{from_master:<1}] (expect: 0)")

                    # We have a match!
                    if not (is_lgpl + is_shared + have_vulkan + from_master):
                        logging.info(f"{debug_prefix} - >> :: We have a match!!")
                        download_url = item["browser_download_url"]
                        break

                logging.info(f"{debug_prefix} Download URL: [{download_url}]")

                # Where we'll save the compressed zip of FFmpeg
                ffmpeg_zip = self.downloads_dir + f"{sep}{name}"

                # Download FFmpeg build
                download_existed = self.download.wget(download_url, ffmpeg_zip, f"FFmpeg v={name}")

                # Verify we don't have an older version extracted..
                self.verify_external_already_present(
                    external_name = external,
                    zipped_download = name,
                    target_externals_dir = target_externals_dir
                )

                # Extract the files
                self.download.extract_zip(ffmpeg_zip, target_externals_dir)

            # # nihui ncnn vulkan stuff
            
            elif external in ["waifu2x-ncnn-vulkan", "rife-ncnn-vulkan"]:
                debug_prefix = f"[AIOPackageInterface.check_download_externals({external})]"

                # Get the latest release info on waifu2x or rife
                repo = f"https://api.github.com/repos/nihui/{external}/releases/latest"
                logging.info(f"{debug_prefix} Getting latest release info on repository: [{repo}]")
                nihui_releases = json.loads(self.download.get_html_content(repo))

                # The latest assets assets list
                assets = nihui_releases["assets"]

                # nihui releases assets ending with an -windows, -{linux.ubuntu}, -macos
                # so we'll search for those substrings
                want_asset_with = {
                    "linux":   ["linux", "ubuntu"],
                    "macos":   ["macos"],
                    "windows": ["windows"]
                }.get(platform)
                logging.info(f"{debug_prefix} Want asset with substring {want_asset_with}")

                # # Loop through latest assets

                logging.info(f"{debug_prefix} Available assets to download:")

                # Parsing the version we target and want
                for item in assets:

                    # The name of the 
                    name = item["name"]
                    logging.info(f"{debug_prefix} - [{name}]")

                    # If any substring is on the name then it's a match
                    matches = any([want in name for want in want_asset_with])
                
                    # We got an match for this platform
                    if matches:
                        logging.info(f"{debug_prefix} - :: Matches!!")
                        download_url = item["browser_download_url"]
                        break  # this inner most for loop, need to download and extract
                    else:
                        logging.info(f"{debug_prefix} - Doesn't match")
                
                # Log where we'll be downloading from
                logging.info(f"{debug_prefix} Download URL: [{download_url}]")

                # Where to download the nihui zip
                nihui_zip = f"{self.downloads_dir}{sep}{name}"

                # Download the zip and extract, nihui already includes a LICENSE file
                # so we don't have to worry on warning the end user
                self.download.wget(download_url, nihui_zip, f"nihui: {name}")

                # Verify we don't have an older version extracted..
                self.verify_external_already_present(
                    external_name = external,
                    zipped_download = name,
                    target_externals_dir = target_externals_dir
                )

                self.download.extract_zip(nihui_zip, target_externals_dir)
