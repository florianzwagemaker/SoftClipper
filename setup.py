import sys

from setuptools import find_packages, setup

from ReadClipper import __version__

if sys.version_info.major != 3 or sys.version_info.minor < 10:
    print("Error: you must execute setup.py using Python 3.10 or later")
    sys.exit(1)


with open("README.md", "rb") as readme:
    DESCR = readme.read().decode()


setup(
    name="ReadClipper",
    version=__version__,
    packages=find_packages(),
    install_requires=["pysam==0.22.0"],
    entry_points={
        "console_scripts": [
            "readclipper = ReadClipper.__main__:main",
            "ReadClipper = ReadClipper.__main__:main",
        ]
    },
    keywords=[],
    zip_safe=False,
)
