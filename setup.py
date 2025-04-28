from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="glik-sdk",
    version="0.1.10",
    author="Glik",
    author_email="hello@glik.ai",
    description="A package for interacting with the Glik Service-API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rivalz-glik/glik-sdk",
    license='MIT',
    packages=['glik_sdk'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "requests"
    ],
    keywords='glik nlp ai language-processing',
    include_package_data=True,
)
