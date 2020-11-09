import sys

if sys.version_info.major != 3 or sys.version_info.minor < 7:
    print("Error: you must execute setup.py using Python 3.7 or later")
    sys.exit(1)

from setuptools import setup, find_packages

exec(open("SoftClipper/version.py").read())

with open("README.md", "rb") as readme:
    DESCR = readme.read().decode()


setup(
    name="SoftClipper",
    version=__version__,
    packages=find_packages(),
    install_requires=[
        'pysam>=0.16'
    ],
    entry_points={"console_scripts": ['SoftClipper = SoftClipper.SoftClipper:main']},
    keywords=[],
    zip_safe=False
)
