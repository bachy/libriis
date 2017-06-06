from setuptools import setup, find_packages

setup(
    name="Cascade",
    version="0.0.1",
    packages=find_packages(),
    entry_points={
        'gui_scripts': [
            'cascade = cascade.main:__main__',
        ]
    }
)
