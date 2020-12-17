# Build `simple-rsync` on Windows

The following instructions describe how to build `librsync` manually
on Windows with Visual Studio and how to use the compiled library in `librsync-rs`.

## Clone `librsync`

```
git clone https://github.com/librsync/librsync.git
git clone https://github.com/mbrt/librsync-rs.git
```

## Build `librsync`

The instructions are for librsync `v2.3.1`.

```
cd librsync
git checkout v2.3.1
# Fix CMakeLists.txt
git apply ..\CMakeLists.txt.diff
cmake -B build -A x64 -D BUILD_SHARED_LIBS=OFF .
cd build
```

Now open `librsync.sln` with Visual Studio and build `rsync` for release.

## Use in `librsync-rs`

In `librsync-rs/librsync-sys`:

- replace `build.rs` with the current one
- add `links = "rsync"` at the end of `package` section
- put the compiled library `build\Release\rsync.lib` into `librsync-sys\lib\librsync.a`

## Use `librsync-rs` in current package

Now in the current package `Cargo.toml` replace `librsync = "0.2.1`
with `librsync = { path = "windows/librsync-rs" }`.

Then just proceed with `python setup.py install`.
