from setuptools import setup, find_packages

setup(
    name="namespi", 
    version="1.7.0", 
    description="An OSINT employee/username enumeration tool.",
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
