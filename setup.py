#!/usr/bin/env python

from setuptools import setup, find_packages

application_dependencies = ["requests>=2.32", "tenacity>= 9.0.0"]

prod_dependencies = []

test_dependencies = ["pytest", "pytest-env", "pytest-cov", "vcrpy", "requests-mock"]
lint_dependencies = ["flake8", "flake8-docstrings", "black", "isort"]
docs_dependencies = []

dev_dependencies = test_dependencies + lint_dependencies + docs_dependencies + ["ipdb"]
deploy_dependencies = ["requests", "twine"]


with open("README.md", "r") as fh:
    long_description = fh.read()


with open("VERSION", "r") as buf:
    version = buf.read()


setup(
    name="python-presenter",
    version=version,
    description="Presenter pattern to help manage the complexity of bloated controllers/views and logic-laden templates",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Olaoluwa Afolabi",
    author_email="afolabiolaoluwa@gmail.com",
    url="https://github.com/AfolabiOlaoluwa/python-presenter",
    python_requires=">=3.6",
    packages=find_packages(exclude=["tests*", "docs*"]),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
    ],
    install_requires=application_dependencies,
    extras_require={
        "production": prod_dependencies,
        "test": test_dependencies,
        "lint": lint_dependencies,
        "docs": dev_dependencies,
        "dev": dev_dependencies,
        "deploy": deploy_dependencies,
    },
    include_package_data=True,
    zip_safe=False,
)