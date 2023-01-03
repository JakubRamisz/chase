from setuptools import setup, find_packages

with open("README.md", "r", encoding='UTF-8') as readme:
    desc = readme.read()

setup(
    name='chase',
    version='1.0',
    description='Simple simulation of a wolf chasing sheep',
    long_description=desc,
    url='https://github.com/JakubRamisz/chase',
    author='Jakub Ramisz',
    license='MIT',
    packages=find_packages()
)
