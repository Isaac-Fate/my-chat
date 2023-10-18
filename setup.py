from setuptools import setup

setup(
    name="my-chat",
    version="0.0.1",
    packages=["mychat"],
    entry_points={
        "console_scripts": [
            "mychat = mychat:main",
        ],
    },
)
