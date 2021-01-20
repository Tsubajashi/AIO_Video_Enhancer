import sys
import os

# Append previous folder to path
THIS_DIR = os.path.dirname(os.path.abspath(__file__))

import aio
interface = aio.AIOPackageInterface()

# # Ensure Externals

if False:
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

v = "yn_moving_480.mkv"

ffmpeg = interface.get_ffmpeg_wrapper()
ffmpeg.get_video_frame_count(v)
exit()
ffmpeg.video_to_frames(v, context.session_input_original_frames)

rife = interface.get_rife_wrapper()
rife.execute(
    src = context.session_input_original_frames,
    dst = context.session_output_upscaled_frames,
    model = "rife-UHD",  # Can be ["rife", "rife-anime", "rife-HD", "rife-UHD"]
    tta = False,  # Enable tta mode NOTE: SLOW
    uhd = False,  # Enable UHD mode
)

waifu2x = interface.get_waifu2x_wrapper()
waifu2x.execute(
    src = context.session_output_upscaled_frames,
    dst = context.session_output_interpolated_frames,
    noise_level = 3,
    tile_size = 200,
    load_proc_save = "4:4:4",
    model = "models-cunet",  # Can be ["models-cunet", "models-upconv_7_anime_style_art_rgb", "models-upconv_7_photo"]
)
