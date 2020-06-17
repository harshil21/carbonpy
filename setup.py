from setuptools import setup, find_packages
import os

with open("README.md", 'r') as f:
    long_description = f.read()

fn = os.path.join('carbonpy', 'version.py')
with open(fn) as fh:
    code = compile(fh.read(), fn, 'exec')
    exec(code)

setup(
    name='carbonpy',
    version=__version__,
    author='Harshil Mehta',
    author_email='ilovebhagwan@gmail.com',
    description="A Python package which gives IUPAC names of chemical compounds, classifies them and more.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/harshil21/carbonpy',
    packages=find_packages(exclude=['tests*']),
    classifiers=['Development Status :: 1 - Planning',
                 'Intended Audience :: Science/Research',
                 'Intended Audience :: Education',
                 'License :: OSI Approved :: Apache Software License',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python :: 3',
                 'Topic :: Scientific/Engineering :: Chemistry'],
    python_requires='>=3.6')
