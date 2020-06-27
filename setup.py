"""
Climbing Carpool Scheduler

Nathan Silverman <nzsilver@umich.edu>
"""

from setuptools import setup, find_packages


# Note to self, look at 485 p1, maybe need an install requires

setup(
    name="scheduler",
    version="20.0.0-alpha",
    packages=find_packages(),
    install_requires=["gspread", "oauth2client", "pandas"],
    include_package_data=True,
    entry_points={"console_scripts": ["scheduler = scheduler.__main__:main",]},
    test_suite="nose2.collector.collector",
    tests_require=["nose2"],
)
