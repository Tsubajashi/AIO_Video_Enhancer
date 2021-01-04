import sys
import os

# Append previous folder to path
THIS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append("..")
sys.path.append(
    THIS_DIR + "/../"
)

import aio
interface = aio.TopLevelInterface()

# Ensure Externals
want = ["ffmpeg", "waifu2x-ncnn-vulkan", "rife-ncnn-vulkan"]

EVERY_PLATFORM_DEBUG = False

if EVERY_PLATFORM_DEBUG:
    interface.check_download_externals(target_externals = want, platform = "linux")
    interface.check_download_externals(target_externals = want, platform = "windows")
    interface.check_download_externals(target_externals = want, platform = "macos")
else:
    interface.check_download_externals(target_externals = want)
