from os import path
from setuptools import setup, find_packages

from datatree import VERSION

with open(path.join(path.dirname(__file__), 'README.md')) as f:
    readme = f.read()

setup(
    name="datatree",
    version=".".join(map(str, VERSION)),
    license="Creative Commons Attribution 3.0 Unported License",
    description="DataTree is a DSL for creating structured documents in python.",
    long_description=readme,
    url="https://github.com/bigjason/datatree",
    author="Jason Webb",
    author_email="bigjasonwebb@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
       "Operating System :: OS Independent",
       "Intended Audience :: Developers",
       "Programming Language :: Python :: 2.7"
    ]
)
