# A script to build a .py file from .ui file made in QtCreator.
from setuptools import setup

try:
    from pyqt_distutils.build_ui import build_ui
    cmdclass = {"build_ui": build_ui}
except ImportError:
    cmdclass = {}

setup(
    name="crypto_dna",
    version="1.0",
    packages=["crypto_dna"],
    cmdclass=cmdclass,
)
