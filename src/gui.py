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

set_theme(runtime_dict.get("theme", "dark"))

set_style_antialiased_lines(True)
set_main_window_size(1000, 500)
set_style_window_rounding(0)
depth = ">"

combobox_profile_profiles = ["anime", "generic"]

def retrieve_callback(sender, callback):
    for identifier in [
        "Input Video ##inputtext",
        "Output Video##inputtext",
        "Input Video ##inputtext",
        "##combobox_profile",
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

        elif identifier == "##combobox_profile":
            if runtime_dict["last_profile"] != val:
                profile_name = combobox_profile_profiles[val]
                logging.info(f"Changing key runtime_dict[last_profile] to {val} = {profile_name}")
                runtime_dict["last_profile"] = profile_name


        aio.context.runtime.save_current_runtime(depth)


def theme_callback(sender, data):
    runtime_dict["theme"] = sender
    set_theme(sender)
    aio.context.runtime.save_current_runtime(depth)


def menuitem(sender, data):
    if sender == "Project Repository":
        aio.utils.open_url("https://github.com/tsubajashi/aio_video_enhancer", depth)
    elif sender == "Contributors":
        aio.utils.open_url("https://github.com/Tsubajashi/AIO_Video_Enhancer/graphs/contributors")
    elif sender == "Documentation":
        aio.utils.open_url("https://github.com/Tsubajashi/AIO_Video_Enhancer/wiki")

    
with window(
        "Menu Bar",
        width = 1000, height = 5,
        x_pos = 0, y_pos = 0,
        no_resize = True, no_move = True,
        no_scrollbar = True, no_title_bar = True,
        no_collapse = True, horizontal_scrollbar = False,
        no_close = True):
    add_menu_bar("MenuBar")
    
    add_menu("Theme")
    add_menu_item("Cherry", callback = theme_callback)
    add_menu_item("Classic", callback = theme_callback)
    add_menu_item("Dark", callback = theme_callback)
    add_menu_item("Dark 2", callback = theme_callback)
    add_menu_item("Dark Grey", callback = theme_callback)
    add_menu_item("Gold", callback = theme_callback)
    add_menu_item("Grey", callback = theme_callback)
    add_menu_item("Light", callback = theme_callback)
    add_menu_item("Purple", callback = theme_callback)
    add_menu_item("Red", callback = theme_callback)
    end()

    add_menu("About")
    add_menu_item("Project Repository", callback = menuitem)
    add_menu_item("Contributors", callback = menuitem)
    end()

    add_menu("Help")
    add_menu_item("Documentation", callback = menuitem)
    end()

    end()


with window(
        "Input / Output",
        width = 750, height = 100,
        x_pos = 0, y_pos = 31,
        no_resize = True, no_move = True,
        no_scrollbar = True, no_title_bar = True,
        no_collapse = True, horizontal_scrollbar = False,
        no_close = True):

    # Title
    add_text("[ Input / Output ]", bullet = True)
    add_separator()

    # Input Video text entry
    add_input_text(
        "Input Video ##inputtext", hint = "Path", callback = retrieve_callback,
        default_value = runtime_dict.get("input_video", ""), width = 585
    )
    add_same_line()
    add_button("Select##input_video", callback = retrieve_callback)

    # Output Video text entry
    add_input_text(
        "Output Video##inputtext", hint = "Path", callback = retrieve_callback,
        default_value = runtime_dict.get("output_video", ""), width = 585
    )
    add_same_line()
    add_button("Select##output_video", callback = retrieve_callback)
    add_separator()
    

with window(
        "Profile",
        width = 250, height = 100,
        x_pos = 750, y_pos = 31,
        no_resize = True, no_move = True,
        no_scrollbar = True, no_title_bar = True,
        no_collapse = True, horizontal_scrollbar = False,
        no_close = True):
    add_text("[ Profile ]", bullet = True)
    add_separator()

    # Profile
    add_listbox("##combobox_profile", items = combobox_profile_profiles, 
        num_items = 2, callback = retrieve_callback,
        default_value = combobox_profile_profiles.index(runtime_dict.get("last_profile", "anime"))
    )

    add_separator()



with window(
        "Progress",
        width = 1000, height = 50,
        x_pos = 0, y_pos = 450,
        no_resize = True, no_move = True,
        no_scrollbar = True, no_title_bar = True,
        no_collapse = True, horizontal_scrollbar = False,
        no_close = True):
    add_text("[ Progress ]", bullet = True)

    # Profile
    add_progress_bar("Progress##progress_bar", default_value = 0, width = -1)



set_main_window_title("All in One Video Enhancer")
start_dearpygui()

# # # # # # # # #
