import io
import os.path
import subprocess
from setuptools import setup, find_packages
from distutils.cmd import Command

from setuptools_rust import RustExtension


NAME = "simple-rsync"
VERSION = None
DESCRIPTION = "Simple Python interface for librsync"

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
    with io.open(os.path.join(here, "README.md"), encoding="utf-8") as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

about = {}
if not VERSION:
    project_slug = NAME.lower().replace("-", "_").replace(" ", "_")
    with open(os.path.join(here, "package", project_slug, "__version__.py")) as f:
        exec(f.read(), about)
else:
    about["__version__"] = VERSION


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
    name=NAME,
    version=about["__version__"],
    package_dir={"": "package"},
    packages=find_packages("package"),
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Yavor Atov",
    author_email="yavor.atov@gmail.com",
    url="https://github.com/YAtOff/simple-rsync",
    license="Apache",
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Rust"
    ],
    python_requires=">=3.7",
    tests_require=["pytest>=6", "flake8>=3"],
    cmdclass={"test": TestCommand},
    rust_extensions=[RustExtension("simple_rsync.simple_rsync", "Cargo.toml", debug=False)],
    include_package_data=True,
    zip_safe=False
)
