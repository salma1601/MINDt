
import os
from setuptools import setup


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="mindt",
    version="alpha",
    maintainer="Nachiket Nadkarni",
    maintainer_email="nadkarni@fastmail.fm",
    description=("MRI Rodents processing in python."),
    license="CeCILL-B",
    keywords="rodents registration dicom",
    url="https://github.com/samll-animal-MRI/MINDt",
    packages=['mindt', ],
    long_description=read('README.rst'),
    classifiers=[
        "Topic :: Scientific/Engineering",
        "License :: CeCILL-B",
    install_requires=[matplotlib >= 1.1.1,
		     nibabel >= 2.0.1,
		     nipype == 0.11.0,
                     nose == 1.3.1,
		     nose-cov,
		     numpy >= 1.6.2,
		     setuptools >= 3.3,
		     scikit-learn >= 0.15,
		     nilearn >= 0.1.3,
		     pandas >= 0.12,
		     scipy >= 0.11,
		     numpydoc >= 0.5,
		     ipython,
		     Sphinx,
		     sphinx-rtd-theme,
		     Pillow]],
)
