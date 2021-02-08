from setuptools import setup, find_namespace_packages

setup(name='acxDataProcessor', version='1.0', packages=find_namespace_packages(include=['acxDataProcessor.*']), install_requires=['requests', 'pyyaml', 'flatten_json'])
