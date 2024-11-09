from setuptools import find_packages, setup

setup(
    name="kiteplay",
    packages=find_packages(exclude=["kiteplay_tests"]),
    install_requires=[
        "dagster",
        "dagster-cloud"
    ],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)
