# Installation

install python3.5
pip install python-osc drawSvg rdp

# Connect to Firefly network cable

Manually set ip address to 10.10.10.xx

# To Run
python realsense_data_capture.py --ifaceip=10.10.10.xx

# json to svg - uses the drawSvg library
This script will take json files from a defined directory and output
an svg (and png) with the paths drawn into the same directory / directory of
your choice. Filtered paths are drawn in black, unfiltered
paths are drawn in red
