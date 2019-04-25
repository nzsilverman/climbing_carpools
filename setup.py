"""
Climbing Carpool Scheduler

Nathan Silverman <nzsilver@umich.edu>
"""

from setuptools import setup


# Note to self, look at 485 p1, maybe need an install requires

setup(
    name='scheduler',
    version='0.1.0',
    packages=['scheduler'],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'scheduler = scheduler.__main__:main'
        ]
    },
)
