from setuptools import find_packages, setup

setup(
    name="smartunits",
    version="0.1.0",
    description="Standardized unit system. Follows the standards used by WPILibJ. Includes a unit system, unit conversion, and unit arithmetic.",
    url="https://github.com/Mythilllian/SmartUnits",
    license="Unlicense",
    packages=find_packages(),
    install_requires=["jinja2"],
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
)
