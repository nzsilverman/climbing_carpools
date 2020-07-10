from setuptools import setup, find_packages

setup(
    name="scheduler",
    version="2.0.0",
    author="Nathan Silverman",
    author_email="nzsilverman@gmail.com",
    description="Climbing Club Carpool Scheduling Software",
    packages=find_packages(),
    install_requires=["gspread", "gspread-formatting", "oauth2client", "toml"],
    include_package_data=True,
    entry_points={"console_scripts": ["scheduler = scheduler.__main__:main",]},
    test_suite="nose2.collector.collector",
    tests_require=["nose2"],
    python_requires=">=3.6",
)
