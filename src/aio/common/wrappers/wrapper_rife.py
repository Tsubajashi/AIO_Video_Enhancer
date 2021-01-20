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
    def execute(self, src, dst, gpu_id = 0, load_proc_save = "4:4:4", model: str = None, tta = False, uhd = False, oformat = "png"):
        debug_prefix = "[RifeWrapper.video_to_frames]"

        # Build the (basic) command, without models or optional arguments
        command = [self.rife_binary, "-i", src, "-o", dst, "-g", str(gpu_id), "-j", load_proc_save, "-f", oformat]

        # # Optional / extra arguments

        # nihui includes models under the extracted folder so we specify 
        if model is not None:
            sep = os.path.sep

            # User already pointed some directory
            if not os.path.isdir(model):

                # Get the parent directory of the rife binary
                rife_directory = sep.join(self.rife_binary.split(sep)[:-1])

                # The theoretical model path given by the user
                model_path = f"{rife_directory}{sep}{model}"
                
                # Error assertion, invalid model path built
                if not os.path.exists(model_path):
                    logging.error(f"{debug_prefix} Given model [{model}] does not have model path directory in [{model_path}]")
                    sys.exit(-1)

            command += ["-m", model_path]

        # Enable tta mode
        if tta:
            command.append("-x")

        # Enable UHD mode
        if uhd:
            command.append("-u")

        # Log action
        logging.info(f"{debug_prefix} Running command for Rife interpolation: {command}")

        # Run command...
        subprocess.run(command)
