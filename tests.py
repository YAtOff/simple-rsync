import os
import tempfile

import pytest

from simple_rsync import signature, delta, patch


class FileManager:
    def __init__(self) -> None:
        self.files = []

    def create(self) -> str:
        fd, path = tempfile.mkstemp()
        os.close(fd)
        self.files.append(path)
        return path

    def cleanup(self) -> None:
        for file in self.files:
            try:
                os.unlink(file)
            except OSError:
                pass


block_len = 1024
strong_len = 8


@pytest.fixture
def file_manager():
    manager = FileManager()
    try:
        yield manager
    finally:
        manager.cleanup()


def test_full_workflow(file_manager):
    base_file = file_manager.create()
    with open(base_file, "wb") as f:
        f.write(os.urandom(1024 * 10 + 512))

    signature_file = file_manager.create()
    signature(base_file, signature_file, block_len, strong_len)

    new_file = file_manager.create()
    with open(base_file, "rb") as src:
        with open(new_file, "wb") as dest:
            dest.write(os.urandom(512))
            dest.write(src.read(5 * 1024))
            dest.write(os.urandom(512))
            dest.write(src.read())
            dest.write(os.urandom(512))

    delta_file = file_manager.create()
    delta(new_file, signature_file, delta_file)

    result_file = file_manager.create()
    patch(base_file, delta_file, result_file)

    with open(new_file, "rb") as expected:
        with open(result_file, "rb") as result:
            assert expected.read() == result.read()


def test_err_invalid_base_file(file_manager):
    signature_file = file_manager.create()
    with pytest.raises(FileNotFoundError):
        signature("invalid", signature_file, block_len, strong_len)


def test_err_invalid_signature(file_manager):
    signature_file = file_manager.create()
    with open(signature_file, "wb") as f:
        f.write(os.urandom(100))
    new_file = file_manager.create()
    delta_file = file_manager.create()
    with pytest.raises(OSError):
        delta(new_file, signature_file, delta_file)


def test_err_invalid_delta(file_manager):
    base_file = file_manager.create()
    delta_file = file_manager.create()
    with open(delta_file, "wb") as f:
        f.write(os.urandom(100))
    result_file = file_manager.create()
    with pytest.raises(OSError):
        patch(base_file, delta_file, result_file)
