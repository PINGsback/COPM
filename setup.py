from setuptools import setup, find_packages

requirements = ["clipboard", "pyperclip"]

setup(
    name="COPM",
    version="0.0.1",
    author="yo mum",
    author_email="pingsback@gmail.com",
    description="A really bad password manager for chrome os. Run in tkinter.",
    url="https://github.com/PINGsback/COPM/",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)