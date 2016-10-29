
from setuptools import setup
setup(
    name='pynverse',
    packages=['pynverse'],
    version='0.1.1',
    description='A library for calculating the numberical inverse of a function',
    author='Alvaro Sanchez-Gonzalez',
    author_email='sanchezgnzlz.alvaro@gmail.com',
    url='https://github.com/alvarosg/pynverse',
    download_url='https://github.com/alvarosg/pynverse/tarball/0.1.1',
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
    install_requires=['scipy','numpy'],
)



def configuration(parent_package='', top_path=None):
    from numpy.distutils.misc_util import Configuration
    config = Configuration(None, parent_package, top_path)
    config.set_options(ignore_setup_xxx_py=True,
                       assume_default_configuration=True,
                       delegate_options_to_subpackages=True,
                       quiet=True)

    config.add_subpackage('pynverse')
    return config
