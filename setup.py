from setuptools import setup
from setuptools import find_packages
import re
from os.path import abspath, dirname, join

CURDIR = dirname(abspath(__file__))

#with open("README.rst", "r", encoding='utf-8') as fh:
#    long_description = fh.read()

with open(join(CURDIR, 'LiveResults', 'LiveResults.py'), encoding='utf-8') as f:
    VERSION = re.search("\n__version__ = '(.*)'", f.read()).group(1)

setup(
    name="robotframework-liveresults",
    version=VERSION,
    author="xyz",
    author_email="xyz@dummyo.de",
    description="A listener for Live Results of Robot Framework execution.",
    long_description="To be done",
    long_description_content_type="text/x-rst",
    url="https://github.com/franky1964/RF-LiveResults",
    packages=['LiveResults'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Testing :: Acceptance",
        "Framework :: Robot Framework",
    ],
    install_requires=[
        'robotframework >= 3.1',
        'robotframework-screencaplibrary'
    ],
    python_requires='>=3.6'
)

