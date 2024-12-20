from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="namespi", 
    version="1.7.1", 
    description="An OSINT employee/username enumeration tool.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Waffl3ss",
    author_email="name@example.com",
    url="https://github.com/waffl3ss/NameSpi",
    packages=find_packages(),
    py_modules=["NameSpi"],
    install_requires=[
        "requests",
	"pyhunter",
	"PyYAML",
	"Unidecode",
	"yaspin",
    ],
    entry_points={
        "console_scripts": [
            "namespi=NameSpi:main_generator",        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
