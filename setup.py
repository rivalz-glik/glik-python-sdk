from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

requirements = [
    "requests>=2.25.1",
    "pydantic>=1.8.2",
]

setup(
    name="glik-sdk",
    version="0.0.1",
    author="Glik",
    author_email="hello@glik.ai",
    description="A Python SDK for interacting with the Glik Service-API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rivalz-glik/glik-sdk",
    project_urls={
        "Bug Tracker": "https://github.com/rivalz-glik/glik-sdk/issues",
        "Documentation": "https://github.com/rivalz-glik/glik-sdk#readme",
    },
    license="MIT",
    packages=find_packages(include=["glik_sdk", "glik_sdk.*"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.6",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "isort>=5.0",
            "flake8>=3.9",
            "mypy>=0.910",
        ],
    },
    keywords="glik nlp ai language-processing api sdk",
    include_package_data=True,
    zip_safe=False,
)
