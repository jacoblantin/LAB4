# LAB4
 
This is the Git Repository for LAB04 for ME405.

The repository contains the files for Lab03 needed for this lab, modified for this labs needs. The previous main.py file has been renamed to control.py.

The current main.py file contains the code modified from basic_tasks.py to be used in a scheduler for this lab. The two tasks
in main.py are two separate control loops that each control a motor set to a Kp of 8 and set to a set number of revoultions.

The Kp of 6 was found from testing the flywheel motor at different Kp's. Tests from Kp = 24 to 4 are shown below. A low Kp of
4 was what we deided to be "bad performance."
![fig1 - Kp from 24 to 4](https://github.com/jacoblantin/LAB4/assets/145752175/52707a67-309d-44fd-b8da-c2135fa4b9c1)

The Kp chosen of 6 is shown compared to the "nice" 24 in the graph shown below.
![fig3 - Kp, 24 and 6](https://github.com/jacoblantin/LAB4/assets/145752175/9becfdff-6b42-4cef-83aa-b95ca2c51306)

The main.py file thus runs the two motors at a Kp of 6 in a scheduler that runs the tasks at the same time.
