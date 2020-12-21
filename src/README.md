## Running from the source code

Install Python 3, pip and ffmpeg on your system (preferably 3.8 or 3.9)

- **Arch Linux**: `sudo pacman -S python python-pip ffmpeg`

<hr>

*(Optional): Create a virtual environment to isolate Python packages*

- `python3 -m venv aio-venv`
- `source ./aio-venv/bin/activate`

<hr>

Open a shell on this directory

- `sh install_requirements.sh`
- `python3 gui.py`