from setuptools import setup, find_packages
import os

VERSION = "1.1.1"
DESCRIPTION = "aquova's common bot package"
LONG_DESCRIPTION = "A package containing common functionality for my Discord bots"

os.chdir(os.path.dirname(__file__))
setup(
    name="commonbot",
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=["discord.py==1.5.1"]
)
