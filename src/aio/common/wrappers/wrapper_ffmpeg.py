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

    # Converts a video to images
    def video_to_frames(self, input_video, target_dir, frame_extension = "jpg", padded_zeros = 8):
        debug_prefix = "[FFmpegWrapper.video_to_frames]"

        # Build the command
        command = [
            self.ffmpeg_binary, "-i", input_video,
            "-vsync", "vfr",  # Mitigation on variable frame rate
            "-q:v", "1", f"{target_dir}{os.path.sep}%0{padded_zeros}d.{frame_extension}"
        ]

        # Log action
        logging.info(f"{debug_prefix} Running command for extracting video to frames: {command}")

        # Run command...
        subprocess.run(command)
    
    def frames_to_video(self,
            input_frames_dir, frames_externsion,
            original_video_map_audio,
            output_video,
            fps, width, height,
            crf = 18,
            override = True,
            padded_zeros = 8, **kwargs):
        debug_prefix = "[FFmpegWrapper.video_to_frames]"

        # Build the command
        command = [
            self.ffmpeg_binary,
            "-r", f"{fps}",
            "-i", f"{input_frames_dir}{os.path.sep}%0{padded_zeros}d.{frames_externsion}",
            "-i", f"{original_video_map_audio}",
            "-map", "0:v", "-map", "1:a",
            "-c:v", "libx264", "-vf", f"fps={fps},scale={width}x{height}",
            "-crf", f"{crf}",
            output_video
        ]

        if override:
            command.append("-y")

        # Log action
        logging.info(f"{debug_prefix} Running command for converting images -> video also map original audio streams [{command}]")

        # Run command...
        subprocess.run(command)
    
    # # Video info

    # Returns a dictionary with some info of the video
    # keys: frame_count, duration (seconds), fps, width, height
    def get_video_info(self, target_video):
        debug_prefix = "[FFmpegWrapper.get_video_info]"

        # Log action
        logging.info(f"{debug_prefix} Getting info of the video [{target_video}]")

        # Get frame count and the duration, we use the same function as we just grab the same output
        frame_count_and_duration = self.get_video_frame_count_and_duration(of_video = target_video)

        # Resolution
        resolution = self.get_video_resolution(of_video = target_video)

        # Build the info dictionary also call some other specific functions
        info = {
            "frame_count": frame_count_and_duration["frame_count"],
            "duration": frame_count_and_duration["duration"],  # Duration probably won't be required but it's a free bonus
            "fps": self.get_video_frame_rate(of_video = target_video),
            "width": resolution[0],
            "height": resolution[1],
        }

        # Log action
        logging.info(f"{debug_prefix} Info of the video: {info}")

        return info

    # Get the information on the video resolution, returns list of [width, height]
    def get_video_resolution(self, of_video):
        debug_prefix = "[FFmpegWrapper.get_video_resolution]"

        # Build the command
        command = [
            self.ffprobe_binary, "-v", "error",
            "-select_streams", "v:0",
            "-show_entries", "stream=height,width",
            "-of", "csv=s=x:p=0", of_video
        ]

        # Log action
        logging.info(f"{debug_prefix} Running command for extracting video resolution: {command}")

        # Get the output
        resolution = subprocess.check_output(command, stderr = subprocess.STDOUT).decode("utf-8").replace("\n", "")
        logging.info(f"{debug_prefix} Resolution is [{resolution}]")

        # FFprobe gives us a WxH so we split on the x and assign to the width and height
        width, height = resolution.split("x")
        logging.info(f"{debug_prefix} - Width:  [{width}]")
        logging.info(f"{debug_prefix} - Height: [{height}]")

        return [int(width), int(height)]

    # Attempt to get the frame count and duration, uses -vsync cfr for constant frame rate
    # Variable frame rate (VFR) is quite annoying to deal with and probably won't be as compatible
    def get_video_frame_count_and_duration(self, of_video):
        debug_prefix = "[FFmpegWrapper.get_video_frame_count]"

        # Build the command
        command = [
            self.ffmpeg_binary, "-i", of_video,
            "-vsync", "cfr",  # Mitigation on variable frame rate
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

        # Regex on the time= mark
        duration_raw = re.search(r"time=(\d+):(\d+):(\d+).(\d+)", output.replace(" ", ""))
        duration = 0
        duration += float(f"{duration_raw.group(3)}.{duration_raw.group(4)}") # Seconds + Milisseconds
        duration += int(duration_raw.group(2)) * 60   # Minutes
        duration += int(duration_raw.group(1)) * 3600 # Hours

        # Log the frame count, return it
        logging.info(f"{debug_prefix} Frame count is [{frames}]")
        return {"frame_count": int(frames), "duration": duration}

    # Attempt to get the video frame rate, returns string like "24/1" if PAL video
    # or some other "24000/1001" if NTSC video
    def get_video_frame_rate(self, of_video):
        debug_prefix = "[FFmpegWrapper.get_video_frame_rate]"

        # Build the command
        command = [
            self.ffprobe_binary, "-v", "error",
            "-select_streams", "v:0",
            "-show_entries", "stream=avg_frame_rate",
            "-of", "default=noprint_wrappers=1:nokey=1",
            of_video
        ]

        # Log action
        logging.info(f"{debug_prefix} Running command for extracting frame rate of the video: {command}")

        # Get the output
        frame_rate = subprocess.check_output(command, stderr = subprocess.STDOUT).decode("utf-8").replace("\n", "")
        logging.info(f"{debug_prefix} Frame rate is [{frame_rate}]")

        return frame_rate
