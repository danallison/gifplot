from setuptools import setup

with open('README.md', 'r') as readme:
    long_description = readme.read()

setup(
    name='gifplot',
    version='0.0.1',
    description='Make animated gifs with matplotlib',
    long_description=long_description,
    url='https://github.com/danallison/gifplot',
    author='Dan Allison',
    author_email='daniel.j.allison@gmail.com',
    license='MIT',
    packages=['gifplot'],
    install_requires=['numpy', 'matplotlib']
)
