"""
DocWal Python SDK setup
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="docwal",
    version="1.0.1",
    author="DocWal",
    author_email="support@docwal.com",
    description="Official Python SDK for DocWal API - Issue and manage verifiable digital credentials",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/docwal/docwal-python",
    project_urls={
        "Bug Tracker": "https://github.com/docwal/docwal-python/issues",
        "Documentation": "https://docs.docwal.com",
        "Source Code": "https://github.com/docwal/docwal-python",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.25.0",
    ],
    keywords="docwal credentials verifiable digital education blockchain",
)
