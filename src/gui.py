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

runtime_dict = aio.context.runtime.runtime_dict

# # GUI specific

from dearpygui.core import *
from dearpygui.simple import *

set_main_window_size(1000, 500)

combobox_profile_profiles = ["anime", "generic"]

def retrieve_callback(sender, callback):
    for identifier in [
        "Input Video ##inputtext",
        "Output Video##inputtext",
        "Input Video ##inputtext",
        "Profile##combobox",
    ]:
        # print(f"[{identifier}]: {get_value(identifier)}")
        
        # The value of the identifier that has changed
        val = get_value(identifier)

        if identifier == "Input Video ##inputtext":
            if runtime_dict["input_video"] != val:
                logging.info(f"Changing key runtime_dict[input_video] to {val}")
                runtime_dict["input_video"] = val

        elif identifier == "Output Video##inputtext":
            if runtime_dict["output_video"] != val:
                logging.info(f"Changing key runtime_dict[output_video] to {val}")
                runtime_dict["output_video"] = val

        elif identifier == "Profile##combobox":
            if runtime_dict["last_profile"] != val:
                logging.info(f"Changing key runtime_dict[last_profile] to {val}")
                runtime_dict["last_profile"] = combobox_profile_profiles[val]


        aio.context.runtime.save_current_runtime("")


with window(
        "Input / Output",
        width = 500, height = 250,
        x_pos = 0, y_pos = 0,
        no_resize = True, no_move = True,
        no_scrollbar = True, no_title_bar = True,
        no_collapse = True, horizontal_scrollbar = False,
        no_close = True):

    # Title
    add_text("[ Input / Output ]", bullet = False)
    add_separator()

    # Input Video
    add_input_text(
        "Input Video ##inputtext", hint = "Path", callback = retrieve_callback,
        default_value = runtime_dict.get("input_video", "")
    )
    add_same_line()
    add_button("Select##input_video", callback = retrieve_callback)

    # Output Video
    add_input_text(
        "Output Video##inputtext", hint = "Path", callback = retrieve_callback,
        default_value = runtime_dict.get("output_video", "")
    )
    add_same_line()
    add_button("Select##output_video", callback = retrieve_callback)

    add_separator()

    # Profile
    add_listbox("Profile##combobox", items = combobox_profile_profiles, 
        num_items = 2, callback = retrieve_callback,
        default_value = combobox_profile_profiles.index(runtime_dict.get("last_profile", "anime"))
    )

set_main_window_title("All in One Video Enhancer")
start_dearpygui()

# # # # # # # # #
