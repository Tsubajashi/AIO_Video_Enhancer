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
#   Purpose: FFmpeg wrapper
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
import re
import os

class FFmpegWrapper:
    def __init__(self, ffmpeg_binary, ffprobe_binary):
        debug_prefix = "[FFmpegWrapper.__init__]"
        
        self.ffmpeg_binary = ffmpeg_binary
        self.ffprobe_binary = ffprobe_binary

        logging.info(f"{debug_prefix} FFmpeg / FFprobe binaries: [{self.ffmpeg_binary}], [{self.ffprobe_binary}]")

    def video_to_frames(self, input_video, target_dir, padded_zeros = 8):
        debug_prefix = "[FFmpegWrapper.video_to_frames]"

        # Build the command
        command = [
            self.ffmpeg_binary, "-i", input_video,
            "-q:v", "1", f"{target_dir}{os.path.sep}%0{padded_zeros}d.jpg"
        ]

        # Log action
        logging.info(f"{debug_prefix} Running command for extracting video to frames: {command}")

        # Run command...
        subprocess.run(command)

    def get_video_frame_count(self, input_video):
        debug_prefix = "[FFmpegWrapper.get_video_frame_count]"

        # Build the command
        command = [
            self.ffmpeg_binary, "-i", input_video,
            "-hide_banner", "-loglevel", "info",
            "-map", "0:v:0", "-c", "copy", "-f", "null", "-"
        ]

        # Log action
        logging.info(f"{debug_prefix} Running command for extracting video to frames: {command}")

        # Get the output
        output = subprocess.check_output(command, stderr = subprocess.STDOUT).decode("utf-8")
        logging.debug(f"{debug_prefix} Got command output: [{output}]")

        # Run regex on the output for getting the number after frame=, we do however
        # replace all spaces with nothing so we have a "uniform" string like:
        #   > frame=239fps=0.0q=-1.0Lsize=N/Atime=00:00:09.87bitrate=N/Aspeed=1e+04x
        # And it's easier to parse this way, also we only get the first and (prob) only match
        logging.info(f"{debug_prefix} Running regular expression for parsing the frame count")
        frames = re.search(r"frame=(\d+)", output.replace(" ", "")).group(1)

        # Log the frame count, return it
        logging.info(f"{debug_prefix} Frame count is [{frames}]")
        return int(frames)