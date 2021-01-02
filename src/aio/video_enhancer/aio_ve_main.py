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

from aio.video_enhancer.aio_ve_context import AioVEnhancerContext
from aio.video_enhancer.aio_ve_core import AioVEnhancerCore
import logging
import shutil
import math
import sys
import os


class AioVEnhancerMain:
    def __init__(self, aiove_interface):
        debug_prefix = "[AioVEnhancerMain.__init__]"
        self.aiove_interface = aiove_interface
        self.top_level_interface = self.aiove_interface.top_level_interface

        logging.info(f"{debug_prefix} Assigning Utils")
        self.utils = self.top_level_interface.utils

        # Runtime / configs / communicator across files
        logging.info(f"{debug_prefix} Creating AioVEnhancerContext")
        self.context = AioVEnhancerContext(self)

        # Main routines
        logging.info(f"{debug_prefix} Creating AioVEnhancerCore")
        self.core = AioVEnhancerCore(self)

    # Execute AIO main routine
    def run(self):
        logging.info(f"[AioVEnhancerMain.run] Executing AIOCore.run()")
        self.core.run()
