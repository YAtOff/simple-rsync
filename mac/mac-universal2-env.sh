#!/bin/bash

python_version=$(python -c 'import platform; print(".".join(platform.python_version_tuple()[:2]))')
export CMAKE_OSX_ARCHITECTURES="arm64;x86_64"
export PYO3_CROSS_LIB_DIR="/Library/Frameworks/Python.framework/Versions/${python_version}/lib/"
export PYO3_CROSS_PYTHON_VERSION="${python_version}"
export DEVELOPER_DIR=/Applications/Xcode.app/Contents/Developer
export MACOSX_DEPLOYMENT_TARGET='10.13'
export ARCHFLAGS='-arch x86_64 -arch arm64'

