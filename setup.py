from setuptools import setup, find_packages
import sys
from simplefind import __version__


with open("README.rst") as thefile:
    README = thefile.read()

setup(
    name="simplefind",
    version=__version__,
    packages=find_packages(),
    author="Vince Veselosky",
    author_email="vince@veselosky.com",
    description="",
    long_description=README,
    license="MIT",
    url="",
    # could also include download_url, classifiers, etc.
    install_requires=["click"],
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    entry_points={"console_scripts": ["ff=simplefind.tool:find"]},
)
