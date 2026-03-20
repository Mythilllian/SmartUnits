from setuptools import setup

setup(
    name="smartunits",
    version="0.1.0",
    description="Standardized units for robotics",
    url="https://github.com/Mythilllian/SmartUnits",
    license="Unlicense",
    packages=["smartunits"],
    install_requires=[],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
)
