import sys
import os

# Append previous folder to path
THIS_DIR = os.path.dirname(os.path.abspath(__file__))

import aio
interface = aio.AIOPackageInterface()

# # Ensure Externals

if False:
    want = ["ffmpeg", "waifu2x-ncnn-vulkan", "rife-ncnn-vulkan"]

    EVERY_PLATFORM_DEBUG = True

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

ffmpeg = interface.get_ffmpeg_wrapper()
ffmpeg.video_to_frames("yn_moving_480.mkv", context.session_input_original_frames)

rife = interface.get_rife_wrapper()
rife.execute(
    i = context.session_input_original_frames,
    o = context.session_output_interpolated_frames,
    x = False,  # Enable tta mode NOTE: SLOW
    u = False,  # Enable UHD mode
    m = "rife-UHD"  # Can be ["rife", "rife-anime", "rife-HD", "rife-UHD"]
)