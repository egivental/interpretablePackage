import setuptools

with open("README.md") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "Interpretability",
    version = "0.0.2",
    author = "Emile Givental",
    author_email = "emilegivental@gmail.com",
    description="A selection of interpretable methods with logging and printouts",
    long_description=long_description,
    url="https://github.com/egivental/resetInterpretability",
    packages = setuptools.find_packages(),
    install_requires = ['Prettytable>=0.7.2', 'pandas>=0.24.2', 'numpy>=1.16.4', 'sklearn>=0.0'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent"
    ],

    )

