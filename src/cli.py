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
#   Purpose: Demo usage of AIO in a "script" form, in the future this might
# hold a CLI interface perhaps with some extra functionality?
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
 
import sys
import os

# Append previous folder to path
THIS_DIR = os.path.dirname(os.path.abspath(__file__))

import aio
interface = aio.AIOPackageInterface()

# # Ensure Externals

if True:
    want = ["ffmpeg", "waifu2x-ncnn-vulkan", "rife-ncnn-vulkan"]

    EVERY_PLATFORM_DEBUG = False

    if EVERY_PLATFORM_DEBUG:
        interface.check_download_externals(target_externals = want, platform = "linux")
        interface.check_download_externals(target_externals = want, platform = "windows")
        interface.check_download_externals(target_externals = want, platform = "macos")
    else:
        interface.check_download_externals(target_externals = want)

# # Video Enhancer

video_enhancer_interface = interface.get_video_enhancer_interface()
video_enhancer_interface.setup_session(session_name = "developers_developers_developers")
context = video_enhancer_interface.aio_ve_main.context

# # # User configurable

input_video = "yn_moving_480.mkv"

# # #

# Info on the video
ffmpeg = interface.get_ffmpeg_wrapper()
info = ffmpeg.get_video_info(input_video)

# # 1st pass - Interpolation

double_fps = 2 * eval(info["fps"])
process_images_in_format = "png"

# Extract video to files
ffmpeg.video_to_frames(
    input_video = input_video,
    target_dir = context.session_input_original_frames,
    frame_extension = process_images_in_format
)
assert info["frame_count"] == len(os.listdir(context.session_input_original_frames))

# Interpolate from the extracted images folder to the interpolated one
rife = interface.get_rife_wrapper()
rife.execute(
    src = context.session_input_original_frames,
    dst = context.session_output_interpolated_frames,
    model = "rife-anime",  # Can be ["rife", "rife-anime", "rife-HD", "rife-UHD"]
    oformat = process_images_in_format,
    tta = False,  # Enable tta mode NOTE: SLOW
    uhd = False,  # Enable UHD mode
)

# Create video out of the interpolated frames just for measuring
ffmpeg.frames_to_video(
    input_frames_dir = context.session_output_interpolated_frames,
    frames_externsion = process_images_in_format,
    original_video_map_audio = input_video,
    output_video = "rife.mkv",
    fps = double_fps,
    width = info["width"],
    height = info["height"],
)

# # 2nd pass - Upscale

# Upscale the interpolated frames, output to the upscaled frames directory
waifu2x = interface.get_waifu2x_wrapper()
waifu2x.execute(
    src = context.session_output_interpolated_frames,
    dst = context.session_output_upscaled_frames,
    noise_level = 3,
    tile_size = 200,
    load_proc_save = "4:4:4",
    oformat = process_images_in_format,
    model = "models-upconv_7_anime_style_art_rgb",  # Can be ["models-cunet", "models-upconv_7_anime_style_art_rgb", "models-upconv_7_photo"]
)

# Encode final video, that is get the interpolated and upscaled frames and make a video
ffmpeg.frames_to_video(
    input_frames_dir = context.session_output_upscaled_frames,
    frames_externsion = process_images_in_format,
    original_video_map_audio = input_video,
    output_video = "rife-waifu2x.mkv",
    fps = double_fps,
    width = 2 * info["width"],  # These were upscaled by a factor of 2x
    height = 2 * info["height"],
)