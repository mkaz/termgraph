try:
    from setuptools import setup
except ImportError:
    raise ImportError(
        "setuptools module required, please go to "
        "https://pypi.python.org/pypi/setuptools and follow the instructions "
        "for installing setuptools"
    )
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='termgraph',
    packages=['termgraph'],
    entry_points={'console_scripts': ['termgraph=termgraph.termgraph:main']},
    version='0.1.4',
    author="mkaz",
    author_email="marcus@mkaz.com",
    url='https://github.com/mkaz/termgraph',
    download_url='https://pypi.python.org/pypi/termgraph/',
    license='MIT',
    description='a python command-line tool which draws basic graphs in the terminal',
    platforms='any',
    keywords='python CLI tool drawing graphs shell terminal',
    python_requires='>=3.6',
    install_requires=['colorama'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6'],
    long_description=long_description,
    long_description_content_type='text/markdown'
)
