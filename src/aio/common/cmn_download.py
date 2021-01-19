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
#   Purpose: Download utilities
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
from tqdm import tqdm
import requests
import zipfile
import logging
import time
import wget
import sys
import os


class Download:

    def wget_progress_bar(self, current, total, width=80):
        # current         \propto time.time() - startdownload 
        # total - current \propto eta
        # eta = (total-current)*(time.time()-startdownload)) / current

        try: # div by zero
            eta = int(( (time.time() - self.start) * (total - current) ) / current)
        except Exception:
            eta = 0

        avgdown = ( current / (time.time() - self.start) ) / 1024

        currentpercentage = int(current / total * 100)
        
        print("\r Downloading file [{}]: [{}%] [{:.2f} MB / {:.2f} MB] ETA: [{} sec] AVG: [{:.2f} kB/s]".format(self.download_name, currentpercentage, current/1024/1024, total/1024/1024, eta, avgdown), end='', flush=True)

    # Downloads with wget, returns False if file didn't exist, True if it already exists
    def wget(self, url, save, name = "Undefined"):
        debug_prefix = "[Download.wget]"

        self.download_name = name
        self.start = time.time()

        logging.info(f"{debug_prefix} Get file from URL [{url}] saving to [{save}]")

        if os.path.exists(save):
            logging.info(f"{debug_prefix} Download file already exists, skipping")
            return True

        wget.download(url, save, bar=self.wget_progress_bar)
        print()
        return False
    
    # Get html content
    def get_html_content(self, url):
        debug_prefix = "[Download.get_html_content]"

        logging.info(f"{debug_prefix} Getting content from [{url}]")

        r = requests.get(url)
        return r.text

    def extract_zip(self, src, dst):
        debug_prefix = "[Download.extract_zip]"
        logging.info(f"{debug_prefix} Extracing [{src}] -> [{dst}]")
        
        with zipfile.ZipFile(src, 'r') as zipped:
            zipped.extractall(dst)