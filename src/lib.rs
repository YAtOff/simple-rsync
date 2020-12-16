extern crate librsync;

use std::fs::File;
use std::io::{BufReader};

use librsync::whole::signature_with_options as librsync_signature;
use librsync::whole::delta as librsync_delta;
use librsync::whole::patch as librsync_patch;
use librsync::SignatureType;
use librsync::Error as LibrsyncError;
use pyo3::prelude::*;
use pyo3::wrap_pyfunction;
use pyo3::exceptions::PyOSError;


fn librsync_to_py_error(librsync_error: LibrsyncError) -> PyErr {
    PyOSError::new_err(format!("{}", librsync_error))
}

#[pyfunction]
fn signature(data_file_path: &str, signature_file_path: &str, block_len: usize, strong_len: usize) -> PyResult<u64> {
    let data_file = File::open(data_file_path)?;
    let mut data_file = BufReader::new(data_file);
    let mut signature_file = File::create(signature_file_path)?;
    librsync_signature(
        &mut data_file,
        &mut signature_file,
        block_len,
        strong_len,
        SignatureType::MD4
    ).map_err(librsync_to_py_error)
}

#[pyfunction]
fn delta(data_file_path: &str, signature_file_path: &str, delta_file_path: &str) -> PyResult<u64> {
    let mut data_file = File::open(data_file_path)?;
    let mut signature_file = File::open(signature_file_path)?;
    let mut delta_file = File::create(delta_file_path)?;
    librsync_delta(
        &mut data_file,
        &mut signature_file,
        &mut delta_file
    ).map_err(librsync_to_py_error)
}


#[pyfunction]
fn patch(base_file_path: &str, delta_file_path: &str, result_file_path: &str) -> PyResult<u64> {
    let mut base_file = File::open(base_file_path)?;
    let mut delta_file = File::open(delta_file_path)?;
    let mut result_file = File::create(result_file_path)?;
    librsync_patch(
        &mut base_file,
        &mut delta_file,
        &mut result_file
    ).map_err(librsync_to_py_error)
}

/// A Python module implemented in Rust.
#[pymodule]
fn simple_rsync(py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(signature, m)?)?;
    m.add_function(wrap_pyfunction!(delta, m)?)?;
    m.add_function(wrap_pyfunction!(patch, m)?)?;

    Ok(())
}
