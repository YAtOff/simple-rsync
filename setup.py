import subprocess
from setuptools import setup, find_packages
from distutils.cmd import Command

from setuptools_rust import RustExtension


class TestCommand(Command):
    description = "run test commands"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        subprocess.check_call(["flake8"])
        subprocess.check_call(["pytest", "tests.py"])


setup(
    name="simple-rsync",
    version="0.1.0",
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Rust"
    ],
    packages=find_packages(),
    python_requires=">=3.7",
    tests_require=["pytest>=6", "flake8>=3"],
    cmdclass={"test": TestCommand},
    rust_extensions=[RustExtension("simple_rsync", "Cargo.toml", debug=False)],
    include_package_data=True,
    zip_safe=False
)
