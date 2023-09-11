"""Builds the project as a CLI executable
"""
from setuptools import setup, find_packages

setup(
    name='droneframe',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        'argparse'
    ],
    entry_points={
        'console_scripts': [
            'droneframe = droneframe.cli:main',
        ],
    },
    author='Anwar Ali-Ahmad',
    author_email='contact@anwaraliahmad.tech',
    description='Extract frames from drone footage along with their EXIF data.',
    license='MIT',
    url='https://github.com/anwaraliahmad/droneframe',
    long_description=open('README.md', encoding="utf-8").read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.11',
    ],
)
