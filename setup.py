from setuptools import setup, find_packages

setup(
    name="einstein-models",
    version="0.1.1",
    packages=find_packages(),
    package_data={
        'einstein_models': ['data/*.py'],
        'einstein_models.models': ['models/*.py'],
        'einstein_models.rest': ['rest/*.py'],

    },
    install_requires=[
        "requests",
        "python-dotenv",
    ],
    author="Amir Khan",
    author_email="amir.khan@salesforce.com",
    description="Python SDK for Salesforce Einstein Models API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/amirkhan-ak-sf/einstein-models",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
) 