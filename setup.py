from setuptools import setup, find_packages
from hbpair import __version__

setup(
    name="hbpair-cli",
    version=__version__,
    packages = find_packages(exclude=['docs', 'tests*']),
    install_requires = ['docopt'],
    entry_points = {
        'console_scripts': [
            'hbpair=hbpair.cli:main',
        ],
    },
    description='Pair programming utilities',
    author='Ashley Trinh',
    author_email='ashley.trinh@hackbrightacademy.com',
    license='MIT',
)
