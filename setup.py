import sys
from setuptools import setup
from goread import __version__, __author__, __url__, __license__

setup(
    name = "goread",
    version = __version__,
    description = "Fetch Book info / Author's 30 top works via CLI",
    url = __url__,
    author = __author__,
    license = __license__,
    keywords = ["Book", "Author", "Read"],
    install_requires = [],
    python_requires = "~=3.7",
    py_modules = ["goread"],
    entry_points = { "console_scripts": ["goread = goread:main"] }
)
