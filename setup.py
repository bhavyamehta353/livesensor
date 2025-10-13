# Why and what is the use of this file ---> install dependencies, packages, modules. Handles metadata.
from setuptools import find_packages, setup
from typing import List


def get_requirements()->List[str]: #--> we are returning a list of strings
    req_list : List[str] = []
    return req_list


setup(
    name = 'APS FAULT PREDICTION',
    version = '0.0.1',
    author = "Bhavya Mehta",
    author_email = "bhavyamehta353@gmail.com",
    packages = find_packages(), # ---> finds all packages in the environment
    install_requires = get_requirements(), #["pymongo"]
)