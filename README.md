# Internet speed test plot - with speedtest-cli and matplotlib
Example of plot https://github.com/brentoncollins/ninternet-speed-plot/example-plot.png

There has been alot of talk around the NBN speeds in Australia lately, so I thought that I would put my two cents
in for anyone who wants some data to complain with. 

Every hour it will use matplotlib to create a plot of your current connection speeds and save them to a image file, every 24 at midnight it will make a copy of your daily plot and save it in a logs directory for you to check or send off to complain.

This was created in python 3.x

Also remember that if you are downloadin/uploading that the plot speeds will be affected as your bandwidth is being used up....


## Prerequisites

You will require the following for this to run:

Python 3.x

speedtest-cli

matplotlib

numpy

## Install

Best to run everything as super-user so that you have permissions to create new files.

apt-get install python3-setuptools python3-dev build-essential 

git clone https://github.com/brentoncollins/internet-speed-plot

python3 setup.py install

python3 speed.py


## Feedback

If you have anyfeedback, or it doesnt work, please message me as this is the first commit and I most probably have forgotten something.
brenton.collins@outlook.com
