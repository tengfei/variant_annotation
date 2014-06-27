from setuptools import setup, find_packages

setup(
    name='variant_annotation',
    version='1.0.0',
    packages=find_packages(exclude=['test-data']),
    install_requires=['sbgsdk'],
    include_package_data=True,
    package_data={
        'variant_annotation': ['*.R']
    }
)
