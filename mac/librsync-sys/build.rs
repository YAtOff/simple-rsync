use std::env;
use std::path::PathBuf;

fn main() {
    let mut lib_path = PathBuf::from(env::var("CARGO_MANIFEST_DIR").unwrap());
    lib_path.push("lib");

    println!(
        "cargo:rustc-link-search=native={}",
        lib_path.to_str().unwrap()
    );
    println!("cargo:rustc-link-lib=static=rsync");
}
