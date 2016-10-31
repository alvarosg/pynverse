
from setuptools import setup, find_packages
import imp

version = imp.load_source('pynverse.version', 'pynverse/version.py')
rev = version.git_revision

setup(
    name='pynverse',
    packages=find_packages(),
    version=rev,
    description='A library for calculating the numerical inverse of a function',
    author='Alvaro Sanchez-Gonzalez',
    author_email='sanchezgnzlz.alvaro@gmail.com',
    url='https://github.com/alvarosg/pynverse',
    download_url='https://github.com/alvarosg/pynverse/tarball/' + rev,
    keywords=['inverse', 'function', 'numerical'],
    license='MIT',
    classifiers=[
            'Development Status :: 4 - Beta',
            'Intended Audience :: Developers',
            'Topic :: Software Development :: Build Tools',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.2',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
    ],
    test_suite='nose.collector',
    install_requires=['scipy>=0.11', 'numpy>=1.6'],
    setup_requires=['nose>=1.0', 'scipy>=0.11', 'numpy>=1.6'],
    tests_require=['nose>=1.0', 'scipy>=0.11', 'numpy>=1.6'],
)