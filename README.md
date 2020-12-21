# Simple Python interface for librsync

## Install

`pip install simple-rsync`

## Build

1. Make sure Rust toolchain is installed. If not goto https://rustup.rs/ to install it.
2. Create an virtual environment and run: `python setup.py develop` for develop build 
or `python setup.py install` for release build

## Verify

`python setup.py test`

## Use

```python
from simple_rsync import signature, delta, patch


base_file = "base"
new_file = "new"
signature_file = "sig"
delta_file = "delta"
result_file = "result"

signature(base_file, signature_file, block_len=1024, strong_len=8)
delta(new_file, signature_file, delta_file)
patch(base_file, delta_file, result_file)

with open(new_file, "rb") as expected:
    with open(result_file, "rb") as result:
        assert expected.read() == result.read()
```

## Release on Mac OSX

Set `MACOSX_DEPLOYMENT_TARGET` if you want the wheel to be compatible with older versions.
For CPython from Python.org: `MACOSX_DEPLOYMENT_TARGET=10.9 python setup.py bdist_wheel`.
For custom bulid of `librsync` again see the instructions for Windows.
