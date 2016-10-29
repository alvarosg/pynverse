
from distutils.core import setup
setup(
    name='pynverse',
    packages=['pynverse'],
    version='0.1',
    description='A library for calculating the numbericla inverse of a function',
    author='Alvaro Sanchez-Gonzalez',
    author_email='sanchezgnzlz.alvaro@gmail.com',
    url='https://github.com/alvarosg/pynverse',
    download_url='https://github.com/alvarosg/pynverse/tarball/0.1',
    keywords=['inverse', 'function', 'numerical'],
    classifiers=[],
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

if __name__ == '__main__':
    from numpy.distutils.core import setup
    setup(**configuration(top_path='').todict())
