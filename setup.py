from setuptools import find_packages, os, setup

with open(
    os.path.join(os.path.abspath(os.path.dirname(__file__)), "adz/__init__.py")
) as f:
    META = {
        x[0]: x[1].strip()[1:-1]
        for x in [l.split(" = ", 1) for l in f.readlines() if not l.find("__")]
    }

with open("readme.md") as f:
    long_description = f.read()

setup(
    name="adz",
    version=META["__version__"],
    author="ambrozic",
    author_email="ambrozic@gmail.com",
    maintainer="ambrozic",
    maintainer_email="ambrozic@gmail.com",
    description="Command line interface for HTTP requests defined in yaml configuration file",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="BSD",
    url="https://github.com/ambrozic/adz",
    project_urls={
        "Code": "https://github.com/ambrozic/adz",
        "Documentation": "https://github.com/ambrozic/adz",
    },
    keywords="cli http requests yaml",
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    python_requires=">=3.6",
    install_requires=[
        "click==7.0,<8.0",
        "pyaml>=19.4,<20.0",
        "pygments>=2.4,<3.0",
        "requests>=2.0.0,<3.0.0",
    ],
    extras_require={
        "tests": [
            "black==19.10b0",
            "codecov>=2.0,<3.0",
            "isort>4.0,<5.0",
            "pipdeptree>=0.13,<1.0",
            "pytest-asyncio==0.10.0",
            "pytest-cov>=2.7,<3.0",
            "pytest>=5.0,<6.0",
            "uvicorn>=0.8.0,<0.9.0",
        ]
    },
    entry_points={"console_scripts": ["adz=adz.cli:main"]},
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python",
        "Environment :: Web Environment",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Intended Audience :: Developers",
    ],
)
