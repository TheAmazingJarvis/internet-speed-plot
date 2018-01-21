from setuptools import setup
import sys

if sys.version_info <= (3,0):
	sys.stdout.write('\033[1;31m\nSorry, requires Python 3.x, not Python 2.x\n\033[1;m')
	sys.exit(1)
	
	
setup(
    name='Internet-speed-plot',
    version='1.0',
    packages=[],
    url='',
    license='MIT',
    author='Brenton Collins',
    author_email='brenton.collins@outlook.com',
	description='Creates a plot image with matplotlib and Speedtest API hourly',
    install_requires=[
        'speedtest-cli',
        'matplotlib',
        'numpy',
    ],
)
