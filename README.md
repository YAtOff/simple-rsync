# Simple Python interface for librsync

## Build

1. Make sure Rust toolchain is installed. If not goto https://rustup.rs/ to install it.
2. Create an virtual environment and run: `python setup.py install`

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
