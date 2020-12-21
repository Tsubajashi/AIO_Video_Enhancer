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
#   Purpose: Utilities for videos, mainly a wrapper around FFmpeg / FFprobe
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

import logging


class AIOVideo:
    def __init__(self, aio_main):
        debug_prefix = "[AIOCore.__init__]"
        self.aio_main = aio_main

        # # Get FFmpeg / FFprobe binaries

        # # FFmpeg

        logging.info(f"{debug_prefix} Getting FFmpeg binary, also searching on externals dir")
        self.ffmpeg_bin = self.aio_main.utils.get_executable_with_name(
            "ffmpeg", extra_paths = self.aio_main.context.paths.externals_dir
        )

        # That function returns None if none was found, this is an error and we can't continue
        if self.ffmpeg_bin is None:
            err = "No FFmpeg binary was found, we can't continue"
            logging.error(f"{debug_prefix} {err}")
            raise RuntimeError(err)

        logging.info(f"{debug_prefix} FFmpeg binary found at [{self.ffmpeg_bin}]")


        # # FFprobe
        
        logging.info(f"{debug_prefix} Getting FFprobe binary, also searching on externals dir")
        self.ffprobe_bin = self.aio_main.utils.get_executable_with_name(
            "ffprobe", extra_paths = self.aio_main.context.paths.externals_dir
        )

        # That function returns None if none was found, this is an error and we can't continue
        if self.ffprobe_bin is None:
            err = "No FFprobe binary was found, we can't continue"
            logging.error(f"{debug_prefix} {err}")
            raise RuntimeError(err)

        logging.info(f"{debug_prefix} FFprobe binary found at [{self.ffprobe_bin}]")



