# MIT License
#
# Copyright (c) 2020,
#  - Tremeschin < https://tremeschin.gitlab.io > 
#  - Tsubajashi < https://github.com/Tsubajashi >
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

# AIOVE

debug_prefix = "[gui.py]"

import aio_enhancer

# Create main class of AIO
aio = aio_enhancer.AIOEnhancerMain()

import threading
# threading.Thread(target = aio.run, daemon = True).start()

import logging

database = aio.context.runtime.database

# Fail safe
if not "dearpygui" in database.keys():
    logging.warn(f"{debug_prefix} dearpygui key not in database")
    database["dearpygui"] = {}
else:
    logging.info(f"{debug_prefix} dearpygui key was in database, will load last configuration")

# # GUI specific

from dearpygui.core import *
from dearpygui.simple import *

set_main_window_size(1000, 500)

def retrieve_callback(sender, callback):
    for identifier in [
        "Input Video##inputtext",
        "Output Video##inputtext",
    ]:
        # print(f"[{identifier}]: {get_value(identifier)}")
        
        # The value of the identifier that has changed
        val = get_value(identifier)

        if identifier == "Input Video##inputtext":
            if database["dearpygui"]["input_video"] != val:
                logging.info(f"Changing key [dearpygui][input_video] to {val}")
                database["dearpygui"]["input_video"] = val

        elif identifier == "Output Video##inputtext":
            if database["dearpygui"]["output_video"] != val:
                logging.info(f"Changing key [dearpygui][output_video] to {val}")
                database["dearpygui"]["output_video"] = val


with window(
        "Input / Output",
        width = 500, height = 250,
        x_pos = 0, y_pos = 0,
        no_resize = True, no_move = True,
        no_scrollbar = True, no_title_bar = True,
        no_collapse = True, horizontal_scrollbar = False,
        no_close = True):

    add_text("[ Input / Output ]", bullet = False)
    add_separator()

    add_input_text(
        "Input Video##inputtext", hint = "Path", callback = retrieve_callback,
        default_value = database["dearpygui"].get("input_video", "")
    )
    add_same_line()
    add_button("Select##input_video", callback = retrieve_callback)

    add_input_text(
        "Output Video##inputtext", hint = "Path", callback = retrieve_callback,
        default_value = database["dearpygui"].get("output_video", "")
    )
    add_same_line()
    add_button("Select##output_video", callback = retrieve_callback)


set_main_window_title("All in One Video Enhancer")
start_dearpygui()

# # # # # # # # #
