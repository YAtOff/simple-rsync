Clone librsync

```
git clone https://github.com/librsync/librsync.git
git clone https://github.com/mbrt/librsync-rs.git
```

The instructions are for librsync `v2.3.1`.
```
cd librsync
git checkout v2.3.1
# Fix CMakeLists.txt
git apply ..\CMakeLists.txt.diff
cmake -B build -A x64 -D BUILD_SHARED_LIBS=OFF .
cd build
```

Now open `librsync.sln` with Visual Studio and build for release. The build
will fail with `C2491`. To fix it remove the `LIBRSYNC_EXPORT` macro in the
places with compiler error.

Then in `librsync-rs` replace `librsync-sys` with the current one
and put the compiled library `build\Release\rsync.lib` into
`librsync-sys\lib\librsync.a`.

Now in the current package `Cargo.toml` replace `librsync = "0.2.1`
with `librsync = { path = "windows/librsync-rs" }`.

Now just proceed with `python setup.py install`.
