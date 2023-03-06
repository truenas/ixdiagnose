from distutils.core import setup
from setuptools import find_packages

VERSION = '0.1'

setup(
    name='ixdiagnose',
    description='Generate TrueNAS Scale System Debug',
    version=VERSION,
    include_package_data=True,
    packages=find_packages(),
    license='GNU3',
    platforms='any',
    entry_points={
        'console_scripts': [
            'ixdiagnose2 = ixdiagnose.main:cli'
        ]
    }
)
