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
#   Purpose: nihui's Waifu2x NCNN Vulkan wrapper
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


class Waifu2xVulkanWrapper:
    def __init__(self, waifu2x_binary):
        debug_prefix = "[Waifu2xVulkanWrapper.__init__]"
        
        self.waifu2x_binary = waifu2x_binary

        logging.info(f"{debug_prefix} Waifu2x Vulkan binary is: [{self.waifu2x_binary}]")

    # Execute rife binary with some of its settings
    def execute(self, src, dst, noise_level, gpu_id = None, load_proc_save = "2:2:2", model: str = None, tta = False, tile_size = 0, oformat = "png"):
        debug_prefix = "[Waifu2xVulkanWrapper.video_to_frames]"

        # Build the (basic) command, without models or optional arguments
        command = [
            self.waifu2x_binary, "-i", src, "-o", dst, "-n", str(int(noise_level)),
            "-j", load_proc_save, "-t", str(int(tile_size)), "-f", oformat
        ]

        if gpu_id is not None:
            command += ["-g", str(gpu_id)]

        # # Optional / extra arguments

        # nihui includes models under the extracted folder so we specify 
        if model is not None:
            sep = os.path.sep

            # User already pointed some directory
            if not os.path.isdir(model):
                    
                # Get the parent directory of the rife binary
                waifu2x_directory = sep.join(self.waifu2x_binary.split(sep)[:-1])

                # The theoretical model path given by the user
                model_path = f"{waifu2x_directory}{sep}{model}"
                
                # Error assertion, invalid model path built
                if not os.path.exists(model_path):
                    logging.error(f"{debug_prefix} Given model [{model}] does not have model path directory in [{model_path}]")
                    sys.exit(-1)
            
            command += ["-m", model_path]

        # Enable tta mode
        if tta:
            command.append("-x")

        # Log action
        logging.info(f"{debug_prefix} Running command for Waifu2x upscaling: {command}")

        # Run command...
        subprocess.run(command)
