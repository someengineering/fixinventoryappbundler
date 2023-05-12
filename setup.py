import os
import pkg_resources
import resotoappbundler
from setuptools import setup, find_packages


def read(file_name: str) -> str:
    with open(os.path.join(os.path.dirname(__file__), file_name)) as of:
        return of.read()


setup(
    name=resotoappbundler.__title__,
    version=resotoappbundler.__version__,
    description=resotoappbundler.__description__,
    license=resotoappbundler.__license__,
    packages=find_packages(),
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    entry_points={
        "console_scripts": [
            "resotoappbundler = resotoappbundler.__main__:main",
        ]
    },
    include_package_data=True,
    zip_safe=False,
    install_requires=[str(requirement) for requirement in pkg_resources.parse_requirements(read("requirements.txt"))],
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    classifiers=[
        # Current project status
        "Development Status :: 4 - Beta",
        # Audience
        "Intended Audience :: System Administrators",
        "Intended Audience :: Information Technology",
        # License information
        "License :: OSI Approved :: Apache Software License",
        # Supported python versions
        "Programming Language :: Python :: 3.9",
        # Supported OS's
        "Operating System :: POSIX :: Linux",
        "Operating System :: Unix",
        # Extra metadata
        "Environment :: Console",
        "Natural Language :: English",
        "Topic :: Security",
        "Topic :: Utilities",
    ],
    keywords="cloud security",
    url="https://github.com/someengineering/resoto-apps/tree/main/resotoappbundler",
)
