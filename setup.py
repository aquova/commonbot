from setuptools import setup, find_packages
import os

VERSION = "1.7.3.2"
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
    install_requires=["py-cord==1.7.3"]
)
