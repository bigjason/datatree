from os import path
from setuptools import setup, find_packages

from datatree import VERSION

with open(path.join(path.dirname(__file__), 'README.rst')) as f:
    readme = f.read()

setup(
    name='datatree',
    version='.'.join(map(str, VERSION)),
    license='Creative Commons Attribution 3.0 Unported License',
    description='DataTree is a DSL for creating structured documents in python.',
    long_description=readme,
    url='https://github.com/bigjason/datatree',
    author='Jason Webb',
    author_email='bigjasonwebb@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
       'Development Status :: 4 - Beta',
       'Topic :: Text Processing :: Markup',
       'Topic :: Text Processing :: Markup :: XML',
       'Operating System :: OS Independent',
       'Intended Audience :: Developers',
       'Programming Language :: Python :: 2.6',
       'Programming Language :: Python :: 2.7'
    ]
)
