from setuptools import setup, find_packages
import os

VERSION = "2.0.0-beta1"
DESCRIPTION = "aquova's common bot package"
LONG_DESCRIPTION = "A package containing common functionality for my Discord bots"

os.chdir(os.path.dirname(__file__))
setup(
    name="commonbot",
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    package_data={"commonbot": ["py.typed"]},
    install_requires=[]
)
