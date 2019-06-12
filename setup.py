from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='Pituophis',
    version='1.0',
    install_requires=['natsort'],
    packages=['pituophis'],
    url='https://github.com/dotcomboom/Pituophis',
    license='BSD 2-Clause License',
    author='dotcomboom',
    author_email='dotcomboom@protonmail.com',
    description='Python 3 library for building Gopher clients and servers',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent"
    ],
)
