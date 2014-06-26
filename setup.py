from setuptools import setup, find_packages

setup(
    name='variant_annotation',
    version='1.0.0',
    packages=find_packages(exclude=['test-data']),
    install_requires=['sbgsdk']
)
