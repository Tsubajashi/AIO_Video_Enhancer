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
#   Purpose: nihui's Rife NCNN Vulkan wrapper
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

import aio.common.cmn_any_logger
import subprocess
import logging
import sys
import os

class RifeWrapper:
    def __init__(self, rife_binary):
        debug_prefix = "[RifeWrapper.__init__]"
        
        self.rife_binary = rife_binary

        logging.info(f"{debug_prefix} Rife binary is: [{self.rife_binary}]")

    # Execute rife binary with some of its settings
    def execute(self, i, o, g = 0, j = "4:4:4", m: str = None, x = False, u = False):
        debug_prefix = "[RifeWrapper.video_to_frames]"

        # Build the (basic) command, without models or optional arguments
        command = [self.rife_binary, "-i", i, "-o", o, "-g", str(g), "-j", j]

        # # Optional / extra arguments

        # nihui includes models under the extracted folder so we specify 
        if m is not None:
            sep = os.path.sep

            # Get the parent directory of the rife binary
            rife_directory = sep.join(self.rife_binary.split(sep)[:-1])

            # The theoretical model path given by the user
            model_path = f"{rife_directory}{sep}{m}"
            
            # Error assertion, invalid model path built
            if not os.path.exists(model_path):
                logging.error(f"{debug_prefix} Given model [{m}] does not have model path directory in [{model_path}]")
                sys.exit(-1)

        # Enable tta mode
        if x:
            command.append("-x")

        # Enable UHD mode
        if u:
            command.append("-u")

        # Log action
        logging.info(f"{debug_prefix} Running command for extracting video to frames: {command}")

        # Run command...
        subprocess.run(command)
