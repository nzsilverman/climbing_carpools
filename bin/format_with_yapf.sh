#! /bin/bash

# This script recursively formats all python files in place from 
# the current directory down. It uses the setup.cfg file for 
# yapf settings. In the absence of a setup.cfg yapf defaults will
# be used 

yapf -i -r --verbose --style='{based_on_style: google, spaces_before_comment: 4, indent_width: 4}' .