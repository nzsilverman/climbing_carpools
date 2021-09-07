""" Script that installs dependencies needed for this project.

    Typical Usage Example: (from command line)

        pip install -e .
"""

from setuptools import setup, find_packages
from scheduler.util import get_version

version = get_version()

setup(
    name="scheduler",
    version=version,
    author="Roberts Kalnins, Nathan Silverman",
    author_email="rkalnins@umich.com",
    description="Climbing Club Carpool Scheduling Software",
    packages=find_packages(),
    install_requires=[
        "gspread", "gspread-formatting", "oauth2client", "toml", "nose2"
    ],
    include_package_data=True,
    entry_points={"console_scripts": ["scheduler = scheduler.__main__:main",]},
    test_suite="nose2.collector.collector",
    tests_require=["nose2"],
    python_requires=">=3.6",
)
